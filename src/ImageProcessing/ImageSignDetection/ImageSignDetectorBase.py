import cv2

class ImageSignDetectorBase:
    BLACK_DIGIT = 'black'
    WHITE_DIGIT = 'white'
    PIXELS_IN_IMAGE = 28 * 28

    def __init__(self, settings):
        print("Init Edge Detection Base")

    def detectSign(self, image):
        raise NotImplemented("detectSign from abstract ImageSignDetectionBase not implemented")

    def determineDigitColor(self, image, isThresholded = True):
        whitePixelCount = cv2.countNonZero(image)

        # If there are more white pixels, we assume the background is white
        # therefore, the digit must be black #logic #mathPro
        if whitePixelCount > self.PIXELS_IN_IMAGE:
            return self.BLACK_DIGIT
        else:
            return self.WHITE_DIGIT
