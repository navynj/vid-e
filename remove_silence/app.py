import os, json
from flask import (Flask,
                   jsonify,
                   make_response,
                   render_template,
                   request,
                   url_for,
                   redirect,send_from_directory)
from celery import Celery


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'temp')
app.config['ALLOWED_EXTENSIONS'] = ['mp4']
app.config['JSON_AS_ASCII'] = False
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']


# 0. 홈화면 : 파일 업로드
@app.route('/')
def index():
    return render_template('index.html', 
                           title = {'main':'편집할 영상을 업로드하세요',
                                    'sub':'mp4 확장자를 지원합니다'})

# 1-1. 영상 목록 페이지 - 업로드 비디오 저장 및 오디오 추출 :: 기존 form.submit()방식
@app.route('/process', methods = ['POST'])
def upload():
    from file_processing import save_video, extract_wav, speech_to_text
    data = {'split':{}, 'effect':[]}
    if request.method == "POST":
        # 0. 비디오 업로드
        data['video'] = save_video(request.files['input-file'])
        id = data['video']['id']
        # 1. 오디오 추출
        data['audio'] = extract_wav(data['video']['name'])
        # 2. stt 변환
        data['keyword_sentences'] = speech_to_text(data['audio']['gcs_uri'])
        # 3. json 저장
        data_path = os.path.join(UPLOAD_FOLDER, id, f"{id}.json")
        with open(data_path, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        # 4. html 렌더링
        return render_template("process.html", 
                               title = {
                                   'main' :'편집 방법을 선택하세요',
                                   'sub' : '자동 무음제거와 효과음 키워드 추천 기능을 제공합니다.'
                                },
                               video = data['video']
                            )
# 1-2. 영상 페이지 - 목록 링크로 접근
@app.route('/<id>')
def show_menu(id):
    data_path = os.path.join(UPLOAD_FOLDER, id, f'{id}.json')
    with open(data_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return render_template("process.html", 
                            title = {
                                'main' :'편집 방법을 선택하세요',
                                'sub' : '자동 무음제거와 효과음 키워드 추천 기능을 제공합니다.'
                            },
                            video = data['video']
                        )
    

# 2-1. 무음 구간 편집 화면
@app.route('/<id>/rm_silence')
def rm_silence(id):
    from rm_silence import split
    data_path = os.path.join(UPLOAD_FOLDER, id, f'{id}.json')
    with open(data_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return render_template("rm_silence.html",
                           title = {
                                   'main' :'무음 영역 dB를 입력하세요',
                                   'sub' : '낮은 값일수록 무음영역이 늘어납니다'
                                },
                           video = data['video'],
                           audio = data['audio']
                        )

# 2-2. 무음 구간 편집 과정 : topdB입력 - 무음 제거 - 결정 :: fetch 방식
@app.route('/<id>/rm_silence', methods = ['GET', 'POST'])
def rm_silence_process(id):
    from rm_silence import split
    import numpy as np
    if request.method == 'POST':
        # 영상 data 불러오기
        data_path = os.path.join(UPLOAD_FOLDER, id, f'{id}.json')
        with open(data_path, "r", encoding='utf-8') as json_file:
            data = json.load(json_file)
        # top_dB 처리 - 오디오 저장 / 데이터 반환
        tdb = request.get_json()['tdb']
        data['split'][tdb] = split(tdb, id)
        # 영상 data 업데이트 후 필요 반환
        with open(data_path, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        return jsonify({
                        "title" : {
                            'main' : '무음제거 결과',
                            'sub': f'{tdb} 값으로 무음구간이 삭제되었습니다'
                        },
                        "video" : data['video'],
                        "split" : data['split'][tdb]
                    })

# 3-1. 효과음 추가 과정
@app.route('/<id>/add_effect')
def add_effect(id):
    from add_effect import get_effect_from
    # 키워드 문장 리스트
    data_path = os.path.join(UPLOAD_FOLDER, id, f'{id}.json')
    with open(data_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    # 효과음 라이브러리
    long_effect, short_effect = get_effect_from("sound-effect")

    return render_template("add_effect.html",
                           title = {
                               'main' : '효과음 추가하세요',
                               'sub': '키워드를 선택한 후 우측의 효과음을 추가하세요.'
                            },
                           video = data['video'],
                           long_effect = long_effect,
                           short_effect = short_effect,
                           audio = data['audio'],
                           keyword_sentences = data['keyword_sentences'])

@app.route('/<id>/add_effect', methods = ['GET', 'POST'])
def test(id):
    from add_effect import add_effect
    import numpy as np
    if request.method == 'POST':
        video_id = id
        audio_time = request.get_json()['audio_time']           
        effect_list = request.get_json()['audio_list']
        add_effect(video_id, audio_time, effect_list)
        return jsonify({"audio_time" : audio_time,
                         "audio_list" : effect_list})
     

# 처리 완료 파일 다운로드 :: 작업X, 기존 form submit 방식 예상
@app.route('/<id>/download', methods = ['GET','POST'])
def download():
    if request.method == "POST":
        from rm_silence import remove_silence
        output_info = json.loads(json.loads(jsonify(request.form['output_info']).data, encoding='utf-8'))
        file_info = json.loads(json.loads(jsonify(request.form['file_info']).data, encoding='utf-8'))
        removed_video = remove_silence(file_info['onlyname'], file_info['ext'],output_info['tdb'], output_info['sr'], output_info['nonmute_intervals'])
        return render_template("download.html", 
                               title = {'main':'Download',
                                        'sub': f'your video'},
                               output = {'src' : removed_video}
                            )

@app.route('/')
def archive():
    return render_template('archive.html', 
                           data = {})

if __name__ == '__main__':
    app.run(debug = True)
