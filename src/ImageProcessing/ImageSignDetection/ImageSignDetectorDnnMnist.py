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

    def detectSign(self, image):

        im_cutted_and_inverted = cv2.threshold(image.copy(), 100, 255, cv2.THRESH_BINARY_INV)[1]
        im_resize1 = cv2.resize(im_cutted_and_inverted, (28, 28))
        im_resize2 = resize(im_resize1, (28, 28), mode='constant')
        im_final = im_resize2.reshape(1, 28, 28, 1)
        ans = self.model.predict(im_final)

        prediction = ans[0].tolist().index(max(ans[0].tolist()))
        propability = ans[0].tolist()[prediction] * 100

        return [prediction, propability]