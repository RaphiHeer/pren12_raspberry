from .ImageSignDetectorBase import *
import cv2
import time

class ImageSignDetectorSaveForTraining:
    def __init__(self, settings):
        print("Init Edge Detection Base")
        self.path = "../../ml/"

    def detectSign(self, image, regionRectangle, debugger = None):
        # Get sign as a fitting square
        imageRegion = self.getFittingImageRegion(image, regionRectangle)

        # Thresholding of image to get a binary image
        im_thresh = cv2.threshold(imageRegion, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Resize to 28*28 pixel since mnist takes only this size
        try:
            im_resize1 = cv2.resize(im_thresh, (28, 28))
        except:
            print("Error on resizing")
            print(regionRectangle)
            #cv2.imshow("Error image:", image)
            #cv2.imshow("Error region:", im_thresh)
            #cv2.waitKey()

        # Determine which color the digit was and correct if needed since mnist needs white digits
        digitColor = self.determineDigitColor(im_resize1)
        if digitColor == self.BLACK_DIGIT:
            im_resize1 = ~im_resize1

        # Resize again to fit the CNN
        im_resize2 = resize(im_resize1, (28, 28), mode='constant')
        im_final = im_resize2.reshape(1, 28, 28, 1)

        filename = self.path + str(time.time()) + ".png"

        cv2.imwrite(filename, im_final)
