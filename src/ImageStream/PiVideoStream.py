# import the necessary packages
from .ImageVideoStreamBase import *
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread #, Lock
from multiprocessing import Lock, Queue
from imutils.video import FPS
import time
import cv2


class PiVideoStream(ImageVideoStreamBase):
    def __init__(self, settings, useMultiProcessing = False):

        self.useMultiProcessing = useMultiProcessing

        # Read settings
        self.resolution = settings['resolution']
        self.framerate = settings['framerate']
        self.shutterTime = settings['shutterTime']
        self.iso = settings['iso']

        # Init camera and settings
        self.camera = PiCamera()
        self.camera.resolution = self.resolution
        self.camera.framerate = self.framerate
        self.camera.exposure_mode = 'off'
        self.camera.rotation = 180
        self.camera.shutter_speed = self.shutterTime
        self.camera.iso = self.iso

        # Create stream
        self.rawCapture = PiRGBArray(self.camera, size=self.resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.started = False
        self.stopped = False

        # Count images and FPS
        self.imagesReaded = 0
        self.startMeasureTime = 0

        # Create lock
        if self.useMultiProcessing:
            self.imageQueue = Queue(maxsize=5)
            self.lock = Lock()

    def start(self):
        # If start was already called
        if self.started:
            return self
        self.started = True

        # start the thread to read frames from the video stream
        if self.useMultiProcessing:
            t = Thread(target=self.updateMultProcessing, args=())
        else:
            t = Thread(target=self.updateMultiThreading, args=())
        t.daemon = True
        self.startMeasureTime = time.time()
        t.start()
        return self

    def updateMultProcessing(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            frame = f.array
            self.rawCapture.truncate(0)
            if self.imageQueue.full():
                print("Cleaning 1 element from queue")
                self.imageQueue.get(block=True)
            self.imageQueue.put(frame)
            #print("Set next frame")
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def updateMultiThreading(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)
            #print("Set next frame")
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        if self.useMultiProcessing:
            retFrame = self.imageQueue.get(block=True)
        else:
            retFrame = self.frame.copy()

        self.imagesReaded += 1

        # return the frame most recently read
        return retFrame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def getImageQueue(self):
        return self.imageQueue