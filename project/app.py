from flask import (Flask,
                   jsonify,
                   request,
                   render_template,
                   redirect,
                   url_for,
                   Response)
from celery import Celery
import os, redis

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)

red = redis.StrictRedis()

UPLOAD_FOLDER = os.path.join(app.static_folder, 'storage')


# home
@app.route('/')
def index():
    return render_template('status/index.html')


# upload : 비디오 업로드 / 오디오 추출
@app.route('/upload', methods=['POST'])
def upload():
    from tasks import file_processing#, add_effect_stt
    if request.method == 'POST':
        vid = file_processing.delay(request.files['video'])
        return redirect(url_for('process', id=vid))

# process : 비디오 개별 프로세스 진행상황
@app.route('/<id>')
def video_process_status(id):
    from file_data import load_data
    data = load_data(id)
    return render_template('status/video.html',
                           video = data['video'],
                           rm_silence = data['output']['rm_silence'],
                           add_effect = data['output']['add_effect'])

# event stream : 프로세스 완료 
@app.route('/export_status')
def get_event():
    from sse_pubsub import subscribe_event
    return Response(subscribe_event(), mimetype="text/event-stream")

# rm_silence : 무음 제거
@app.route('/<id>/rm_silence')
def rm_silence_process(id):
    from file_data import load_data
    os.makedirs(os.path.join(UPLOAD_FOLDER, id, 'split'), exist_ok=True)
    data = load_data(id)
    return render_template('process/rm_silence.html',
                           video = data['video'],
                           audio = data['audio'],
                           output = data['output'])

@app.route('/<id>/rm_silence_split', methods=['POST'])
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
        return jsonify({'sr': data['sr'],
                        'intervals': data['intervals']['mute']})

@app.route('/<id>/rm_silence_export', methods=['POST'])
def rm_silence_export(id):
    from tasks import rm_silence_export
    if request.method == 'POST':        
        tdb = request.form['tdb']
        print('■■■■■■ before export')
        rm_silence_export.delay(id, tdb)
        print('■■■■■■ after export')
        return redirect(url_for('video_process_status', id=id))
        


# add_effect : 효과음 추가
@app.route('/<id>/add_effect')
def add_effect_process(id):
    from file_data import load_data
    data = load_data(id)
    return render_template('process/add_effect.html',
                           video = data['video'],
                           audio = data['audio'],
                           keyword_sentences = data['keyword_sentences'])
    
@app.route('/<id>/add_effect', methods=['POST'])
def add_effect_export(id):
    from tasks import add_effect_export
    if request.method == 'POST':
        data, vid = add_effect.delay(id)
        save_data(data['id'], data)
    return render_template('process/add_effect.html')


# archive
@app.route('/archive')
def archive():
    return render_template('status/archive.html')

if __name__ == '__main__':
    app.run(debug = True)