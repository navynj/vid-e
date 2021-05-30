from flask import (Flask,
                   jsonify,
                   request,
                   render_template,
                   redirect,
                   url_for,
                   Response)
from celery import Celery
import os, redis, glob
import numpy as np

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)

red = redis.StrictRedis()

UPLOAD_FOLDER = os.path.join(app.static_folder, 'storage')
EFFECT_FOLDER = os.path.join(app.static_folder, 'lib', 'sound_effect')

# home
@app.route('/')
def index():
    from file_data import load_data_list
    video_list = load_data_list('video')
    output_list = load_data_list('output')
    return render_template('status/index.html',
                           title = 'HOME',
                           video = video_list,
                           output = output_list,
                           len = len)

# upload : 비디오 업로드 / 오디오 추출
@app.route('/upload', methods=['POST'])
def upload():
    from tasks import file_processing
    if request.method == 'POST':
        f = request.files['video']
        vid = file_processing(f.filename, f.read())
        return redirect(url_for('video_process_status', id=vid))

# process : 비디오 개별 프로세스 진행상황
@app.route('/<id>')
def video_process_status(id):
    from file_data import load_data
    data = load_data(id)
    return render_template('status/video.html',
                           title = f'{id}',
                           video = data['video'],
                           rm_silence = data['output']['rm_silence'],
                           add_effect = data['output']['add_effect'])

# event : 프로세스 완료 
@app.route('/export_status')
def get_event():
    from sse_pubsub import subscribe_event
    return Response(subscribe_event(), mimetype="text/event-stream")

# rm_silence : 무음 제거 진행 페이지
@app.route('/<id>/rm_silence')
def rm_silence_process(id):
    from file_data import load_data
    os.makedirs(os.path.join(UPLOAD_FOLDER, id, 'split'), exist_ok=True)
    data = load_data(id)
    return render_template('process/rm_silence.html',
                           title = 'Remove silence',
                           video = data['video'],
                           audio = data['audio'],
                           output = data['output'])
    
# rm_silence : 무음구간 split
@app.route('/<id>/rm_silence/split', methods=['POST'])
def rm_silence_split(id):
    from file_data import temp_exists, load_temp
    from tasks import rm_silence_split
    from celery import chain
    from celery.result import AsyncResult
    if request.method == 'POST':
        tdb = request.get_json()['tdb']
        if temp_exists(id, 'split', f'{tdb}.json'):
            data = load_temp(id, 'split', f'{tdb}.json')
        else:
            result = rm_silence_split.delay(id, tdb)
            data = AsyncResult(id=result.id, app=celery).get()
        return jsonify({'intervals': data['intervals']['mute']})
    
# rm_silence : 무음 제거 결과 export
@app.route('/<id>/rm_silence/export', methods=['POST'])
def rm_silence_export(id):
    from tasks import rm_silence_export
    import time
    if request.method == 'POST':        
        tdb = request.form['tdb']
        rm_silence_export.delay(id, tdb)
        time.sleep(0.1)
    return redirect(url_for('video_process_status', id=id))

# add_effect : 효과음 추가 진행 페이지
@app.route('/<id>/add_effect')
def add_effect_process(id):
    from file_data import load_data
    from process_add_effect import effect_data, get_effect_src
    data = load_data(id)
    return render_template('process/add_effect.html',
                           title = 'Add effect',
                           video = data['video'],
                           audio = data['audio'],
                           output = data['output']['rm_silence']['src'],
                           sentence_text = list(map(lambda x:x["text"], data['keyword_sentences'])),
                           sentences_time = list(map(lambda x:x["time"], data['keyword_sentences'])),
                           effect_data = effect_data,
                           effect_src = get_effect_src(),
                           enumerate=enumerate)

# add_effect : 효과음 추가 결과 export
@app.route('/<id>/add_effect/export', methods=['GET', 'POST'])
def add_effect_export(id):
    from tasks import add_effect_export
    import time
    if request.method == 'POST':
        effect_list = request.get_json()['effect_list']           
        time_list = request.get_json()['time_list']
        add_effect_export.delay(id, effect_list, time_list)
        time.sleep(0.1)
    return redirect(url_for('video_process_status', id=id))

# add_effect : 효과음 추가 결과 export
@app.route('/<id>/shortcut', methods=['GET', 'POST'])
def shortcut(id):
    from tasks import stt_process
    from file_data import load_data, save_data
    data = load_data(id)
    if request.method == 'POST':
        output = request.get_json()["output"]
        skip = request.get_json()["skip"]
        data['output'] = output
        save_data(id, data)
        if skip:
            stt_process.delay(id, audio=data['audio'])
    return jsonify({"rmStatus" : output["rm_silence"]["status"],
                    "addStatus" : output["add_effect"]["status"],
                    "msg" : output["add_effect"]["msg"]})

# archive
@app.route('/archive')
def archive():
    from file_data import load_data_list
    video_list = load_data_list('video')
    output_list = load_data_list('output')
    return render_template('status/archive.html',
                            title = 'ARCHIVE',
                            video = video_list,
                            output = output_list)
    
if __name__ == '__main__':
    app.run(debug = True)