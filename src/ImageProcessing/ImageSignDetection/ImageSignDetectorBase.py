import cv2

class ImageSignDetectorBase:
    BLACK_DIGIT = 'black'
    WHITE_DIGIT = 'white'
    PIXELS_IN_IMAGE = 28 * 28

    def __init__(self, settings):
        print("Init Edge Detection Base")

    def detectSign(self, image, regionRectangle, debugger = None):
        raise NotImplemented("detectSign from abstract ImageSignDetectionBase not implemented")

    def determineDigitColor(self, image, isThresholded = True):
        whitePixelCount = cv2.countNonZero(image)

        # If there are more white pixels, we assume the background is white
        # therefore, the digit must be black #logic #mathPro
        if whitePixelCount > self.PIXELS_IN_IMAGE / 2:
            return self.BLACK_DIGIT
        else:
            return self.WHITE_DIGIT

    def getFittingImageRegion(self, image, regionRectangle):

        x, y, w, h = regionRectangle

        # Calculate new Height
        newHeight = int(h * 1.4)
        heightDiffPerSite = int((newHeight - h) / 2)
        leftY = y - heightDiffPerSite

        # Correct width to heigth ratio to get a square
        diffHW = h - w
        newWidth = w + diffHW
        addProSite = diffHW / 2

        leftX = int(x - addProSite)
        rightX = int(x + w + addProSite)

        if leftX < 0:
            leftX = 0
        if leftY < 0:
            leftY = 0

        return image[leftY:(leftY+newHeight),leftX:rightX].copy()