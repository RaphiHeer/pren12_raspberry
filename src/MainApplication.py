import argparse
from threading import Thread
from ConfigReader import *
from ImageProcessing import *
from ImageDebugger import *
from keras.models import load_model
from time import sleep

#from src.SignDetection.ImagePreProcessing import *
#from src.SignDetection.FeatureExtraction import *
#from src.SignDetection.NumberPrediction import *

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=False, help="path to input image")
args = vars(ap.parse_args())

if args["config"]:
    configPath = args["config"]
else:
    configPath = "Ressources/config.json"

config = ConfigReader(configPath)
"""
#import CNN model weight
model= load_model('./model/mnist_trained_model.h5')
imageDebugger = ImageDebugger(True, False)

# imagePreprocessor = # ImagePreprocessor()
#featureExtractor = CannyContouring() # FeatureExtractor()
#numberPredictor = TensorFlowMnistPredictor() # NumberPredictor()

imageProcessor = ImageProcessor(config, model, imageDebugger)
imageProcessor.start_detecting("asdf", "1")

#imageProcessor1 = ImageProcessor(config, model, imageDebugger)
imageProcessor2 = ImageProcessor(config, model, imageDebugger)
imageProcessor3 = ImageProcessor(config, model, imageDebugger)
imageProcessor4 = ImageProcessor(config, model, imageDebugger)

#Thread(target=imageProcessor1.start_detecting, args=("", "1")).start()
#Thread(target=imageProcessor2.start_detecting, args=("", "2")).start()
#Thread(target=imageProcessor3.start_detecting, args=("", "3")).start()
#Thread(target=imageProcessor4.start_detecting, args=("", "4")).start()

print("All threads started")
sleep(10)
"""