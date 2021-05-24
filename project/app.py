from flask import (Flask,
                   jsonify,
                   request,
                   render_template,
                   redirect,
                   url_for,
                   Response)
from celery import Celery
import os, redis, glob, json
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
    from file_path import get_video_list
    vid_data = get_video_list()

    return render_template('status/index.html',
                            data = vid_data)

# upload : 비디오 업로드 / 오디오 추출
@app.route('/upload', methods=['POST'])
def upload():
    from tasks import file_processing
    if request.method == 'POST':
        f = request.files['video']
        fb = f.read()
        vid = file_processing(f.filename, fb)
        return redirect(url_for('video_process_status', id=vid))

# process : 비디오 개별 프로세스 진행상황
@app.route('/<id>')
def video_process_status(id):
    from file_data import load_data
    data = load_data(id)
    return render_template('status/video.html',
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
                           video = data['video'],
                           audio = data['audio'],
                           output = data['output']['rm_silence']['src'],
                           keyword_sentences = data['keyword_sentences'],
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

# archive
@app.route('/archive')
def archive():
    from file_path import get_video_list
    from file_data import load_data
    data = []
    v_data = []
    u_vid=[]
    u_vid_s=[]
    vid_data = get_video_list()
    for i in range(len(vid_data)):
        for id in vid_data[0]:
            data = load_data(id)
            v_data.append(data)

    print(vid_data)

    # for i in range(len(vid_data[0])):
    #     print("****************")
    #     print(v_data[i]['output'])


    for m in range(len(vid_data)+1):
        u_vid = v_data[m]['output']
        u_vid_s.append(u_vid)
    # print("****************")
    # print(u_vid_s)
    # print("****************")
    return render_template('status/archive.html',
                            data = vid_data,
                            # rm_silence = data['output']['rm_silence'],
                            # add_effect = data['output']['add_effect'])
                            update_vids = u_vid_s)
if __name__ == '__main__':
    app.run(debug = True)