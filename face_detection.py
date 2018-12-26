import cv2
import os


class FaceDetection:
    def __init__(self, path, name):
        rects, img = self.__detect(path)
        self.__box(rects, img, name)

    def  __detect(self, path):
        img = cv2.imread(path)
        cascade = cv2.CascadeClassifier("static/haarcascade/haarcascade_frontalface_alt.xml")
        rects = cascade.detectMultiScale(img, 1.15, 3, cv2.CASCADE_SCALE_IMAGE, (20, 20))

        if len(rects) == 0:
            return [], img
        rects[:, 2:] += rects[:, :2]
        return rects, img

    def __box(self, rects, img, name):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 4)

        cv2.imwrite('static/detected_img/' + name, img)
