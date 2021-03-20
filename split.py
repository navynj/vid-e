import numpy as np
import librosa
from scipy.io.wavfile import write
import moviepy.editor as mp
import sys

UPLOAD_FOLDER = '/Users/gimjin-a/Desktop/flask_upload/static/uploads/'

path = 'front_vs_back.wav'
def get_non_mute(tdb):
    tdb = int(tdb)
    y, sr = librosa.load(f"{UPLOAD_FOLDER}{path}")
    non_mute_intervals = librosa.effects.split(y, top_db=tdb)
    non_mute_audio = [y[i[0]:i[1]] for i in non_mute_intervals]
    non_mute_audio = np.concatenate(non_mute_audio)
    write(f"{UPLOAD_FOLDER}{tdb}_split.wav", sr, non_mute_audio)
    return sr, non_mute_intervals, tdb


def remove_silence(sr, non_mute_intervals):
    try:
        clip = mp.VideoFileClip(f"{UPLOAD_FOLDER}{path.split('.')[0]}.mp4")
        non_mute_clips = [clip.subclip(i[0]/sr, i[1]/sr) for i in non_mute_intervals]
        final_clip = mp.concatenate_videoclips(non_mute_clips)
        final_clip.write_videofile(f"{UPLOAD_FOLDER}{path.split('.')[0]}_OUTPUT.mp4",
                                    temp_audiofile='temp-audio.m4a',
                                    remove_temp=True,
                                    codec="libx264", audio_codec="aac")
    except IOError :
        sys.exit()
      #return final_clip