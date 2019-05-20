import cv2

class ImageDebugger:
    def __init__(self, showImage = False, saveImage = False):
        """"
        if isinstance(showImage, str):
            self.showImage = (showImage == 'true')


        if isinstance(saveImage, str):
            self.saveImage = (saveImage == 'true')
        """

        self.showImage = True
        self.saveImage = False

    def debugImage(self, caption, image):
        if(self.showImage):
            cv2.imshow(caption, image)
        if(self.saveImage):
            filename = caption + 'png'
            cv2.imwrite(filename, image)

    def drawContoursOnImage(self, image, regions, colorBoundingBox):

        if self.showImage | self.saveImage:
            for region in regions:
                print(region)
                #rect = cv2.boundingRect(region)
                x, y, w, h = rect
                cv2.drawContours(image, [region], -1, (240, 0, 159), 3)
                cv2.rectangle(image, (x,y), (x+w, y+h), colorBoundingBox, 2)

        return

    def writePreditcionOnImage(self, image, region, prediction, propability, color):
        if self.showImage | self.saveImage:
            x, y, w, h = region
            cv2.putText(image, ("%i" % prediction), (x-20, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(image, ("%.3f %%" % propability), (x + 50, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        return