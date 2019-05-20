from .ImageFeatureDetectorBase import *
import cv2

class ImageFeatureDetectionFindContours(ImageFeatureDetectorBase):

    def __init__(self, settings):
        #if settings['mode'] == 'RETR_EXTERNAL':
        self.mode = cv2.RETR_EXTERNAL

        #if settings['method'] == 'CHAIN_APPROX_SIMPLE':
        self.method = cv2.CHAIN_APPROX_SIMPLE

        self.infoStopDividerIncline = 3
        self.infoStopDividerOffset = 200

        return

    def detectFeatures(self, image, debugDrawImage = None):
        RegionsOfInterest = []

        cnts = cv2.findContours(image.copy(), self.mode, self.method)[0]
        cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        for c in cnts:
            rect = cv2.boundingRect(c)
            print(rect)
            x, y, w, h = rect

            if w > h:
                self.drawContour(debugDrawImage, c, rect, (0, 0, 255))
                continue

            heigthWidthRatio = h / w
            if heigthWidthRatio < 1.5:
                self.drawContour(debugDrawImage, c, rect, (0, 100, 240))
                continue

            if h < 20:
                self.drawContour(debugDrawImage, c, rect, (0, 120, 200))
                continue

            if h > 100:
                self.drawContour(debugDrawImage, c, rect, (0, 150, 180))
                continue

            if x < 10 | x > (image.shape[1] / 2):
                self.drawContour(debugDrawImage, c, rect, (0, 150, 180))
                continue


            region = {}
            region["rectangle"] = rect
            region["isInfoSignal"] = self.isInfoSignal(rect)

            if region["isInfoSignal"]:
                self.drawContour(debugDrawImage, c, rect, (0, 255, 0))
            else:
                self.drawContour(debugDrawImage, c, rect, (0, 210, 0))

            RegionsOfInterest.append(region)

        return RegionsOfInterest

    def isInfoSignal(self, rect):
        x, y, w, h = rect
        maxY = self.infoStopDividerIncline * x + self.infoStopDividerOffset

        if maxY > y:
            return True
        return False

    def drawContour(self, debugDrawImage, c, rect, color):
        if debugDrawImage is not None:
            x, y, w, h = rect
            cv2.drawContours(debugDrawImage, [c], -1, (240, 0, 159), 2)
            cv2.rectangle(debugDrawImage, (x, y), (x + w, y + h), color, 2)