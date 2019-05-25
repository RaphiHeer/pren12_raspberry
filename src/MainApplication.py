import argparse
from threading import Thread
from multiprocessing import Process
from ConfigReader import *
from ImageProcessing import *
from ImageProcessing.ImageDebugger import *
from ImageProcessing.ImageProcessorFactory import *
from ImageStream import *
from ImageStream.FileVideoStream import *
from ImageStream.PiVideoStream import *

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=False, help="path to input image")
args = vars(ap.parse_args())

if args["config"]:
    configPath = args["config"]
else:
    configPath = "Ressources/config.json"
print("Load config from: " + configPath)


def createVideoStream(videoConfig):
    if videoConfig["type"] == "picam":
        return PiVideoStream(videoConfig)
    elif videoConfig["type"] == "file":
        return FileVideoStream(videoConfig)


def createProcesses(imageProcessors, stream):
    processList = []
    for imageProcessor in imageProcessors:
        processList.append(Process(target=imageProcessor.processVideoStream, args=(stream, "")))

    return processList

def createThreads():
    threadList = []

    return threadList

def runMainApplication(configPath):
    config = ConfigReader(configPath)

    debugger = ImageDebugger(config.getApplicationSettings)

    stream = createVideoStream(config.getImageStreamSettings())
    stream = stream.start()

    factory = ImageProcessorFactory()

    imageProcessors = factory.createImageProcessors(config.imageProcessors, debugger)

    #processList = createProcesses(imageProcessors, stream)

    imageProcessors[0].processVideoStream(stream, "")
    #for process in processList:
    #    process.start()

if __name__ == '__main__':
    runMainApplication(configPath)

"""
#import CNN model weight
model= load_model('./model/mnist_trained_model.h5')
imageDebugger = ImageDebugger(True, False)

# imagePreprocessor = # ImagePreprocessor()
#featureExtractor = CannyContouring() # FeatureExtractor()
#numberPredictor = TensorFlowMnistPredictor() # NumberPredictor()

imageProcessor = ImageProcessor(config, model, imageDebugger)
imageProcessor.start_detecting("asdf", "1")

#imageProcessor1 = ImageProcessor(config, model, imageDebugger)
imageProcessor2 = ImageProcessor(config, model, imageDebugger)
imageProcessor3 = ImageProcessor(config, model, imageDebugger)
imageProcessor4 = ImageProcessor(config, model, imageDebugger)

#Thread(target=imageProcessor1.start_detecting, args=("", "1")).start()
#Thread(target=imageProcessor2.start_detecting, args=("", "2")).start()
#Thread(target=imageProcessor3.start_detecting, args=("", "3")).start()
#Thread(target=imageProcessor4.start_detecting, args=("", "4")).start()

print("All threads started")
sleep(10)
"""
