import os, json
from flask import (Flask,
                   jsonify,
                   make_response,
                   render_template,
                   request,
                   url_for,
                   redirect,send_from_directory)
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.join(app.static_folder, 'temp')
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
    from process import extract_wav, speech_to_text, get_clean_text
    if request.method == "POST":
        # 업로드 비디오 저장
        f = request.files['input-file']
        file_name = secure_filename(f.filename)
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        f.save(file_path)
        # 오디오 추출
        gcs_uri, file_url, wav_name = extract_wav(file_name)
        # stt 변환
        stt_result = speech_to_text(gcs_uri)
        transcripts = get_clean_text(stt_result)
        return render_template("process.html", 
                               title = {
                                   'main' :'Remove Silence',
                                   'sub' : '최소 db를 입력하세요'
                                }, 
                               file = {
                                   'name' : file_name, # 변수명 video_name으로 수정, 객체도 video로 수정하자..
                                   'onlyname' : file_name.split('.')[0], # 변수명.. id 정도로? 수정하자
                                   'ext' : file_name.split('.')[1],
                                   'path' : file_path
                                },
                               audio = {
                                   'name' : wav_name,
                                   'path' : file_url
                                   'gcs_uri' : gcs_uri
                                },
                               result = stt_result
                            )

# 무음 구간 제거 : topdB입력 - 무음 제거 - 결정 :: fetch 방식
@app.route('/process/<name>.<ext>', methods = ['GET', 'POST'])
def show_result(name, ext):
    from process import split
    if request.method == 'POST':
        tdb = request.get_json()['tdb']
        removed_audio, sr, nonmute_intervals, mute_intervals = split(tdb, name+'.wav')
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
                            'tdb' : tdb,
                            'sr' : sr,
                            'nonmute_intervals' : nonmute_intervals.tolist(),
                            'mute_intervals': mute_intervals.tolist()
                       }
                    })

# 처리 완료 파일 다운로드 :: 작업X, 기존 form submit 방식 예상
@app.route('/download', methods = ['GET','POST'])
def download():
    if request.method == "POST":
        from process import remove_silence
        output_info = json.loads(json.loads(jsonify(request.form['output_info']).data, encoding='utf-8'))
        file_info = json.loads(json.loads(jsonify(request.form['file_info']).data, encoding='utf-8'))
        removed_video = remove_silence(file_info['onlyname'], file_info['ext'],output_info['tdb'], output_info['sr'], output_info['nonmute_intervals'])
        return render_template("download.html", 
                               title = {'main':'Download',
                                        'sub': f'your video'},
                               output = {'src' : removed_video}
                            )



if __name__ == '__main__':
    app.run(debug = True)