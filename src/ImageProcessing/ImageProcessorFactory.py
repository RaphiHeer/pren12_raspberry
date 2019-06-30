from .ImageProcessor import *
from .ImagePreProcessing.ImagePreProcessorBase import *
from .ImagePreProcessing.ImagePreProcessorNone import *
from .ImagePreProcessing.ImagePreProcessorGammaCorrection import *
from .ImageSegmentation.ImageSegmentationBase import *
from .ImageSegmentation.ImageSegmentationCanny import *
from .ImageSegmentation.ImageSegmentationThreshold import *
from .ImageFeatureDetection.ImageFeatureDetectorBase import *
from .ImageFeatureDetection.ImageFeatureDetectorFindContours import *
from .ImageSignDetection.ImageSignDetectorBase import *
from .ImageSignDetection.ImageSignDetectorDnnMnist import *
from .ImageSignDetection.ImageSignDetectorTemplateMatching import *

def createImageProcessorList(settings, debugger):
    imageProcessors = []

    for imageProcessorSetting in settings:

        imageProcessor = createImageProcessor(imageProcessorSetting, debugger)

        imageProcessors.append(imageProcessor)

    return imageProcessors

def createImageProcessor(imageProcessorSetting, debugger, logger = None):
    imagePreProcessor = createImagePreProcessor(imageProcessorSetting['preProcessing'])
    imageSegmentation = createImageSegmentation(imageProcessorSetting['segmentation'])
    imageFeatureDetector = createImageFeatureDetector(imageProcessorSetting['featureDetection'])
    imageSignDetector = createImageSignDetector(imageProcessorSetting['signDetection'])

    imageProcessor = ImageProcessor(imagePreProcessor, imageSegmentation, imageFeatureDetector, imageSignDetector, debugger, logger=logger)
    return imageProcessor

def createImagePreProcessor(settings):
    imagePreProcessor = ImagePreProcessorNone(settings)
    if settings['type'] == 'none':
        imagePreProcessor = ImagePreProcessorNone(settings)
    elif settings['type'] == 'gammaCorrection':
        imagePreProcessor = ImagePreProcessorGammaCorrection(settings)

    return imagePreProcessor

def createImageSegmentation(settings):
    if settings['type'] == 'canny':
        imageSegmentation = ImageSegmentationCanny(settings)
    elif settings['type'] == 'threshold':
        imageSegmentation = ImageSegmentationThreshold(settings)

    return imageSegmentation

def createImageFeatureDetector(settings):
    if settings['type'] == 'findContours':
        imageFeatureDetector = ImageFeatureDetectionFindContours(settings)

    return imageFeatureDetector

def createImageSignDetector(settings):
    if settings['type'] == 'DnnMnist':
        imageSignDetector = ImageSignDetectorDnnMnist(settings)
    else: # settings['type'] == "TM":
        imageSignDetector = ImageSignDetectorTemplateMatching(settings)

    return imageSignDetector