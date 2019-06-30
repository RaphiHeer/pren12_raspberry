from .ImageSignDetectorBase import *
import cv2
import uuid

class ImageSignDetectorTemplateMatching(ImageSignDetectorBase):


    def __init__(self, settings):

        self.scoreThresholds = {}
        self.scoreThresholds[1] = 0.7
        self.scoreThresholds[2] = 0.75
        self.scoreThresholds[3] = 0.75
        self.scoreThresholds[4] = 0.85
        self.scoreThresholds[5] = 0.75
        self.scoreThresholds[6] = 0.75
        self.scoreThresholds[7] = 0.75
        self.scoreThresholds[8] = 0.75
        self.scoreThresholds[9] = 0.75


        folder = "templates/"
        self.whiteTemplateList = {}
        self.blackTemplateList = {}

        for i in range(1, 10):
            whiteDigitFilename = folder + ("white_%d.png" % i)
            whiteDigitImage = cv2.imread(whiteDigitFilename)
            self.whiteTemplateList[i] = cv2.cvtColor(whiteDigitImage, cv2.COLOR_BGR2GRAY)


            blackDigitFilename = folder + ("black_%d.png" % i)
            blackDigitImage = cv2.imread(blackDigitFilename)
            self.blackTemplateList[i] = cv2.cvtColor(blackDigitImage, cv2.COLOR_BGR2GRAY)

    def calculateScoreshold(self, scoredDigit, scoreList):
        return


    def detectSign(self, image, digitColor, debugger=None):

        scoreList = {}

        maxScore = 0
        scoreDigit = 0

        if digitColor == "white":
            templateList = self.whiteTemplateList
        else:
            templateList = self.blackTemplateList

        for i in range(1, 10):
            res = cv2.matchTemplate(image, templateList[i], cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            scoreList[i] = max_val

            if max_val > maxScore:
                maxScore = max_val
                scoreDigit = i


        if scoreDigit != 0 and maxScore > self.scoreThresholds[scoreDigit]:
            prediction = scoreDigit
            probability = maxScore
            print("TM: Digit was %d with a probability of %.2f" % (prediction, probability))

        else:
            prediction = -1
            probability = maxScore

        #cv2.imwrite("tm/" + str(uuid.uuid4()) + ".png", image)
        #print("Saved image")

        return (prediction, probability)