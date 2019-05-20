from .ImagePreProcessorBase import *
import numpy as np
import cv2

class ImagePreProcessorGammaCorrection(ImagePreProcessorBase):

    def __init__(self, settings):
        self.gamma = settings['gamma']
        return

    def preProcessImage(self, image):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / self.gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)