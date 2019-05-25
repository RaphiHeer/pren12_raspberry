import json

class ConfigReader:

    def __init__(self, configPath):
        print("Created Configreader")
        with open(configPath) as json_data:
            jsonData = json.load(json_data)

        self.setApplicationSettings(jsonData)
        self.setImageStreamSettings(jsonData)
        self.setImageProcessorSettings(jsonData)

    def getApplicationSettings(self):
        return self.applicationSettings

    def getImageStreamSettings(self):
        return self.imageStreamSettings

    def getImageProcessors(self):
        return self.imageProcessors

    def setApplicationSettings(self, jsonData):
        jsonApplicationSettings = jsonData.get("applicationSettings", {})
        self.applicationSettings = {}

        self.applicationSettings["logfile"] = jsonApplicationSettings.get("logfile", "data.log")
        self.applicationSettings["createLogs"] = jsonApplicationSettings.get("createLogs", False)
        self.applicationSettings["logfileRandomPrefix"] = jsonApplicationSettings.get("logfileRandomPrefix", True)
        self.applicationSettings["showImages"] = jsonApplicationSettings.get("showImages", True)
        self.applicationSettings["saveImages"] = jsonApplicationSettings.get("saveImages", False)


    def setImageStreamSettings(self, jsonData):
        jsonImageStreamSettings = jsonData.get("imageStream", "default")
        self.imageStreamSettings = {}
        if jsonImageStreamSettings == "default":
            self.imageStreamSettings["shutterTime"] = 4000
        else:
            self.imageStreamSettings["type"] = jsonImageStreamSettings.get("type", "picam")
            if self.imageStreamSettings["type"] == "picam":
                self.imageStreamSettings["shutterTime"] = jsonImageStreamSettings.get("shutterTime", 4000)
                self.imageStreamSettings["iso"] = jsonImageStreamSettings.get("iso", 1000)
                self.imageStreamSettings["framerate"] = jsonImageStreamSettings.get("framerate", 40)
                self.imageStreamSettings["resolutionW"] = jsonImageStreamSettings.get("resolutionW", 640)
                self.imageStreamSettings["resolutionH"] = jsonImageStreamSettings.get("resolutionH", 480)
                self.imageStreamSettings["resolution"] = (self.imageStreamSettings["resolutionW"], self.imageStreamSettings["resolutionH"])
            elif jsonImageStreamSettings["type"] == "file":
                self.imageStreamSettings["path"] = jsonImageStreamSettings.get("path")
                self.imageStreamSettings["framerate"] = jsonImageStreamSettings.get("framerate", 30)
            print(self.imageStreamSettings)

    def setImageProcessorSettings(self, jsonData):
        jsonImageProcessors = jsonData.get("imageProcessors", "None")

        self.imageProcessors = []

        for jsonImageProcessor in jsonImageProcessors:
            self.imageProcessors.append(self.createImageProcessorSettings(jsonImageProcessor))

    def createImageProcessorSettings(self, jsonImageProcessor):
        imageProcessorSettings = {}
        imageProcessorSettings["id"] = jsonImageProcessor.get("id")
        imageProcessorSettings["type"] = jsonImageProcessor.get("type")
        imageProcessorSettings["imageSource"] = jsonImageProcessor.get("imageSource", "videoStream")

        jsonPreProcessor = jsonImageProcessor.get("preProcessing")
        jsonSegmentation = jsonImageProcessor.get("segmentation")
        jsonFeatureDetection = jsonImageProcessor.get("featureDetection")
        jsonSignDetection = jsonImageProcessor.get("signDetection")

        imageProcessorSettings["preProcessing"] = self.createImagePreProcessorSettings(jsonPreProcessor)
        imageProcessorSettings["segmentation"] = self.createImageSegmentation(jsonSegmentation)
        imageProcessorSettings["featureDetection"] = self.createImageFeatureDetection(jsonFeatureDetection)
        imageProcessorSettings["signDetection"] = self.createImageSignDetection(jsonSignDetection)

        return imageProcessorSettings

    def createImagePreProcessorSettings(self, jsonImagePreprocessor):
        preProcessorSettings = {}
        preProcessorSettings["type"] = jsonImagePreprocessor.get("type", "none")

        if preProcessorSettings["type"] == "gammaCorrection":
            preProcessorSettings["gamma"] = jsonImagePreprocessor.get("gamma", 2)

        return preProcessorSettings



    def createImageSegmentation(self, jsonImageSegmentation):
        segmentationSettings = {}
        segmentationSettings["type"] = jsonImageSegmentation.get("type", "canny")

        if segmentationSettings["type"] == "canny":
            segmentationSettings["threshold1"] = jsonImageSegmentation.get("threshold1", 200)
            segmentationSettings["threshold2"] = jsonImageSegmentation.get("threshold2", 210)
        elif segmentationSettings["type"] == "threshold":
            segmentationSettings["threshold1"] = jsonImageSegmentation.get("threshold1", 150)
            segmentationSettings["threshold2"] = jsonImageSegmentation.get("threshold2", 255)
            segmentationSettings["threshMode"] = jsonImageSegmentation.get("threshMode", "binary")

        return segmentationSettings

    def createImageFeatureDetection(self, jsonImageFeatureDetection):
        featureDetectionSettings = {}
        featureDetectionSettings["type"] = jsonImageFeatureDetection.get("type", "findContours")

        if featureDetectionSettings["type"] == "findContours":
            featureDetectionSettings["mode"] = jsonImageFeatureDetection.get("mode", "RETR_EXTERNAL")
            featureDetectionSettings["method"] = jsonImageFeatureDetection.get("method", "CHAIN_APPROX_SIMPLE")


        return featureDetectionSettings

    def createImageSignDetection(self, jsonImageSignDetection):

        signDetectionSettings = {}
        signDetectionSettings["type"] = jsonImageSignDetection.get("type", "DnnMnist")

        if signDetectionSettings["type"] == "DnnMnist":
            signDetectionSettings["path"] = jsonImageSignDetection.get("path", "model/mnist_trained_model.h5")

        return signDetectionSettings

