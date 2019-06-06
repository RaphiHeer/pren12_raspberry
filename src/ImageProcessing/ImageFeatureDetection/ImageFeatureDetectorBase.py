import cv2

class ImageFeatureDetectorBase:
    BLACK_DIGIT = 'black'
    WHITE_DIGIT = 'white'
    PIXELS_IN_IMAGE = 28 * 28

    def __init__(self, settings):
        print("Init Feature Detection Base")

    def detectFeatures(self, originalImage, segmentedImage, drawImage = None):
        raise NotImplemented("detectFeatures from abstract ImageFeatureDetectionBase not implemented")

    def readImageRegionAsSquareFromImage(self, image, regionRectangle):
        # Get sign as a fitting square
        imageRegion = self.getFittingImageRegion(image, regionRectangle)

        print(imageRegion.std())

        # Thresholding of image to get a binary image
        thresholdedImage = cv2.threshold(imageRegion, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Resize to 28*28 pixel since mnist takes only this size
        try:
            resizedImage = cv2.resize(thresholdedImage, (28, 28))

        except:
            print("Error on resizing")
            print(regionRectangle)
            cv2.imshow("Error image:", image)
            cv2.imshow("Error region:", thresholdedImage)
            cv2.waitKey()
            return

        # Determine which color the digit was and correct if needed since mnist needs white digits
        digitColor = self.determineDigitColor(resizedImage)
        if digitColor == self.BLACK_DIGIT:
            im_resize1 = ~resizedImage

        return resizedImage

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