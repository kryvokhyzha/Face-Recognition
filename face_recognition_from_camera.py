import face_recognition
import cv2
import os
import pandas as pd

from time import time


class FaceRecognitionFromCamera:
    def __init__(self):
        self._images = []
        self._input_video = None
        self._face_locations = []
        self._face_encodings = []
        self._face_names = []
        self._face_group = []
        self._face_date = []
        self._frame_number = 0

        dirs = os.listdir(os.getcwd() + '/images')
        print('Group folder list:', dirs)
        dirs1 = []

        for sub_dir in dirs:
            im_list = list(os.listdir('images/' + sub_dir))
            im1 = []
            for i in im_list:
                im1.append('images/' + sub_dir + '/' + i)
            dirs1 = list(set(list(dirs1) + im1))

        for sub_dir in dirs1:
            im_list = list(os.listdir(sub_dir))
            im1 = []
            for i in im_list:
                im1.append(sub_dir + '/' + i)
            self._images = list(set(list(self._images) + im1))

    def start_recognition(self, tolerance=0.5, show_border=True):
        print('Tolerance value:', tolerance)
        print('Show_border value:', show_border)

        index = 0
        for i in [-1, 0, 1, 2]:
            capture = cv2.VideoCapture(i)
            if capture.isOpened():
                index = i
                break
        else:
            return True

        self._input_video = cv2.VideoCapture(index)
        print('Video capture index:', index)

        know_faces = []
        for image in self._images:
            current_image = face_recognition.load_image_file(image)
            know_faces.append(face_recognition.face_encodings(current_image)[0])

        while True:
            ret, frame = self._input_video.read()

            self._frame_number += 1

            rgb_frame = frame[:, :, ::-1]

            self._face_locations = face_recognition.face_locations(rgb_frame)
            self._face_encodings = face_recognition.face_encodings(rgb_frame, self._face_locations)

            # self._face_names = []
            # self._face_group = []
            # self._face_date = []
            for face_encoding in self._face_encodings:
                match = face_recognition.compare_faces(know_faces, face_encoding, tolerance=tolerance)

                name = None
                group = None
                date = None

                try:
                    count = match.index(True)
                    name = str(self._images[count]).split('/')[2]
                    group = str(self._images[count]).split('/')[1]
                    date = pd.Timestamp.now()
                except:
                    pass

                if (name and group and date) and not(name in self._face_names):
                    self._face_names.append(name)
                    self._face_group.append(group)
                    self._face_date.append(date)
                    print(self._face_names, self._face_group, self._face_date)

            for (top, right, bottom, left), name in zip(self._face_locations, self._face_names):
                if not name:
                    continue
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                if show_border:
                    cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            k = cv2.waitKey(1)
            if k == 27 or k == 13 or k == 32:
                break

            cv2.imshow('Video', frame)

        self._input_video.release()
        cv2.destroyAllWindows()
        return False

    def write_to_excel(self, file_name='Student_list'):
        df = pd.DataFrame({'Student': self._face_names, 'Group': self._face_group, 'Time': self._face_date})
        writer = pd.ExcelWriter('static\\output\\from webcam\\' +
                                file_name + '_' + str(int(time() * 1000)) + '.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
