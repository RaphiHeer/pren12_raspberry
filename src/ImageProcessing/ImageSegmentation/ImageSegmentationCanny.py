from .ImageSegmentationBase import *
import cv2

class ImageSegmentationCanny(ImageSegmentationBase):

    def __init__(self, settings):
        self.threshold1 = settings['threshold1']
        self.threshold2 = settings['threshold2']

    def segmentImage(self, image):
        return cv2.Canny(image, self.threshold1, self.threshold2)