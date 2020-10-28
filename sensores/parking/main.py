import argparse
import yaml

from coordinates_generator import CoordinatesGenerator
from motion_detector import MotionDetector
from colors import *
import logging


def main():
    #logging.basicConfig(level=logging.INFO)

    # image file to generate coordinates on
    image_file = 'images/parking3.png'

    # data file to be used with OpenCV
    data_file = 'data/park3.yml'

    # video file to detect motion on
    video_file = 'videos/parking3.mp4'
    #video_file = '0'

    # starting frame on the video
    start_frame = 0

    # do .yml file: false to using an existing
    do_file = True

    if do_file:
        with open(data_file, "w+") as points:
            # draw segments and write file .yml with their info
            generator = CoordinatesGenerator(image_file, points, COLOR_RED)
            generator.generate()

    with open(data_file, "r") as data:
        # info from .yml file writen before
        points = yaml.load(data, Loader=yaml.FullLoader)

        # segment monitoring
        detector = MotionDetector(video_file, points, int(start_frame))
        detector.detect_motion()

if __name__ == '__main__':
    main()
