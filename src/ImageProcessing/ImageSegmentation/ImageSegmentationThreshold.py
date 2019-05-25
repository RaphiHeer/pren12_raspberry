from .ImageSegmentationBase import *
import cv2

class ImageSegmentationThreshold(ImageSegmentationBase):

    def __init__(self, settings):
        self.threshold1 = settings['threshold1']
        self.threshold2 = settings['threshold2']

        if settings["threshMode"] == "otsu":
            self.THRESH_MODE = cv2.THRESH_OTSU
        elif settings["threshMode"] == "binOtsu":
            self.THRESH_MODE = cv2.THRESH_OTSU + cv2.THRESH_BINARY
        else:
            self.THRESH_MODE = cv2.THRESH_BINARY

    def segmentImage(self, image):
        thresh = cv2.threshold(image, self.threshold1, self.threshold2, self.THRESH_MODE)[1]
        return thresh