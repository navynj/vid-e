import os, sys
import numpy as np
import moviepy.editor as mp
import librosa
from scipy.io.wavfile import write
from app import UPLOAD_FOLDER

def extract_wav(name):
    wav_path = os.path.join(UPLOAD_FOLDER, f"{name.split('.')[0]}.wav")
    wav_name = f"{name.split('.')[0]}.wav"
    clip = mp.VideoFileClip(os.path.join(UPLOAD_FOLDER, name))
    clip.audio.write_audiofile(wav_path)
    return wav_path, wav_name

def split(tdb, path):
    # get non mute intervals
    tdb = int(tdb)
    y, sr = librosa.load(os.path.join(UPLOAD_FOLDER, path))  
    non_mute_intervals = librosa.effects.split(y, top_db=tdb)
    # get mute intervals
    temp = non_mute_intervals.flatten()
    temp = np.insert(temp, 0, 0)
    mute_intervals = np.append(temp, len(y))
    # split audio
    non_mute_audio = [y[i[0]:i[1]] for i in non_mute_intervals]
    non_mute_audio = np.concatenate(non_mute_audio)
    output_path = os.path.join(UPLOAD_FOLDER, "split.wav")
    write(output_path, sr, non_mute_audio)
    return output_path, sr, non_mute_intervals, mute_intervals

def remove_silence(fname, ext, tdb, sr, non_mute_intervals):
    try:
        input_path = os.path.join(UPLOAD_FOLDER, f'{fname}.{ext}')
        output_path = os.path.join(UPLOAD_FOLDER, f'{fname}_{tdb}OUTPUT.mp4')
        clip = mp.VideoFileClip(input_path)
        non_mute_clips = [clip.subclip(i[0]/int(sr), i[1]/int(sr)) for i in non_mute_intervals]
        final_clip = mp.concatenate_videoclips(non_mute_clips)
        final_clip.write_videofile(output_path,
                                    temp_audiofile='temp-audio.m4a',
                                    remove_temp=True,
                                    codec="libx264", audio_codec="aac")
        return output_path
    except IOError :
        sys.exit()