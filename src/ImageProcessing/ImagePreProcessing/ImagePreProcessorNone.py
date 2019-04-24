from .ImagePreProcessorBase import *

class ImagePreProcessorNone(ImagePreProcessorBase):

    def __init__(self, settings):
        return

    def preProcessImage(self, image):
        return image