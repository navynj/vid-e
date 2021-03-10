import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
#from . import cutting

UPLOAD_FOLDER = '/Users/gimjin-a/Desktop/github/ssumit/static/upload/'
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
        #업로드하면 cutting페이지 나오고 업로드한 파일 재생할 수 있게끔 했다
        return render_template("sucess.html", output = "upload/"+filename)
    #파일업로드하고나서 cut sound 선택할 수 있게 하는게 나을라나?

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