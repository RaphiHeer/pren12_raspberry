import argparse
import importlib
from threading import Thread
import time
from multiprocessing import Process
from ConfigReader import *
from ImageProcessing import *
from ImageProcessing.ImageDebugger import *
from ImageProcessing.ImageProcessorFactory import *
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


def createProcesses(imageProcessors, stream, arduinoConnector):
    processList = []
    for imageProcessor in imageProcessors:
        processList.append(Process(target=imageProcessor.processVideoStream, args=(stream, arduinoConnector)))

    return processList

def createThreads():
    threadList = []

    return threadList

def runMainApplication(configPath):
    config = ConfigReader(configPath)

    debugger = ImageDebugger(config.getApplicationSettings())
    arduinoConnector = ArduinoConnector()

    stream = createVideoStream(config.getImageStreamSettings())
    stream = stream.start()

    factory = ImageProcessorFactory()

    imageProcessors = factory.createImageProcessors(config.imageProcessors, debugger)

    processList = createProcesses(imageProcessors, stream, arduinoConnector)

    #imageProcessors[0].processVideoStream(stream, "")
    for process in processList:
        process.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Keyboard Interrupt received")
            for process in processList:
                process.terminate()
            print("Shutting down application")
            break


if __name__ == '__main__':
    runMainApplication(configPath)

