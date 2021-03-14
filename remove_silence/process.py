import moviepy.editor as mp
import librosa
import librosa.display
import numpy as np
import IPython.display
import matplotlib.pyplot as plt



UPLOAD_FOLDER = '/Users/gimjin-a/Desktop/noise/static/upload/'

# 1. Audio extract from video and load librosa
def extract_wav(name):
    wav_path = f"{UPLOAD_FOLDER}{name.split('.')[0]}.wav"
    wav_name = f"{name.split('.')[0]}.wav"
    clip = mp.VideoFileClip(f"{UPLOAD_FOLDER}{name}")
    clip.audio.write_audiofile(wav_path)
    return wav_path, wav_name

def plot(path, name):
    #저장경로, 이름 설정
    png_path = f"{UPLOAD_FOLDER}{name.split('.')[0]}.png"
    png_name = f"{name.split('.')[0]}.png"
    y, sr = librosa.load(path)
    librosa.display.waveplot(y, sr, alpha = 0.5)
    plt.xlabel("time(s)")
    plt.grid()
    plt.savefig(png_path)
    return png_name



"""
def get_non_mute(y, tdb):
    non_mute_intervals = librosa.effects.split(y, top_db=tdb)
    non_mute_audio = [y[i[0]:i[1]] for i in non_mute_intervals]
    non_mute_audio = np.concatenate(non_mute_audio)
    IPython.display.display(IPython.display.Audio(data=non_mute_audio, rate=sr))
    return non_mute_intervals, non_mute_audio

def remove_silence(sr, non_mute_intervals):
      non_mute_clips = [clips[index].subclip(i[0]/sr, i[1]/sr) for i in non_mute_intervals]
      final_clip = mp.concatenate_videoclips(non_mute_clips)
      final_clip.write_videofile(f"{OUTPUT}/{fnames[index].split('.')[0]}_OUTPUT.mp4")
      shutil.move(f"{INPUT}/{fnames[index]}", f"{COMPLETE}/{fnames[index]}")
      return final_clip, audio_inputs[:index] + audio_inputs[index+1:]

      top_db = get_num("top_db")
        
non_mute_intervals, non_mute_audio = get_non_mute(y, top_db)

final_clip, audio_inputs = remove_silence(sr, non_mute_intervals)"""