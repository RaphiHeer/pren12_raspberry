from multiprocessing import Process, Pool, Pipe
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import time

from ImageProcessing import *
from ImageProcessing.ImageDebugger import *
import ImageProcessing.ImageProcessorFactory as factory

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

def runImageProcessingProcessPool(imageProcessorSettingsList, applicationSettings, stream, arduinoConnector):
    print("Using Multiprocessing")
    #processList = createProcesses(imageProcessors, stream, arduinoConnector)
    with ProcessPoolExecutor(max_workers=6) as pool:
        for imageProcessorSettings in imageProcessorSettingsList:
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
    return

def runImageProcessingThreadPool(imageProcessorSettingsList, applicationSettings, stream, arduinoConnector):
    print("Using Threads")
    # threadList = createImageProcessingThreadList(imageProcessors, stream, arduinoConnector)
    debugger = ImageDebugger(applicationSettings)
    with ThreadPoolExecutor(max_workers=6) as pool:
        for imageProcessorSettings in imageProcessorSettingsList:
            print("Starting new threads\n\n\n")
            print(imageProcessorSettingsList)
            pool.submit(runImageProcessorAsThread, imageProcessorSettings, stream, debugger, arduinoConnector)
            print("AfterSubmit")
            # thread.start()

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print("Keyboard Interrupt received")
                arduinoConnector.shutdownConnection()
                stream.stop()
                pool.shutdown()
                break

    return
