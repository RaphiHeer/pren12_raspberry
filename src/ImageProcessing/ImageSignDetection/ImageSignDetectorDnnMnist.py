from .ImageSignDetectorBase import *
import cv2
import tensorflow as tf
from tensorflow import keras
from skimage.transform import resize
from keras.models import load_model

class ImageSignDetectionDnnMnist(ImageSignDetectorBase):

    def __init__(self, settings):
        self.modelPath = settings['path']
        self.model = load_model(self.modelPath)

    def detectSign(self, image, debugger = None):
        im_cutted = cv2.threshold(image.copy(), 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        im_resize1 = cv2.resize(im_cutted, (28, 28))

        digitColor = self.determineDigitColor(im_resize1)
        if digitColor == self.BLACK_DIGIT:
            im_resize1 = cv2.invert(im_resize1)

        im_resize2 = resize(im_resize1, (28, 28), mode='constant')
        #cv2.imshow("Contour for MNIST", im_resize2)
        #cv2.waitKey()
        im_final = im_resize2.reshape(1, 28, 28, 1)

        ans = self.model.predict(im_final)

        prediction = ans[0].tolist().index(max(ans[0].tolist()))
        probability = ans[0].tolist()[prediction] * 100

        print("%s digit detected. Digit was %d with a probability of %.2f" % (digitColor, prediction, probability))

        return [prediction, probability]