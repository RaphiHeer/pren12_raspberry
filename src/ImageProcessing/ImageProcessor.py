from .ImageDebugger import *
from .ImagePreProcessing.ImagePreProcessorBase import *
from .ImageEdgeDetection.ImageEdgeDetectorBase import *
from .ImageFeatureDetection.ImageFeatureDetectorBase import *
from .ImageSignDetection.ImageSignDetectorBase import *
import cv2

class ImageProcessor:

    def __init__(self,
                 preProcessor: ImagePreProcessorBase,
                 edgeDetector: ImageEdgeDetectorBase,
                 featureDetector: ImageFeatureDetectorBase,
                 signDetector: ImageSignDetectorBase):
        self.preProcessor = preProcessor
        self.edgeDetector = edgeDetector
        self.featureDetector = featureDetector
        self.signDetector = signDetector

        self.debugger = ImageDebugger(True, False)

    def setDebugger(self, debugger):
        self.debugger = debugger

    def processVideoStream(self, videoStream, boardConnector):

        while True:
            image = videoStream.read()
            cv2.imshow("Test", image)
            print("Read next image")

            imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.debugger.debugImage("From Camera", image)

            imagePreProcessed = self.preProcessor.preProcessImage(imageGray)
            self.debugger.debugImage("After PreProcessing", imagePreProcessed)

            imageEdge = self.edgeDetector.detectEdges(imagePreProcessed)
            self.debugger.debugImage("After edgeDetection", imageEdge)

            regionsOfInterest = self.featureDetector.detectFeatures(imageEdge)
            self.debugger.drawContoursOnImage(image, regionsOfInterest, (0,255,0))

            for region in regionsOfInterest:
                x, y, w, h = region
                regionImage = imageGray[y-5:(y+h+5),x-5:(x+w+5)].copy()
                prediction, propability = self.signDetector.detectSign(regionImage)
                print("Prediction: %d\tPropability%.2f" % (prediction, propability))
                self.debugger.writePreditcionOnImage(image, region, prediction, propability, (0,255,0))

            self.debugger.debugImage("ROIs", image)