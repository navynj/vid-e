import moviepy.editor as mp
import librosa
import numpy as np
from file_path import get_file_path, get_path, get_src

def split(tdb, id):
    """ 오디오 무음 제거 후 해당 구간 타임스탬프 반환 """
    # get non mute intervals
    tdb = int(tdb)
    y, sr = librosa.load(get_file_path(f"{id}.wav"))
    non_mute_intervals = librosa.effects.split(y, top_db=tdb)
    # get mute intervals
    temp = [t/sr for t in non_mute_intervals.flatten()]
    temp = np.insert(temp, 0, 0) # temp, 0번째 위치, 0 값
    mute_intervals = np.append(temp, len(y)/sr) # temp, 종료 시간값
    # return data
    split_data = {
        'tdb' : tdb,
        'sr' : sr,
        'intervals' : {
            'mute' : mute_intervals.tolist(),
            'non_mute' : non_mute_intervals.tolist()
        }
    }
    return split_data

def silence_export(id, video_name, data):
    """ 영상 무음 구간 제거 """
    tdb, sr, intervals = data
    clip = mp.VideoFileClip(get_file_path(video_name))
    clip_list = [clip.subclip(i[0]/int(sr), i[1]/int(sr)) for i in intervals['non_mute']]
    final_clip = mp.concatenate_videoclips(clip_list)
    try:
        video_name = f'rm{tdb}dB_{id}.mp4'
        path = get_path(id, f'rm{tdb}dB_{id}.mp4')
        print(path)
        final_clip.write_videofile(path,
                                   temp_audiofile='temp-audio.m4a',
                                   remove_temp=True,
                                   codec="libx264", audio_codec="aac")
        src = get_src(path)
        return {
            'rm_silence': {
                'status' : 'COMPLETE',
                'src' : src,
                'name' : video_name
            },
            'add_effect': {
                'status' : 'READY',
                'src' : '',
                'msg' : 'exporting...'
            }
        }
    except Exception as e:
        print(e)
        return {
            'rm_silence': {
                'status' : 'READY',
                'src' : ''
            },
            'add_effect': {
                'status' : 'DISABLED',
                'src' : ''
            }
        }