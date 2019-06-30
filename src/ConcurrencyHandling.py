from multiprocessing import Process, Pool, Pipe, current_process, get_logger, log_to_stderr
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import time
import logging
from ImageProcessing import *
from ImageProcessing.ImageDebugger import *
import ImageProcessing.ImageProcessorFactory as factory


# Function called if a process for image processing is created
def runImageProcessorAsProcess(settings, arduinoConnector, stream):

    logger = get_logger()
    logger.info("Process created: " + current_process().name)

    applicationSettings, imageProcessorSettings = settings
    imageDebugger = ImageDebugger(applicationSettings)

    imageProcessor = factory.createImageProcessor(imageProcessorSettings, imageDebugger, logger)
    logger.info("Image processor created. Process video stream starts on process: " + current_process().name)

    imageProcessor.processVideoStream(stream, arduinoConnector)

    return

# Function called if a thread for image processing is created
def runImageProcessorAsThread(imageProcessorSetting, stream, arduinoConnector, debugger):
    try:
        logger = logging.getLogger()
        logger.info("Run new Thread!")
        imageProcessor = factory.createImageProcessor(imageProcessorSetting, debugger, logger)
        logger.debug("Started image processing")
        imageProcessor.processVideoStream(stream, arduinoConnector)
        logger.debug("Ended image Processing")
    except Exception as e:
        logger.critical("Exception in thread: %s" % str(e))
    return

def runImageProcessingProcessPool(applicationSettings, imageProcessorSettings, stream, arduinoConnector):
    print("Using Multiprocessing")
    #processList = createProcesses(imageProcessors, stream, arduinoConnector)
    log_to_stderr()
    logger = get_logger()
    logger.setLevel(logging.DEBUG)
    logger.info("Setup logger")
    logger.debug(imageProcessorSettings)
    processList = []
    for i in range(0, imageProcessorSettings["numberOfImageProcessors"]):
        logger.info("Starting new process")
        settings = [applicationSettings, imageProcessorSettings]

        process = Process(target=runImageProcessorAsProcess, args=(settings, arduinoConnector, stream))
        processList.append(process)
        process.start()

    logger.info("Stuff initialized")

    while True:
        try:
            time.sleep(1)
            print("Main app is sleeping")
        except KeyboardInterrupt:
            print("Keyboard Interrupt received")
            for process in processList:
                process.close()
            arduinoConnector.shutdownConnection()
            stream.stop()
            break
    return

def runImageProcessingThreadPool(applicationSettings, imageProcessorSettings, stream, arduinoConnector):
    print("Using Threads")
    debugger = ImageDebugger(applicationSettings)

    with ThreadPoolExecutor(max_workers=6) as pool:
        for i in range(1, imageProcessorSettings["numberOfImageProcessors"]):
            print("Starting new threads\n\n\n")
            print(imageProcessorSettings)
            pool.submit(runImageProcessorAsThread, imageProcessorSettings, stream, arduinoConnector, debugger)
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
