

class ImageFeatureDetectorBase:
    def __init__(self, settings):
        print("Init Feature Detection Base")

    def detectFeatures(self, image):
        raise NotImplemented("detectFeatures from abstract ImageFeatureDetectionBase not implemented")