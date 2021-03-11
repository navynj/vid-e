import os

from flask import (
    Flask,
    render_template,
    request,
    url_for,
    jsonify
)


app = Flask(__name__)

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
        # 파일객체 저장하기
        f = request.files['input-file']
        filename = secure_filename(f.filename)
        f.save(UPLOAD_FOLDER + filename)

        # clips = [mp.VideoFileClip(f"{INPUT}/{fname}"]

        # load audio / show waveform information

        # input topDB / get topDB

        # get silence

        # remove silence

        return render_template("process.html", output = "uploads/"+filename)
    
if __name__ == '__main__':
    app.run(debug = True)