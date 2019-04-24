from .ImageEdgeDetectorBase import *
import cv2

class ImageEdgeDetectorCanny(ImageEdgeDetectorBase):

    def __init__(self, settings):
        self.threshold1 = settings['threshold1']
        self.threshold2 = settings['threshold2']

    def detectEdges(self, image):
        return cv2.Canny(image, self.threshold1, self.threshold2)