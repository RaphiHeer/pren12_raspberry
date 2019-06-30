from .ImageSignDetectorBase import *
import cv2
""""
from skimage.transform import resize
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
"""
from skimage.transform import resize
import time
import uuid

class ImageSignDetectorDnnMnist(ImageSignDetectorBase):

    def __init__(self, settings):
        import tensorflow as tf
        from tensorflow import keras
        from keras.models import load_model
        self.modelPath = settings['path']
        self.savePredictions = settings['savePredictions']

        if self.savePredictions:
            self.savePredictionsPath = settings['savePredictionsPath']

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


        # Predict image
        print("Before prediction")
        ans = self.model.predict(im_final)
        pred = ans
        ans = ans[0].tolist()
        print("After prediction")
        print(pred.argmax(axis=1)[0])

        # Read predictions from CNN
        prediction = ans.index(max(ans))
        probability = ans[prediction] * 100

        print("\n\nPrediction:")
        for i in range(0, 10):
            print("Prop of %d is %.2f" % (i, ans[i]))

        for i in cv2.img_hash.averageHash(image):
            print(i)
        if self.savePredictions and probability > 80:
            cv2.imwrite(self.savePredictionsPath + ("/%d/" % prediction) + str(uuid.uuid4()) + ".png", image)

        print("DNN: Digit detected. Digit was %d with a probability of %.2f" % (prediction, probability))

        return [prediction, probability]