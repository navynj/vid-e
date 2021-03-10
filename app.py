import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
#from . import cutting

UPLOAD_FOLDER = './static/video/'
ALLOWED_EXTENSIONS = {'mp4', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#파일 업로드페이지 렌더링
@app.route('/')
#@app.route('/index')
def index():
    return render_template("index.html")

#파일 업로드
@app.route('/upload', methods = ['GET','POST'])
def upload_file():
    if request.method == "POST":
        #파일객체 가져오기
        f = request.files['mp4file']
        filename = secure_filename(f.filename)
        f.save(UPLOAD_FOLDER + filename)
        return render_template("sucess.html", output = "video/"+filename)
 

#무음자르기 페이지 렌더링
@app.route('/cut')
def cut():
    return render_template("cut.html", title = "cut")

#추후 효과음추가 페이지 렌더링
@app.route('/sound')
def sound():
    return render_template("sound.html", title = "sound")


if __name__ == '__main__':
    app.run(debug = True)