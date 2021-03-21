import os
from flask import (Flask,
                   jsonify,
                   make_response,
                   render_template,
                   request,
                   url_for,
                   redirect,send_from_directory)
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/temp/'
ALLOWED_EXTENSIONS = {'mp4', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 파일 업로드
@app.route('/')
def index():
    return render_template('index.html', 
                           title = {'main':'Upload your video',
                                    'sub':'Remove silence from your video'})

# 업로드 비디오 저장 및 오디오 추출 :: 기존 form.submit()방식
@app.route('/process', methods = ['GET','POST'])
def extract_audio():
    from process import extract_wav
    if request.method == "POST":
        # 업로드 비디오 저장
        f = request.files['input-file']
        file_name = secure_filename(f.filename)
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        f.save(file_path)
        # 오디오 추출
        wav_path, wav_name = extract_wav(file_name)
        return render_template("process.html", 
                               title = {
                                   'main' :'Remove Silence',
                                   'sub' : '최소 db를 입력하세요'
                                }, 
                               file = {
                                   'name' : file_name,
                                   'onlyname' : file_name.split('.')[0],
                                   'ext' : file_name.split('.')[1],
                                   'path' : file_path
                                },
                               audio = {
                                   'name' : wav_name,
                                   'path' : wav_path
                                }
                            )

# 무음 구간 제거 : topdB입력 - 무음 제거 - 결정 :: fetch 방식
@app.route('/process/<name>.<ext>', methods = ['GET', 'POST'])
def show_result(name, ext):
    from process import split
    if request.method == 'POST':
        tdb = request.get_json()['tdb']
        removed_audio, sr, nonmute_intervals = split(tdb, name+'.wav')
        return jsonify({
                        "title" : {
                            'main' : 'Download',
                            'sub': f'{tdb} 값으로 무음구간이 삭제된 결과입니다'
                        },
                        "file" : {
                            'name' : f'{name}.{ext}',
                            'onlyname' : name,
                            'ext' : ext,
                            'path' : os.path.join(UPLOAD_FOLDER, f'{name}.{ext}')
                        },
                        "output" : {
                            'src' : removed_audio,
                            'sr' : sr,
                            'intervals' : nonmute_intervals.tolist()
                       }
                    })

# 처리 완료 파일 다운로드 :: 작업X, 기존 form submit 방식 예상
@app.route('/download', methods = ['GET','POST'])
def download():
    if request.method == "POST":
        from process import remove_silence
        removed_video = remove_silence(sr, non_mute_intervals)
        return render_template("download.html", 
                               title = {'main':'Download',
                                        'sub':'your video'}, 
                               output = {'src' : remove_video})



if __name__ == '__main__':
    app.run(debug = True)