

class ImageVideoStreamBase:
    def __init__(self, settings):
        print("Init ImageVideoStreamBase")

    def start(self):
        raise NotImplemented("start from abstract ImageVideoStreamBase not implemented")

    def read(self):
        raise NotImplemented("read from abstract ImageVideoStreamBase not implemented")

    def stop(self):
        raise NotImplemented("stop from abstract ImageVideoStreamBase not implemented")