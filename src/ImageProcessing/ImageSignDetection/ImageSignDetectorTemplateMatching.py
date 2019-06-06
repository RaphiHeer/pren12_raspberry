from .ImageSignDetectorBase import *
import cv2

class ImageSignDetectionDnnMnist(ImageSignDetectorBase):

    def __init__(self, settings):

        folder = "template/"
        self.templateList = []

        for i in range(1, 9):
            filename = "template_%d.png" % i
            templateImage = cv2.imread(filename)
            self.templateList[i] = templateImage

    def detectSign(self, image, regionRectangle, debugger=None):

        scores = []

        for templateImage in self.templateList:
            res = cv2.matchTemplate(image, templateImage, cv2.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        prediction = 1
        probability = 10
        return (prediction, probability)