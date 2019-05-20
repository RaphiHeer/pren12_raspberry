from .ImageProcessor import *
from .ImagePreProcessing.ImagePreProcessorBase import *
from .ImagePreProcessing.ImagePreProcessorNone import *
from .ImagePreProcessing.ImagePreProcessorGammaCorrection import *
from .ImageSegmentation.ImageSegmentationBase import *
from .ImageSegmentation.ImageSegmentationCanny import *
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
            imageSegmentation = self.createImageSegmentation(imageProcessorSetting['segmentation'])
            imageFeatureDetector = self.createImageFeatureDetector(imageProcessorSetting['featureDetection'])
            imageSignDetector = self.createImageSignDetector(imageProcessorSetting['signDetection'])

            imageProcessor = ImageProcessor(imagePreProcessor, imageSegmentation, imageFeatureDetector, imageSignDetector)
            imageProcessors.append(imageProcessor)

        return imageProcessors

    def createImagePreProcessor(self, settings):
        imagePreProcessor = ImagePreProcessorNone(settings)
        if settings['type'] == 'none':
            imagePreProcessor = ImagePreProcessorNone(settings)
        elif settings['type'] == 'gammaCorrection':
            imagePreProcessor = ImagePreProcessorGammaCorrection(settings)

        return imagePreProcessor

    def createImageSegmentation(self, settings):
        if settings['type'] == 'canny':
            imageSegmentation = ImageSegmentationCanny(settings)

        return imageSegmentation

    def createImageFeatureDetector(self, settings):
        if settings['type'] == 'findContours':
            imageFeatureDetector = ImageFeatureDetectionFindContours(settings)

        return imageFeatureDetector

    def createImageSignDetector(self, settings):
        if settings['type'] == 'DnnMnist':
            imageSignDetector = ImageSignDetectionDnnMnist(settings)

        return imageSignDetector