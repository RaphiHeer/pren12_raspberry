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
    def __init__(self, settings, imageQueue: Queue):
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
        self.camera.shutter_speed = 20000
        self.camera.iso = self.iso

        # Create stream
        self.rawCapture = PiRGBArray(self.camera, size=self.resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

        # Count images and FPS
        self.imagesReaded = 0
        self.startMeasureTime = 0

        # Create lock
        self.lock = Lock()
        self.imageQueue = imageQueue

    def start(self, useMultiProcessing = False):
        # start the thread to read frames from the video stream
        self.useMultiProcessing = useMultiProcessing

        if useMultiProcessing:
            t = Thread(target=self.updateMultprocessing, args=())
        else:
            t = Thread(target=self.updateMultithreading, args=())
        t.daemon = True
        self.startMeasureTime = time.time()
        t.start()
        return self

    def updateMultprocessing(self):
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
            print("Set next frame")
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def updateMultithreading(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)
            print("Set next frame")
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
            retFrame = self.frame

        self.imagesReaded += 1
        if self.imagesReaded % 50 == 0:
            totalTime = time.time() - self.startMeasureTime
            fps = self.imagesReaded / totalTime
            print("FPS: " + str(fps))

        # return the frame most recently read
        return retFrame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
