from .ImageSignDetectorBase import *
import cv2
import tensorflow as tf
from tensorflow import keras
from skimage.transform import resize
from keras.models import load_model

class ImageSignDetectionDnnMnist(ImageSignDetectorBase):

    def __init__(self, settings):
        self.modelPath = settings['path']
        print("Model not created, please fix before productive!")
        self.model = load_model(self.modelPath)

    def detectSign(self, image, regionRectangle, debugger = None):
        """"
        # Get sign as a fitting square
        imageRegion = self.getFittingImageRegion(image, regionRectangle)

        print(imageRegion.std())

        # Thresholding of image to get a binary image
        im_thresh = cv2.threshold(imageRegion, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Resize to 28*28 pixel since mnist takes only this size
        try:
            im_resize1 = cv2.resize(im_thresh, (28, 28))
        except:
            print("Error on resizing")
            print(regionRectangle)
            cv2.imshow("Error image:", image)
            cv2.imshow("Error region:", im_thresh)
            cv2.waitKey()

        # Determine which color the digit was and correct if needed since mnist needs white digits
        digitColor = self.determineDigitColor(im_resize1)
        if digitColor == self.BLACK_DIGIT:
            im_resize1 = ~im_resize1
        """

        # Resize again to fit the CNN
        im_resize2 = resize(image, (28, 28), mode='constant')
        im_final = im_resize2.reshape(1, 28, 28, 1)

        cv2.imshow("found image", im_resize2)

        # Predict image
        print("Before prediction")
        #ans = self.model.predict(im_final)
        print("After prediction")

        # Read predictions from CNN
        prediction = 1#= ans[0].tolist().index(max(ans[0].tolist()))
        probability = 10#= ans[0].tolist()[prediction] * 100

        print("DNN: Digit detected. Digit was %d with a probability of %.2f" % (prediction, probability))

        return [prediction, probability]