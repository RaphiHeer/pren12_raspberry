import argparse
import importlib
from threading import Thread
import time
from multiprocessing import Process, Queue, Pipe
import threading
import logging
from ConfigReader import *
import ConcurrencyHandling
import vma208
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

# Creates Video Stream
def createVideoStream(videoConfig, useMultiProcessing = False):
    if videoConfig["type"] == "picam":
        return PiVideoStream(videoConfig, useMultiProcessing)
    elif videoConfig["type"] == "file":
        return FileVideoStream(videoConfig, useMultiProcessing)

# Creates a process (obsolete)
def createProcesses(imageProcessors, stream, arduinoConnector):
    processList = []
    for imageProcessor in imageProcessors:
        #processList.append(Process(target=runImageProcessorAsProcess, args=(pipe)))
        processList.append(Process(target=imageProcessor.processVideoStream, args=(stream, arduinoConnector)))

    return processList

# Creates a thread list (obsolete)
def createImageProcessingThreadList(imageProcessors, stream, arduinoConnector):
    threadList = []
    for imageProcessor in imageProcessors:
        threadList.append(Thread(target=imageProcessor.processVideoStream, args=(stream, arduinoConnector)))

    return threadList

def runMainApplication(configPath, logger):

    # Get config reader (reads the config file)
    config = ConfigReader(configPath)

    # Get Applications settings from config
    applicationSettings = config.getApplicationSettings()
    concurrency = applicationSettings['concurrency']

    # Create objects for debugger and Arduino connector
    arduinoConnector = ArduinoConnector(concurrency)

    imageQueue = Queue(maxsize=5)
    if concurrency == "process":
        useMultiProcessing = True
    else:
        useMultiProcessing = False
    stream = createVideoStream(config.getImageStreamSettings(), useMultiProcessing)
    stream = stream.start()

    # Create logfile for vma208
    ts = time.gmtime()
    filename = time.strftime("vma208_logs/%Y-%m-%d %H_%M_%S .log", ts)
    logger.info("Write vma208 log data to file: " + filename)
    Thread(target=vma208.logDrivingData, args=(filename,)).start()

    # Used if multi processing is enabled (most performance)
    if concurrency == "process":
        ConcurrencyHandling.runImageProcessingProcessPool(applicationSettings, config.getImageProcessorSettings(), stream, arduinoConnector)

    # Used if multi threading is enabled
    elif concurrency == "thread":
        ConcurrencyHandling.runImageProcessingThreadPool(applicationSettings, config.getImageProcessorSettings(), stream, arduinoConnector)

    # Used if no concurrency is wished
    else:
        print("Started image processing without concurrency")
        imageProcessor = factory.createImageProcessor(config.getImageProcessorSettings(), debugger)
        imageProcessor.processVideoStream(stream, arduinoConnector)
        return


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", required=False, help="path to input image")
    ap.add_argument("-m", "--multiprocessing", required=False, default=False)
    args = vars(ap.parse_args())

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if args["config"]:
        configPath = args["config"]
        logger.info("Use %s as config file" % configPath)
    else:
        configPath = "Ressources/config.json"
        logger.info("Use default logging file from %s" % configPath)

    print("Load config from: " + configPath)
    runMainApplication(configPath, logger)

