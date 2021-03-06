import cv2 
import numpy as np

from colors import COLOR_WHITE
from drawing_utils import draw_contours


class CoordinatesGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, output, color):
        self.output = output
        self.caption = image
        self.color = color

        self.image = cv2.imread(image).copy()
        self.click_count = 0
        self.ids = 0
        self.coordinates = []

        cv2.namedWindow(self.caption, cv2.WINDOW_GUI_EXPANDED)
        cv2.setMouseCallback(self.caption, self.mouse_callback)

    def generate(self):
        while True:
            cv2.imshow(self.caption, self.image)
            key = cv2.waitKey(0)

            if key == CoordinatesGenerator.KEY_RESET:
                self.image = self.image.copy()
            elif key == CoordinatesGenerator.KEY_QUIT:
                break
        cv2.destroyWindow(self.caption)

    # build the .yml file and draw the segments to be monitored
    def mouse_callback(self, event, x, y, flags, params):

        if event == cv2.EVENT_LBUTTONDOWN:
            #first point
            self.coordinates.append((x, y))
            self.click_count += 1

            #done
            if self.click_count >= 4:
                self.handle_done()

            #while
            elif self.click_count > 1:
                self.handle_click_progress()

        cv2.imshow(self.caption, self.image)

    def handle_click_progress(self):
        cv2.line(self.image, self.coordinates[-2], self.coordinates[-1], (255, 0, 0), 1)

    # write info points that delimit the segment into file
    def handle_done(self):
        cv2.line(self.image,
                     self.coordinates[2],
                     self.coordinates[3],
                     self.color,
                     1)
        cv2.line(self.image,
                     self.coordinates[3],
                     self.coordinates[0],
                     self.color,
                     1)

        coordinates = np.array(self.coordinates)

        # write info points that delimit the segment into file
        self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                          "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                          "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                          "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                          "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")
        
        #draw segment
        draw_contours(self.image, coordinates, str(self.ids + 1), COLOR_WHITE)

        #clean vars
        self.click_count = 0
        for i in range(0, 4):
            self.coordinates.pop()

        self.ids += 1
