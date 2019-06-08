import argparse
import importlib
from threading import Thread
import time
from multiprocessing import Process, Queue, Pipe
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import threading
from ConfigReader import *
import ConcurrencyHandling
from ImageProcessing import *
from ImageProcessing.ImageDebugger import *
import ImageProcessing.ImageProcessorFactory as factory
from ImageStream import *
from ImageStream.FileVideoStream import *
from ArduinoCommunication import *
from ArduinoCommunication.ArduinoConnector import *

try:
    from ImageStream.PiVideoStream import *
except ImportError:
    print("PiCamera is not installed. If this is not a raspberry pi, this is ok.")


ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=False, help="path to input image")
ap.add_argument("-m", "--multiprocessing", required=False, default=False)
args = vars(ap.parse_args())

if args["config"]:
    configPath = args["config"]
else:
    configPath = "Ressources/config.json"

if args["multiprocessing"]:
    useMultiProcessing = True
else:
    useMultiProcessing = False

print("Load config from: " + configPath)


def createVideoStream(videoConfig, imageQueue):
    if videoConfig["type"] == "picam":
        return PiVideoStream(videoConfig, imageQueue)
    elif videoConfig["type"] == "file":
        return FileVideoStream(videoConfig, imageQueue)


def createProcesses(imageProcessors, stream, arduinoConnector):
    processList = []
    for imageProcessor in imageProcessors:
        #processList.append(Process(target=runImageProcessorAsProcess, args=(pipe)))
        processList.append(Process(target=imageProcessor.processVideoStream, args=(stream, arduinoConnector)))

    return processList

def createImageProcessingThreadList(imageProcessors, stream, arduinoConnector):
    threadList = []
    for imageProcessor in imageProcessors:
        threadList.append(Thread(target=imageProcessor.processVideoStream, args=(stream, arduinoConnector)))

    return threadList

def createThreads():
    threadList = []

    return threadList



def runMainApplication(configPath):
    config = ConfigReader(configPath)

    applicationSettings = config.getApplicationSettings()
    concurrency = applicationSettings['concurrency']

    debugger = ImageDebugger(applicationSettings)
    arduinoConnector = ArduinoConnector()

    imageQueue = Queue(maxsize=5)
    stream = createVideoStream(config.getImageStreamSettings(), imageQueue)
    stream = stream.start(useMultiProcessing)

    #factory = ImageProcessorFactory()

    imageProcessors = factory.createImageProcessorList(config.imageProcessors, debugger)

    if concurrency == "process":
        ConcurrencyHandling.runImageProcessingProcessPool(config.imageProcessors, applicationSettings, stream, arduinoConnector)


    elif concurrency == "thread":
        ConcurrencyHandling.runImageProcessingThreadPool(config.imageProcessors, applicationSettings, stream, arduinoConnector)

    else:
        imageProcessor = factory.createImageProcessor(config.imageProcessors[0], debugger)
        print("Started image processing")
        imageProcessor.processVideoStream(stream, arduinoConnector)
        return
    #for process in processList:
    #    process.start()


if __name__ == '__main__':
    runMainApplication(configPath)

