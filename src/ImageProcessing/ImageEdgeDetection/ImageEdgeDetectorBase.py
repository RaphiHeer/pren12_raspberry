

class ImageEdgeDetectorBase:
    def __init__(self, settings):
        print("Init Edge Detection Base")

    def detectEdges(self, image):
        raise NotImplemented("detectEdges from abstract ImageEdgeDetectionBase not implemented")