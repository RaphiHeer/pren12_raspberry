

class ImageFeatureDetectorBase:
    def __init__(self, settings):
        print("Init Feature Detection Base")

    def detectFeatures(self, image, drawImage = None):
        raise NotImplemented("detectFeatures from abstract ImageFeatureDetectionBase not implemented")