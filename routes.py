from app import app

from flask import render_template, request, send_file, send_from_directory

from errors import *
from face_detection import FaceDetection
from face_recognition_from_camera import FaceRecognitionFromCamera
from face_recognition_from_video import FaceRecognitionFromVideo

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


@app.route('/output/<slug1>/<slug2>')
def download(slug1, slug2):
    try:
        target = 'static/output/' + slug1 + '/'
        return send_from_directory(directory=target, filename=slug2, as_attachment=True)
    except Exception as e:
        return str(e)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/site_info')
def site_info():
    return render_template('site_info.html')


@app.route('/how_to_add_img')
def how_to_add_img():
    return render_template('how_to_add_img.html')


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


@app.route('/face_recognition_from_camera', methods=['POST', 'GET'])
def face_recognition_from_camera():
    if request.method == 'POST':
        tolerance = 1.0 - (int(request.form['toleranceSlider']) / 100.)

        face_rec = FaceRecognitionFromCamera()
        error = face_rec.start_recognition(tolerance=tolerance)
        face_rec.write_to_excel()

        list_of_excel = os.listdir('static/output/from webcam/')[-5:]
        list_of_excel.reverse()
        print('List of excel file:', list_of_excel)

        return render_template('face_recognition_from_camera.html', show_label=True,
                               list_of_excel=list_of_excel, error=error)
    else:
        list_of_excel = os.listdir('static/output/from webcam/')[-5:]
        list_of_excel.reverse()
        print('List of excel file:', list_of_excel)

        return render_template('face_recognition_from_camera.html', list_of_excel=list_of_excel,
                               show_label=False, error=False)


@app.route('/face_recognition_from_video', methods=['POST', 'GET'])
def face_recognition_from_video():
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'static\\upload_video\\')
        print('Path to folder with file:', target)

        if not os.path.isdir(target):
            os.mkdir(target)

        error = False
        for file in request.files.getlist('file'):
            print('Name of file:', file)
            filename = file.filename

            destination = ''.join([target, filename])
            print('Path to folder (destination):', destination)

            file.save(destination)

            tolerance = 1.0 - (int(request.form['toleranceSlider']) / 100.)
            skip_frame = int(request.form['skipFrameSlider'])

            face_rec = FaceRecognitionFromVideo()
            error = face_rec.start_recognition(path=destination, tolerance=tolerance, skip_frame=skip_frame)
            face_rec.write_to_excel()

        list_of_excel = os.listdir('static/output/from video/')[-5:]
        list_of_excel.reverse()
        print('List of excel file:', list_of_excel)

        return render_template('face_recognition_from_video.html', error=error,
                               show_label=True, list_of_excel=list_of_excel)
    else:
        list_of_excel = os.listdir('static/output/from video/')[-5:]
        list_of_excel.reverse()
        print('List of excel file:', list_of_excel)
        return render_template('face_recognition_from_video.html', error=False,
                               show_label=False, list_of_excel=list_of_excel)
