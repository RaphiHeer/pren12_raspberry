from .ImageFeatureDetectorBase import *
import cv2

class ImageFeatureDetectionFindContours(ImageFeatureDetectorBase):

    def __init__(self, settings):
        if settings['mode'] == 'RETR_EXTERNAL':
            self.mode = cv2.RETR_EXTERNAL

        if settings['method'] == 'CHAIN_APPROX_SIMPLE':
            self.method = cv2.CHAIN_APPROX_SIMPLE

        return

    def detectFeatures(self, image):
        RegionsOfInterest = []

        cnts = cv2.findContours(image.copy(), self.mode, self.method)[0]

        for c in cnts:
            rect = cv2.boundingRect(c)
            x, y, w, h = rect

            if w < 50 or h < 50:
                continue

            heigthWidthRatio = h / w
            if (heigthWidthRatio < 0.5) | (heigthWidthRatio > 1.5):
                continue

            RegionsOfInterest.append(rect)

        return RegionsOfInterest