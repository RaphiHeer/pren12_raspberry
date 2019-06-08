from .ImageDebugger import *
from .ImagePreProcessing.ImagePreProcessorBase import *
from .ImageSegmentation.ImageSegmentationBase import *
from .ImageFeatureDetection.ImageFeatureDetectorBase import *
from .ImageSignDetection.ImageSignDetectorBase import *
import time
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
            beforeRead = time.time()
            image = videoStream.read()
            afterRead = time.time()
            print("Time too read frame: %.3f" % (afterRead - beforeRead))

            if image is None:
                continue


            imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.debugger.debugImage("From Camera", image)

            imagePreProcessed = self.preProcessor.preProcessImage(imageGray)
            self.debugger.debugImage("After PreProcessing", imagePreProcessed)

            imageEdge = self.segmentation.segmentImage(imagePreProcessed)
            self.debugger.debugImage("After edgeDetection", imageEdge)

            regionsOfInterest = self.featureDetector.detectFeatures(imagePreProcessed, imageEdge, image)
            self.debugger.debugImage("Contours", image)

            mostLeftXpos = 10000
            mostLeftPrediction = None

            for region in regionsOfInterest:

                xPos = region["rectangle"][0]
                print("X Position: %d" % xPos)

                # Send image region to sign detector
                prediction, probability = self.signDetector.detectSign(region['image'], region["rectangle"], self.debugger)

                # Depending on the propability, send image to arduino or not
                if prediction != -1 and xPos < mostLeftXpos:
                    mostLeftPrediction = {"prediction": prediction, "probability": probability,
                                          "isInfoSignal": region["isInfoSignal"], "rectangle": region["rectangle"]}
                else:
                    self.debugger.writePreditcionOnImage(image, region["rectangle"], prediction, probability, (0, 0, 255))

            if mostLeftPrediction is not None:
                    print("Most left signal with digit: %d and a prob of %.2f is a%s" %
                          (mostLeftPrediction["prediction"], mostLeftPrediction["probability"],
                           ("n info sign" if mostLeftPrediction["isInfoSignal"] else " stop sign")))

                    boardConnector.numberDetected(mostLeftPrediction["prediction"], mostLeftPrediction["isInfoSignal"])

                    self.debugger.writePreditcionOnImage(image, mostLeftPrediction["rectangle"], mostLeftPrediction["prediction"], mostLeftPrediction["probability"], (0, 255, 0))
            self.debugger.debugImage("ROIs", image)
            self.debugger.imageProcessed(image)
            image = None

