

class ImageSignDetectorBase:
    def __init__(self, settings):
        print("Init Edge Detection Base")

    def detectSign(self, image):
        raise NotImplemented("detectSign from abstract ImageSignDetectionBase not implemented")

    #def determineDigitColor(self):
