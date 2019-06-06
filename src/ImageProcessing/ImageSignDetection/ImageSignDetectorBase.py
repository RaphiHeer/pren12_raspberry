import cv2

class ImageSignDetectorBase:

    def __init__(self, settings):
        print("Init Edge Detection Base")

    def detectSign(self, image, regionRectangle, debugger = None):
        raise NotImplemented("detectSign from abstract ImageSignDetectionBase not implemented")

