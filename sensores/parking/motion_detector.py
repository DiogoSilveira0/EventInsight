import cv2
import numpy as np
import logging
from drawing_utils import draw_contours
from colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE

import json
from datetime import datetime
import time

import sys
sys.path.insert(0,'..')
from send_message import SendMessage

# function to check if parking slot is free or not
class MotionDetector:
    LAPLACIAN = 1.4
    DETECT_DELAY = 1

    def __init__(self, video, coordinates, start_frame):
        self.video = video
        self.coordinates_data = coordinates
        self.start_frame = start_frame
        self.contours = []
        self.bounds = []
        self.mask = []
        #self.publisher = SendMessage('queue13')

    def detect_motion(self):
        capture = cv2.VideoCapture(self.video)
        capture.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)

        coordinates_data = self.coordinates_data
        logging.debug("coordinates data: %s", coordinates_data)

        for p in coordinates_data:
            coordinates = self._coordinates(p)
            logging.debug("coordinates: %s", coordinates)

            rect = cv2.boundingRect(coordinates)
            logging.debug("rect: %s", rect)

            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1]
            logging.debug("new_coordinates: %s", new_coordinates)

            self.contours.append(coordinates)
            self.bounds.append(rect)

            mask = cv2.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=cv2.LINE_8)

            mask = mask == 255
            self.mask.append(mask)
            logging.debug("mask: %s", self.mask)

        statuses = [False] * len(coordinates_data)
        times = [None] * len(coordinates_data)

        while capture.isOpened():
            statuses_aux = False
            result, frame = capture.read()
            if frame is None:
                break

            if not result:
                raise CaptureReadError("Error reading video capture on frame %s" % str(frame))

            blurred = cv2.GaussianBlur(frame.copy(), (5, 5), 3)
            grayed = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
            new_frame = frame.copy()
            logging.debug("new_frame: %s", new_frame)

            position_in_seconds = capture.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

            for index, c in enumerate(coordinates_data):
                status = self.apply(grayed, index, c)

                if times[index] is not None and self.same_status(statuses, index, status):
                    times[index] = None
                    continue

                if times[index] is not None and self.status_changed(statuses, index, status):
                    if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY:
                        statuses[index] = status
                        statuses_aux = True
                        times[index] = None
                    continue

                if times[index] is None and self.status_changed(statuses, index, status):
                    times[index] = position_in_seconds

            for index, p in enumerate(coordinates_data):
                coordinates = self._coordinates(p)

                color = COLOR_GREEN if statuses[index] else COLOR_BLUE
                draw_contours(new_frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)

            cv2.imshow(str(self.video), new_frame)
            k = cv2.waitKey(1)
            if k == ord("q"):
                break

            #calculate free and occupied and send msg
            if statuses_aux:
                free = len([x for x in statuses if x])
                occupied = len(statuses) - free
                message = json.dumps({
                        "timestamp": datetime.now().isoformat(),
                        "fields": {
                            "free_places" : free,
                            "full_places" : occupied
                        }
                    })
                print(message)
                #self.publisher.send(message)

        capture.release()
        cv2.destroyAllWindows()
        #self.publisher.stop_connection()

    def apply(self, grayed, index, p):
        coordinates = self._coordinates(p)
        logging.debug("points: %s", coordinates)

        rect = self.bounds[index]
        logging.debug("rect: %s", rect)

        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = cv2.Laplacian(roi_gray, cv2.CV_64F)
        logging.debug("laplacian: %s", laplacian)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        status = np.mean(np.abs(laplacian * self.mask[index])) < MotionDetector.LAPLACIAN
        logging.debug("status: %s", status)

        return status

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]


class CaptureReadError(Exception):
    pass
