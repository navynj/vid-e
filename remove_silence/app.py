import os

from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    send_from_directory
)
from werkzeug.utils import secure_filename

import plot
import extract

UPLOAD_FOLDER = './static/temp'
ALLOWED_EXTENSIONS = {'mp4', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 파일 업로드 페이지 렌더링
@app.route('/')
def index():
    return render_template('index.html', title={'main':'Upload your video', 'sub':'Remove silence from your video'})


# 오디오 추출 / 파형 출력 / top_db 입력
@app.route('/process', methods = ['GET','POST'])
def upload_file():
    if request.method == "POST":
        # 파일객체 저장하기
        f = request.files['input-file']
        file_name = secure_filename(f.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        f.save(file_path)
        return render_template("process.html", title={'main':'Top Db', 'sub': file_name}, src=file_path)
    
# 처리 완료 파일 다운로드
@app.route('/download', methods = ['GET','POST'])
def download():
    if request.method == "POST":
        src = request.form['src']
        return render_template("download.html", title = {'main':'Complete', 'sub':'your video'}, src=src)


if __name__ == '__main__':
    app.run(debug = True)