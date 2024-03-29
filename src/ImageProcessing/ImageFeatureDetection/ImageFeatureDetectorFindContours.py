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

        self.m_info_top = 0.45  # y2 - y1 / 250
        self.c_info_top = -50

        self.m_info_bottom = 0.06  # 180 - 165 / 250 - 0
        self.c_info_bottom = 175

        self.m_stop_top = -0.52  # 190 - y1 / 250
        self.c_stop_top = 310

        self.m_stop_bottom = -1.0  # 200 - y1 / 250
        self.c_stop_bottom = 600

        self.m_heightRangeMax = 1.2

        self.max_x = 400

        self.paddingImage = cv2.cvtColor(cv2.imread("Ressources/padding_image.png"), cv2.COLOR_BGR2GRAY)

        return

    def detectFeatures(self, originalImage, segmentedImage, debugDrawImage = None):
        RegionsOfInterest = []

        if debugDrawImage is not None:
            cv2.line(debugDrawImage, (0, self.c_info_top),
                     (self.max_x, (int(self.m_info_top * self.max_x + self.c_info_top))), (255, 0, 0))
            cv2.line(debugDrawImage, (0, self.c_info_bottom),
                     (self.max_x, (int(self.m_info_bottom * self.max_x + self.c_info_bottom))), (255, 0, 0))
            cv2.line(debugDrawImage, (0, self.c_stop_top),
                     (self.max_x, (int(self.m_stop_top * self.max_x + self.c_stop_top))), (0, 0, 255))
            cv2.line(debugDrawImage, (0, self.c_stop_bottom),
                     (self.max_x, (int(self.m_stop_bottom * self.max_x + self.c_stop_bottom))), (0, 0, 255))

        cnts = cv2.findContours(segmentedImage.copy(), self.mode, self.method)[1]

        for c in cnts:
            rect = cv2.boundingRect(c)
            x, y, w, h = rect

            if x == 0:
                self.drawContour(debugDrawImage, c, rect, (0, 0, 255))
                continue

            if w > h:
                self.drawContour(debugDrawImage, c, rect, (0, 0, 255))
                continue

            heigthWidthRatio = h / w
            if 1.5 > heigthWidthRatio or heigthWidthRatio > 5:
                self.drawContour(debugDrawImage, c, rect, (0, 100, 240))
                continue

            if h < 15:
                self.drawContour(debugDrawImage, c, rect, (0, 120, 200))
                continue

            if h > 90:
                self.drawContour(debugDrawImage, c, rect, (0, 150, 180))
                continue

            if w > 55:
                self.drawContour(debugDrawImage, c, rect, (0, 120, 200))
                continue

            if w < 10:
                self.drawContour(debugDrawImage, c, rect, (0, 150, 180))
                continue

            if not self.isInSignRange(x, y):
                self.drawContour(debugDrawImage, c, rect, (50, 150, 180))
                continue

            if not self.isInCalculatedHeightRange(x, h):
                self.drawContour(debugDrawImage, c, rect, (50, 150, 180))
                continue

            region = {}
            region["rectangle"] = rect
            region["isInfoSignal"] = self.isInfoSignal(x, y)
            region["image"], region["digitColor"] = self.readImageRegionAsSquareFromImage(originalImage, rect)

            if debugDrawImage is not None:
                cv2.putText(debugDrawImage, ("H: %d W: %d\nX: %d Y: %d" % (h, w, x, y)), (x + 20, y + h + 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 1)
            if region["isInfoSignal"]:
                self.drawContour(debugDrawImage, c, rect, (0, 255, 0))
            else:
                self.drawContour(debugDrawImage, c, rect, (0, 210, 0))

            RegionsOfInterest.append(region)

        return RegionsOfInterest

    def isInfoSignal(self, x, y):

        return y < 240

    def isInSignRange(self, x, y):
        if x > self.max_x:
            return False
        if (self.m_info_top * x + self.c_info_top) > y:
            return False
        if (self.m_stop_bottom * x + self.c_stop_bottom) < y:
            return False
        return True

    def drawContour(self, debugDrawImage, c, rect, color):
        if debugDrawImage is not None:
            x, y, w, h = rect
            cv2.drawContours(debugDrawImage, [c], -1, (240, 0, 159), 2)
            cv2.rectangle(debugDrawImage, (x, y), (x + w, y + h), color, 2)

    def isInCalculatedHeightRange(self, x, h):
        # Not implemented yet...
        return True
