

class ImageSegmentationBase:
    def __init__(self, settings):
        print("Init Image Segmentation Base")

    def segmentImage(self, image):
        raise NotImplemented("detectEdges from abstract ImageSegmentationBase not implemented")