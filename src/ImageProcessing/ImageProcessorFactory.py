from .ImageProcessor import *
from .ImagePreProcessing.ImagePreProcessorBase import *
from .ImagePreProcessing.ImagePreProcessorNone import *
from .ImageEdgeDetection.ImageEdgeDetectorBase import *
from .ImageEdgeDetection.ImageEdgeDetectorCanny import *
from .ImageFeatureDetection.ImageFeatureDetectorBase import *
from .ImageFeatureDetection.ImageFeatureDetectorFindContours import *
from .ImageSignDetection.ImageSignDetectorBase import *
from .ImageSignDetection.ImageSignDetectorDnnMnist import *

class ImageProcessorFactory:
    def __init__(self):
        return

    def createImageProcessors(self, settings):
        imageProcessors = []

        for imageProcessorSetting in settings:

            imagePreProcessor = self.createImagePreProcessor(imageProcessorSetting['preProcessing'])
            imageEdgeDetector = self.createImageEdgeDetector(imageProcessorSetting['edgeDetection'])
            imageFeatureDetector = self.createImageFeatureDetector(imageProcessorSetting['featureDetection'])
            imageSignDetector = self.createImageSignDetector(imageProcessorSetting['signDetection'])

            imageProcessor = ImageProcessor(imagePreProcessor, imageEdgeDetector, imageFeatureDetector, imageSignDetector)
            imageProcessors.append(imageProcessor)

        return imageProcessors

    def createImagePreProcessor(self, settings):
        imagePreProcessor = ImagePreProcessorNone(settings)
        if settings['type'] == 'none':
            imagePreProcessor = ImagePreProcessorNone(settings)

        return imagePreProcessor

    def createImageEdgeDetector(self, settings):
        if settings['type'] == 'canny':
            imageEdgeDetector = ImageEdgeDetectorCanny(settings)

        return imageEdgeDetector

    def createImageFeatureDetector(self, settings):
        if settings['type'] == 'findContours':
            imageFeatureDetector = ImageFeatureDetectionFindContours(settings)

        return imageFeatureDetector

    def createImageSignDetector(self, settings):
        if settings['type'] == 'DnnMnist':
            imageSignDetector = ImageSignDetectionDnnMnist(settings)

        return imageSignDetector