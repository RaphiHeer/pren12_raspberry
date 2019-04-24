import argparse
from threading import Thread
from ConfigReader import *
from ImageProcessing.ImageProcessor import *
from ImageProcessing.ImageProcessorFactory import *
from ImageProcessing.ImageDebugger import *
from keras.models import load_model
from time import sleep
from imutils.video import VideoStream

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=False, help="path to input image")
args = vars(ap.parse_args())

if args["config"]:
    configPath = args["config"]
else:
    configPath = "Ressources/config.json"

config = ConfigReader(configPath)

factory = ImageProcessorFactory()

objs = factory.createImageProcessors(config.imageProcessors)

vs = VideoStream(src=0).start()
sleep(2.0)
print(objs)
objs[0].processVideoStream(vs, "")

