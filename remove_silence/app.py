import os

from flask import (
    Flask,
    render_template,    
    url_for
)

import plot
import extract

UPLOAD_FOLDER = './static/video/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 파일 업로드 페이지 렌더링
@app.route('/')
def index():
    return render_template('index.html')


# import librosa
# import moviepy.editor as mp
# import numpy as np
# 오디오 추출 
@app.route('/process', methods = ['GET','POST'])
def upload_file():
    if request.method == "POST":
        #파일객체 가져오기
        f = request.files['mp4file']
        filename = secure_filename(f.filename)
        f.save(UPLOAD_FOLDER + filename)
        wav_path, wav_name = extract.extract_wav(filename)
        png_name = plot.plot(wav_path, wav_name)
        return render_template("process.html", output = "uploads/"+filename)
    

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