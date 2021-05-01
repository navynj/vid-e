import os, json
from flask import (Flask,
                   jsonify,
                   make_response,
                   render_template,
                   request,
                   url_for,
                   redirect,send_from_directory)


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'mp4', 'wav'}
UPLOAD_FOLDER = os.path.join(app.static_folder, 'temp')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 파일 업로드
@app.route('/')
def index():
    return render_template('index.html', 
                           title = {'main':'편집할 영상을 업로드하세요',
                                    'sub':'mp4 확장자를 지원합니다'})

# 업로드 비디오 저장 및 오디오 추출 :: 기존 form.submit()방식
@app.route('/menu', methods = ['POST'])
def get_data_from_video():
    from file_processing import save_video, extract_wav, speech_to_text
    result = {}
    if request.method == "POST":
        # 0. 비디오 업로드
        result['video'] = save_video(request.files['input-file'])
        # 1. 오디오 추출
        result['audio'] = extract_wav(result['video']['name'])
        # 2. stt 변환
        result['stt'] = speech_to_text(result['audio']['gcs_uri'])
        # 3. json 저장
        result_path = os.path.join(UPLOAD_FOLDER, f"{result['video']['id']}.json")
        with open(result_path, "w", encoding='utf-8') as json_file:
            json.dump(result, json_file, ensure_ascii=False)
        # 4. html 렌더링
        return render_template("menu.html", 
                               title = {
                                   'main' :'편집 방법을 선택하세요',
                                   'sub' : '자동 무음제거와 효과음 키워드 추천 기능을 제공합니다.'
                                },
                               video = result['video']
                            )

# 무음 구간 편집 화면
@app.route('/rm_silence/<id>')
def rm_silence(id):
    from rm_silence import split
    result_path = os.path.join(UPLOAD_FOLDER, f'{id}.json')
    with open(result_path, "r", encoding='utf-8') as json_file:
        result = json.load(json_file)
    return render_template("rm_silence.html",
                           title = {
                                   'main' :'무음 영역 dB를 입력하세요',
                                   'sub' : '낮은 값일수록 무음영역이 늘어납니다'
                                },
                           video = result['video'],
                           audio = result['audio']
                        )

# topd : topdB입력 - 무음 제거 - 결정 :: fetch 방식
@app.route('/rm_silence/<id>', methods = ['GET', 'POST'])
def show_result(id):
    from rm_silence import split
    import numpy as np
    if request.method == 'POST':
        result_path = os.path.join(UPLOAD_FOLDER, f'{id}.json')
        with open(result_path, "r", encoding='utf-8') as json_file:
            result = json.load(json_file)
        tdb = request.get_json()['tdb']
        result['split'] = split(tdb, id)
        return jsonify({
                        "title" : {
                            'main' : 'Download',
                            'sub': f'{tdb} 값으로 무음구간이 삭제된 결과입니다'
                        },
                        "video" : result['video'],
                        "output" : result['split']
                    })

@app.route('/add_effect/<id>')
def add_effect(id):
    from rm_silence import split
    result_path = os.path.join(UPLOAD_FOLDER, f'{id}.json')
    with open(result_path, "r", encoding='utf-8') as json_file:
        result = json.load(json_file)
    return render_template("add_effect.html",
                           title = {
                               'main' : '효과음을 추가하세요',
                               'sub': '키워드를 선택한 후 우측의 효과음을 추가하세요.'
                            },
                           video = result['video'],
                           audio = result['audio'],
                           stt = result['stt'])

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