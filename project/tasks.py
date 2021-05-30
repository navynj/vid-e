from app import celery

from process_upload import save_video, extract_audio
from process_stt import upload_audio, speech_to_text
from process_rm_silence import split, silence_export
from process_add_effect import effect_export
from sse_pubsub import publish_event
from file_data import load_data, save_data, load_temp, save_temp, remove_temp

# @celery.task
def file_processing(fname, fb):
    data = { 'output': {
                'rm_silence': {
                    'status': 'READY',
                    'src': ''
                }, 
                'add_effect': {
                    'status': 'DISABLED',
                    'src': ''
                }
            }
        }
    data['video'], name, vid = save_video(fname, fb)
    data['audio'] = extract_audio(vid, name, f"{vid}.wav")
    data['split'] = {}
    save_data(vid, data)
    return vid
    
@celery.task
def rm_silence_split(id, tdb):
    """ split by tdb """
    print(f'■■■■ {tdb}db split start...')
    data = load_data(id)
    output = split(tdb, id)
    save_temp(id, 'split', f"{tdb}.json", output)
    print(f'■■■■ {tdb}db split done.')
    return output

@celery.task
def rm_silence_export(id, tdb):
    print('■■■■■■ in export : rm_silence')
    # start
    data = load_data(id)
    data['split'] = load_temp(id, 'split', f'{tdb}.json')
    data['output']['rm_silence']['status'] = 'PROCESS'
    save_data(id, data)
    remove_temp(id, 'split')
    # complete
    data['output'] = silence_export(id, data['video']['name'], data['split'].values()) # status와 src 저장
    data['output']['add_effect']['status'] = 'PROCESS'
    data['output']['add_effect']['msg'] = 'loading..'
    save_data(id, data)
    publish_event('COMPLETE', '{"src": "' + str(data['output']['rm_silence']['src']) + '"}')
    # stt
    stt_process(id, data['output']['rm_silence']['name'])
    
@celery.task
def stt_process(id, video=None, audio=None):
    print("■■■■■■■■ in stt")
    shortcut = "true"
    if not audio:
        audio_name = f"{video.split('.')[0]}.wav"
        audio = extract_audio(id, video, audio_name)
        shortcut = "false"
    upload_audio(audio['name'], audio['path'])
    data = load_data(id)
    data['keyword_sentences'] = speech_to_text(audio['gcs_uri'])
    data['output']['add_effect']['status'] = 'READY'
    data['output']['add_effect']['msg'] = ''
    save_data(id, data)
    publish_event('READY', '{"shortcut": "' + str(shortcut) + '"}')

@celery.task
def add_effect_export(id, effect_list, time_list):
    # start
    data = load_data(id)
    data['output']['add_effect']['status'] = 'PROCESS'
    data['output']['add_effect']['msg'] = 'loading..'
    save_data(id, data)
    # complete 
    if data['output']['rm_silence']['src']:
        video = data['output']['rm_silence']['name']
    else:
        video = data['video']['name']
    data['output']['add_effect'] = effect_export(id, video, effect_list, time_list) # status와 src 저장
    save_data(id, data)
    publish_event('COMPLETE', '{"src": "' + str(data['output']['add_effect']['src']) + '"}')