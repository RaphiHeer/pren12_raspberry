from skimage.io import imread
from skimage.transform import resize
import numpy as np
from skimage import data, io
from skimage import img_as_ubyte		#convert float to uint8
from skimage.color import rgb2gray
import imutils
import time
from time import sleep
from imutils.video import VideoStream
from keras.models import load_model
import cv2
import numpy as np
#from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS


class ImageProcessor:

    def __init__(self, config,  model, imageDebugger):
        self.model = model
        self.config = config
        self.imageDebugger = imageDebugger

    def start_detecting(self, arduinoConnector, threadID):
        print("ImageProcessor_start_detecting")

        #vs = PiVideoStream(resolution=(640, 480)).start()
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        fps = FPS().start()

        while True:
            image = vs.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            print("Thread captured image %s" % threadID)
            # detect edges in the image
            # threshold the image by setting all pixel values less than 225
            # to 255 (white; foreground) and all pixel values >= 225 to 255
            # (black; background), thereby segmenting the image
            edged_image = cv2.Canny(gray, 224, 255)
            self.imageDebugger.debugImage("Edge", edged_image)

            # find contours (i.e., outlines) of the foreground objects in the
            # thresholded image
            cnts = cv2.findContours(edged_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[1]
            output = image.copy()

            # loop over the contours
            for c in cnts:
                # draw each contour on the output image with a 3px thick purple
                # outline, then display the output contours one at a time

                rect = cv2.boundingRect(c)
                x, y, w, h = rect

                # Sort out small elements
                if w < 50 or h < 50:
                    cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
                    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    continue

                # Sort out contours, which have a high difference between height and width
                # heigthWidthRatio = h/w
                # if (heigthWidthRatio < 0.5) | (heigthWidthRatio > 1.5):
                #    cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
                #    cv2.rectangle(output, (x,y), (x+w, y+h), (0,50,210), 2)
                #    continue

                # Resize image for DNN-Prediction
                im_cutted = gray[y - 5:(y + h + 5), x - 5:(x + w + 5)].copy()
                im_cutted_and_inverted = cv2.threshold(im_cutted.copy(), 100, 255, cv2.THRESH_BINARY_INV)[1]

                # If something went wrong in the thresholding function: continue
                if im_cutted_and_inverted is None:
                    cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
                    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    continue

                im_resize1 = cv2.resize(im_cutted_and_inverted, (28, 28))
                im_resize2 = resize(im_resize1, (28, 28), mode='constant')
                im_final = im_resize2.reshape(1, 28, 28, 1)

                self.imageDebugger.debugImage("Resize", im_resize2)

                # Predict digit on image
                start_predict = time.time()
                ans = self.model.predict(im_final)
                time_for_predict = time.time() - start_predict

                number = ans[0].tolist().index(max(ans[0].tolist()))
                prob = ans[0].tolist()[number] * 100

                if prob < 95:
                    cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
                    cv2.rectangle(output, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.putText(output, ("%i" % number), (x - 20, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.putText(output, ("%.3f %%" % prob), (x + 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    continue

                print(ans.shape)

                # cv2.waitKey()
                # print(ans[0])
                # print('DNN predicted digit is: ',ans)

                # print(cv2.contourArea(c))

                # Print predicted digit
                cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(output, ("%i" % number), (x - 20, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(output, ("%.3f %%" % prob), (x + 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # cv2.waitKey()

            self.imageDebugger.debugImage("Contours", output)

            # if q is pressed, break the loop
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            fps.update()

        fps.stop()
        vs.stop()
        cv2.destroyAllWindows()
