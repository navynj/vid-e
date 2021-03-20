import numpy as np
import librosa
from scipy.io.wavfile import write
from app import UPLOAD_FOLDER

def get_non_mute(tdb, path):
    tdb = int(tdb)
    y, sr = librosa.load(f"{UPLOAD_FOLDER}{path}")
    non_mute_intervals = librosa.effects.split(y, top_db=tdb)
    non_mute_audio = [y[i[0]:i[1]] for i in non_mute_intervals]
    non_mute_audio = np.concatenate(non_mute_audio)
    write(f"{UPLOAD_FOLDER}{tdb}split.wav", sr, non_mute_audio)
    return tdb
