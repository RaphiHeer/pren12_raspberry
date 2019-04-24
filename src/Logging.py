import cv2

class Logging:
    displayImages = False


    def displayImage(self, title, image):
        if self.displayImages:
            cv2.imshow(title, image)

