import moviepy.editor as mp
import librosa
import numpy as np
from file_path import get_path, get_src

def split(tdb, id):
    """ 오디오 무음 제거 후 해당 구간 타임스탬프 반환 """
    # get non mute intervals
    tdb = int(tdb)
    y, sr = librosa.load(get_path(f"{id}.wav"))
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

def export(id, video_name, data):
    """ 영상 무음 구간 제거 """
    tdb, sr, intervals = data
    clip = mp.VideoFileClip(get_path(video_name))
    clip_list = [clip.subclip(i[0]/int(sr), i[1]/int(sr)) for i in intervals['non_mute']]
    final_clip = mp.concatenate_videoclips(clip_list)
    try:
        path = get_path(f'{id}_{tdb}OUTPUT.mp4')
        final_clip.write_videofile(path,
                                   temp_audiofile='temp-audio.m4a',
                                   remove_temp=True,
                                   codec="libx264", audio_codec="aac")
        return {
            'status' : 'COMPLETE',
            'src' : get_src(path)
        }
    except:
        print('error occured in rm_silence export')
        return {
            'status' : 'FAIL',
            'src' : ''
        }