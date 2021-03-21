import numpy as np
import moviepy.editor as mp
import librosa
from scipy.io.wavfile import write
from app import UPLOAD_FOLDER

def extract_wav(name):
    wav_path = f"{UPLOAD_FOLDER}{name.split('.')[0]}.wav"
    wav_name = f"{name.split('.')[0]}.wav"
    clip = mp.VideoFileClip(f"{UPLOAD_FOLDER}{name}")
    clip.audio.write_audiofile(wav_path)
    return wav_path, wav_name

def split(tdb, path):
    tdb = int(tdb)
    y, sr = librosa.load(f"{UPLOAD_FOLDER}{path}")
    non_mute_intervals = librosa.effects.split(y, top_db=tdb)
    non_mute_audio = [y[i[0]:i[1]] for i in non_mute_intervals]
    non_mute_audio = np.concatenate(non_mute_audio)
    write(f"{UPLOAD_FOLDER}{tdb}split.wav", sr, non_mute_audio)
    return f"{tdb}split.wav", sr, non_mute_intervals

def remove_silence(sr, non_mute_intervals):
    try:
        output = f"{path.split('.')[0]}.mp4"
        clip = mp.VideoFileClip(f"{UPLOAD_FOLDER}{path.split('.')[0]}.mp4")
        non_mute_clips = [clip.subclip(i[0]/sr, i[1]/sr) for i in non_mute_intervals]
        final_clip = mp.concatenate_videoclips(non_mute_clips)
        final_clip.write_videofile(f"{UPLOAD_FOLDER}{path.split('.')[0]}_OUTPUT.mp4",
                                    temp_audiofile='temp-audio.m4a',
                                    remove_temp=True,
                                    codec="libx264", audio_codec="aac")
        return os.path.join(UPLOAD_FOLDER, output)
    except IOError :
        sys.exit()