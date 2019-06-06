import argparse
import importlib
from threading import Thread
import time
from multiprocessing import Process, Queue, Pipe
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import threading
from ConfigReader import *
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

def runImageProcessorAsProcess(pipe: Pipe):
    print("Process created!!!!!!!!!")
    imageProcessorSetting, arduinoConnector, debugger, stream = pipe.recv()
    imageProcessor = factory.createImageProcessor(imageProcessorSetting, debugger)
    print("This is a new process!!!!!!!!!!")
    imageProcessor.processVideoStream(stream, arduinoConnector)
    return


def runImageProcessorAsThread(imageProcessorSetting, stream, debugger ,arduinoConnector):
    try:
        print("Run new Thread!")
        print(imageProcessorSetting)
        imageProcessor = factory.createImageProcessor(imageProcessorSetting, debugger)
        print("Started image processing")
        imageProcessor.processVideoStream(stream, arduinoConnector)
        print("Ended image Processing")
    except Exception as e:
        print("Exception in thread: %s" % str(e))
    return

def runMainApplication(configPath):
    config = ConfigReader(configPath)

    debugger = ImageDebugger(config.getApplicationSettings())
    arduinoConnector = ArduinoConnector()

    imageQueue = Queue(maxsize=5)
    stream = createVideoStream(config.getImageStreamSettings(), imageQueue)
    stream = stream.start(useMultiProcessing)

    #factory = ImageProcessorFactory()

    imageProcessors = factory.createImageProcessorList(config.imageProcessors, debugger)

    if useMultiProcessing:
        print("Using Multiprocessing")
        #processList = createProcesses(imageProcessors, stream, arduinoConnector)
        with ProcessPoolExecutor(max_workers=6) as pool:
            for imageProcessorSettings in config.imageProcessors:
                print("Starting new process\n\n\n")
                print(imageProcessorSettings)
                parent_conn, child_conn = Pipe()
                pool.submit(runImageProcessorAsProcess, child_conn)
                print("Send stuff")
                #parent_conn.send((imageProcessorSettings, arduinoConnector, debugger, stream))

            print("Stuff initialized")

            while True:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    print("Keyboard Interrupt received")
                    arduinoConnector.shutdownConnection()
                    stream.stop()
                    pool.shutdown()
                    break

    if useMultiProcessing is False:
        print("Using Threads")
        #threadList = createImageProcessingThreadList(imageProcessors, stream, arduinoConnector)
        with ThreadPoolExecutor(max_workers=6) as pool:
            for imageProcessorSettings in config.imageProcessors:
                print("Starting new threads\n\n\n")
                pool.submit(runImageProcessorAsThread, imageProcessorSettings, stream, debugger, arduinoConnector)
                print("AfterSubmit")
                #thread.start()

            while True:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    print("Keyboard Interrupt received")
                    arduinoConnector.shutdownConnection()
                    stream.stop()
                    pool.shutdown()
                    break

    #for process in processList:
    #    process.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Keyboard Interrupt received")
            arduinoConnector.shutdownConnection()
            stream.stop()
            if useMultiProcessing:
                for process in processList:
                    process.terminate()
            else:
                for thread in threadList:
                    thread.stop()
            print("Shutting down application")
            break


if __name__ == '__main__':
    runMainApplication(configPath)

