

class ImagePreProcessorBase:
    def __init__(self, settings):
        print("Init Edge Detection Base")

    def preProcessImage(self, image):
        raise NotImplemented("preProcessImage from abstract ImagePreProcessingBase not implemented")