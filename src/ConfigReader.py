import json

class ConfigReader:



    def __init__(self, configPath):
        print("Created Configreader")
        with open(configPath) as json_data:
            jsonData = json.load(json_data)

        self.setLogSettings(jsonData)
        self.setCameraSettings(jsonData)
        self.setImageProcessorSettings(jsonData)

    def setLogSettings(self, jsonData):
        self.logfile = jsonData.get("logfile", "data.log")
        self.createLogs = jsonData.get("createLogs", False)
        self.logfileRandomPrefix = jsonData.get("logfileRandomPrefix", True)
        self.showImages = jsonData.get("showImages", True)
        self.saveImages = jsonData.get("saveImages", False)


    def setCameraSettings(self, jsonData):
        jsonCameraSettings = jsonData.get("cameraSettings", "default")
        self.cameraSettings = {}
        if jsonCameraSettings == "default":
            self.cameraSettings["shutterTime"] = 1000
        else:
            self.cameraSettings["shutterTime"] = jsonCameraSettings.get("shutterTime", 1000)

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
        jsonEdgeDetection = jsonImageProcessor.get("edgeDetection")
        jsonFeatureDetection = jsonImageProcessor.get("featureDetection")
        jsonSignDetection = jsonImageProcessor.get("signDetection")

        imageProcessorSettings["preProcessing"] = self.createImagePreProcessorSettings(jsonPreProcessor)
        imageProcessorSettings["edgeDetection"] = self.createImageEdgeDetection(jsonEdgeDetection)
        imageProcessorSettings["featureDetection"] = self.createImageFeatureDetection(jsonFeatureDetection)
        imageProcessorSettings["signDetection"] = self.createImageSignDetection(jsonSignDetection)

        return imageProcessorSettings

    def createImagePreProcessorSettings(self, jsonImagePreprocessor):
        preProcessorSettings = {}
        preProcessorSettings["type"] = jsonImagePreprocessor.get("type", "none")

        return preProcessorSettings



    def createImageEdgeDetection(self, jsonImageEdgeDetection):
        edgeDetectionSettings = {}
        edgeDetectionSettings["type"] = jsonImageEdgeDetection.get("type", "canny")

        if edgeDetectionSettings["type"] == "canny":
            edgeDetectionSettings["threshold1"] = jsonImageEdgeDetection.get("threshold1", 200)
            edgeDetectionSettings["threshold2"] = jsonImageEdgeDetection.get("threshold2", 210)

        return edgeDetectionSettings

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

