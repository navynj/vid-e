from app import celery

from process_upload import save_video, extract_audio
from process_stt import speech_to_text
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
    data['audio'] = extract_audio(name, vid)
    data['split'] = {}
    # data['keyword_sentences'] = speech_to_text(data['audio']['gcs_uri'])
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
    save_data(id, data)
    publish_event(data['output']['rm_silence']['src'])
    # stt

@celery.task
def add_effect_export(id, effect_list, time_list):
    # start
    data = load_data(id)
    data['output']['add_effect']['status'] = 'PROCESS'
    save_data(id, data)
    # complete 
    data['output']['add_effect'] = effect_export(id, effect_list, time_list) # status와 src 저장
    save_data(id, data)
    publish_event(data['output']['add_effect']['src'])