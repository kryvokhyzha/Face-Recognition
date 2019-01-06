import face_recognition
import cv2
import os
import pandas as pd

from time import time


class FaceRecognitionFromVideo:
    def __init__(self):
        self._images = []
        self._input_video = None
        self._face_locations = []
        self._face_encodings = []
        self._face_names = []
        self._face_group = []
        self._face_date = []
        self._frame_number = 0

        dirs = os.listdir(os.getcwd()+'/images')
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

    def start_recognition(self, path, tolerance=0.50, skip_frame=20):
        print('Tolerance value:', tolerance)
        print('Skip_frame value:', skip_frame)

        self._input_video = cv2.VideoCapture(path)
        if not self._input_video.isOpened():
            return True


        know_faces = []
        for image in self._images:
            current_image = face_recognition.load_image_file(image)
            know_faces.append(face_recognition.face_encodings(current_image)[0])

        length = int(self._input_video.get(cv2.CAP_PROP_FRAME_COUNT))
        print('Frame count in video:', length)
        while True:
            ret, frame = self._input_video.read()

            if not ret:
                return

            self._frame_number += 1

            if self._frame_number >= length:
                return

            if self._frame_number % skip_frame != 0:
                continue

            print('Current index of frame:', self._frame_number)

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

        # self._input_video.release()
        return False

    def write_to_excel(self, file_name='Student_list'):
        df = pd.DataFrame({'Student': self._face_names, 'Group': self._face_group, 'Time': self._face_date})
        writer = pd.ExcelWriter('static\\output\\from video\\' +
                                file_name + '_' + str(int(time() * 1000)) + '.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
