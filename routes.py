from app import app

from flask import render_template, request

from errors import *
from face_detection import FaceDetection
from face_recognition_from_camera import FaceRecognitionFromCamera

import os
import pandas as pd


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public'
    return r


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/face_detect', methods=['GET', 'POST'])
def face_detect():
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'static\\upload_img\\')
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist('file'):
            print(file)
            filename = file.filename

            destination = ''.join([target, filename])
            print(destination)

            file.save(destination)

            FaceDetection(destination, filename)

            path_detect_img = 'detected_img/' + filename
            path_upload_img = 'upload_img/' + filename

            return render_template('face_detect.html', is_post=True,
                                   path_detect_img=path_detect_img, path_upload_img=path_upload_img)
    else:
        return render_template('face_detect.html', is_post=False)


@app.route('/face_recognition', methods=['POST', 'GET'])
def face_recognition():
    if request.method == 'POST':
        face_rec = FaceRecognitionFromCamera()
        face_rec.start_recognition()
        face_rec.write_to_excel()

        show_excel = False
        if os.path.exists('static/output/Student_list.xlsx'):
            show_excel = True

        return render_template('face_recognition.html', show_excel=show_excel)
    else:
        show_excel = False
        if os.path.exists('static/output/Student_list.xlsx'):
            show_excel = True

        return render_template('face_recognition.html', show_excel=show_excel)
