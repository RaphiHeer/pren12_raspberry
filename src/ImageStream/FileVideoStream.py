# import the necessary packages
from .ImageVideoStreamBase import *
import cv2
import time
from os import listdir
from os.path import isfile, join

class FileVideoStream(ImageVideoStreamBase):
	def __init__(self, settings):
		# initialize the camera and stream
		print(settings)
		self.framerate = settings['framerate']
		self.secondsPerFrame = 1 / self.framerate
		self.path = settings['path']
		self.onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]

		self.frame = None
		self.stopped = False

		self.lastFrameRead = time.time()

		print("Seconds per frame: %.3f secs" % self.secondsPerFrame)
		print("LastFrameRead: %.3f secs" % self.lastFrameRead)
		print("LastFrameRead: %.3f secs" % (time.time() - self.lastFrameRead))
		time.sleep(5)

	def start(self):
		# start the thread to read frames from the video stream
		return self

	def read(self):
		# return the frame most recently read
		filename = self.path + self.onlyfiles.pop(0)
		frame = cv2.imread(filename)

		now = time.time()
		diffBetweenReads = time.time() - self.lastFrameRead
		self.lastFrameRead = now

		#if (diffBetweenReads < self.secondsPerFrame):
		#	print("Sleep till next frame: %.3f millis" % diffBetweenReads)
		#	time.sleep(diffBetweenReads - self.secondsPerFrame)
		time.sleep(0.25)

		return frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True