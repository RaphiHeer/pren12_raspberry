from .ImageSignDetectorBase import *
import cv2

class ImageSignDetectorTemplateMatching(ImageSignDetectorBase):

    scoreThreshold = 0.8

    def __init__(self, settings):

        folder = "templates/"
        self.templateList = {}

        for i in range(1, 10):
            filename = folder + ("template_%d.png" % i)
            templateImage = cv2.imread(filename)
            self.templateList[i] = cv2.cvtColor(templateImage, cv2.COLOR_BGR2GRAY)

    def detectSign(self, image, regionRectangle, debugger=None):

        scores = []

        maxScore = 0
        scoreDigit = 0

        for i in range(1, 10):
            res = cv2.matchTemplate(image, self.templateList[i], cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val > maxScore:
                maxScore = max_val
                scoreDigit = i


        if scoreDigit == 0 or maxScore < self.scoreThreshold:
            prediction = -1
            probability = maxScore

        else:
            prediction = scoreDigit
            probability = maxScore
        return (prediction, probability)