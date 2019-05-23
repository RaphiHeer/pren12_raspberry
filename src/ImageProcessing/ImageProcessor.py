from .ImageDebugger import *
from .ImagePreProcessing.ImagePreProcessorBase import *
from .ImageSegmentation.ImageSegmentationBase import *
from .ImageFeatureDetection.ImageFeatureDetectorBase import *
from .ImageSignDetection.ImageSignDetectorBase import *
import cv2

class ImageProcessor:

    def __init__(self,
                 preProcessor: ImagePreProcessorBase,
                 segmentation: ImageSegmentationBase,
                 featureDetector: ImageFeatureDetectorBase,
                 signDetector: ImageSignDetectorBase,
                 debugger: ImageDebugger):
        self.preProcessor = preProcessor
        self.segmentation = segmentation
        self.featureDetector = featureDetector
        self.signDetector = signDetector

        self.debugger = debugger

    def setDebugger(self, debugger):
        self.debugger = debugger

    def processVideoStream(self, videoStream, boardConnector):
        while True:
            print("Read next image")
            image = videoStream.read()
            cv2.imshow("Test", image)
            cv2.waitKey()

            imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.debugger.debugImage("From Camera", image)

            imagePreProcessed = self.preProcessor.preProcessImage(imageGray)
            self.debugger.debugImage("After PreProcessing", imagePreProcessed)

            imageEdge = self.segmentation.segmentImage(imagePreProcessed)
            self.debugger.debugImage("After edgeDetection", imageEdge)

            regionsOfInterest = self.featureDetector.detectFeatures(imageEdge, image)
            self.debugger.debugImage("Contours", image)
            #self.debugger.drawContoursOnImage(image, regionsOfInterest, (0,255,0))

            for region in regionsOfInterest:
                x, y, w, h = region["rectangle"]

                if x < 5:
                    x = 5
                if y < 5:
                    y = 5


                #regionImage = imagePreProcessed[y-5:(y+h+5),x-5:(x+w+5)].copy()
                #prediction, propability = self.signDetector.detectSign(regionImage)
                #print("Prediction: %d\tPropability%.2f" % (prediction, propability))
                #self.debugger.writePreditcionOnImage(image, region["rectangle"], prediction, propability, (0,255,0))

            self.debugger.debugImage("ROIs", image)