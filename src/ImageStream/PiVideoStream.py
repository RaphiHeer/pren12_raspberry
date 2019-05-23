# import the necessary packages
from .ImageVideoStreamBase import *
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from multiprocessing import Lock
import cv2

class PiVideoStream(ImageVideoStreamBase):
    def __init__(self, settings):
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
        self.stopped = False

        self.lock = Lock()

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        self.lock.acquire()
        retFrame = self.frame
        self.lock.release()
        # return the frame most recently read
        return retFrame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
