from app import celery

@celery.task
def file_processing(f):
    from process_upload import save_video, extract_audio
    data = { 'output': {}, 'split': { 'success': False }, 'effect': { 'success': False } } # init data
    data['video'], name, vid = save_video(f)
    data['audio'] = extract_audio(name, vid)
    save_data(vid, data)

@celery.task
def rm_silence_split(id, tdb):
    """ split by tdb """
    from process_rm_silence import split
    data = load_data(id)
    data['split'][tdb] = split(tdb, id)
    save_data(id, data)
    return data['split'][tdb]

@celery.task
def rm_silence_export(id, tdb):
    from process_rm_silence import export
    from sse_pubsub import publish_event
    data = load_data(id)
    data['output']['rm_silence'] = export(id, data['video']['name'], data['split'][tdb].values()) # status와 src 저장
    save_data(id, data)
    publish_event(data['output']['rm_silence']['src'])

@celery.task
def add_effect_stt(id):
    from process_stt import speech_to_text
    from file_data import load_data, save_data
    data = load_data(id)
    data['keyword_sentences'] = speech_to_text(data['audio']['gcs_uri'])
    save_data(id, data)

@celery.task
def add_effect_export(id):
    from process_add_effect import export
    from file_data import load_data, save_data
    from sse_pubsub import publish_event
    data = load_data(id)
    data['output']['add_effect'] = export(data['video']['name'], data['effect'].values()) # status와 src 저장
    save_data(id, data)
    publish_event(data['output']['add_effect']['src'])