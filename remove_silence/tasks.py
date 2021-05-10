from app import celery
from _data import load_data, save_data


@celery.task
def file_processing(f):
    from _upload import save_video, extract_audio
    data = {'split':{'success':False}, 'effect':{'success':False}}
    data['video'], name, vid = save_video(f)
    data['audio'] = extract_audio(name, vid)
    save_data(vid, data)

@celery.task
def rm_silence_split(id, tdb):
    """ split by tdb """
    from _rm_silence import split
    data = load_data(id)
    data['split'][tdb] = split(tdb, id)
    save_data(id, data)

@celery.task
def rm_silence_export(id, tdb):
    from _rm_silence import export
    data = load_data(id)
    data['output'] = {}
    data['output']['rm_silence'] = export(id, data['video']['name'], data['split'][tdb].values())
    save_data(id, data)

@celery.task
def add_effect_stt(id):
    from _stt import speech_to_text
    from _data_processing import load_data, save_data
    data = load_data(id)
    data['keyword_sentences'] = speech_to_text(data['audio']['gcs_uri'])
    save_data(id, data)

@celery.task
def add_effect_export(id,):
    from _add_effect import export
    data = load_data(id)
    data['output']['add_effect'] = export(data['video']['name'], data['effect'].values())
    save_data(id, data)