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

def get_non_mute(y, tdb):
    non_mute_intervals = librosa.effects.split(y, top_db=tdb)
    non_mute_audio = [y[i[0]:i[1]] for i in non_mute_intervals]
    non_mute_audio = np.concatenate(non_mute_audio)
    return non_mute_intervals, non_mute_audio

def remove_silence(sr, non_mute_intervals):
    non_mute_clips = [video.subclip(i[0]/sr, i[1]/sr) for i in non_mute_intervals] #video라고 명시해놓은 부분:input받은 영상 파일을 의미
    final_clip = mp.concatenate_videoclips(non_mute_clips)
    final_clip.write_videofile(f"{OUTPUT}/{fnames[index].split('.')[0]}_OUTPUT.mp4")
    shutil.move(f"{INPUT}/{fnames[index]}", f"{COMPLETE}/{fnames[index]}")
    return final_clip, audio_inputs[:index] + audio_inputs[index+1:]
"""def show_plt(signal)
    plt.figure(figsize=(8,4))
    librosa.display.waveplot(signal, 44100 , alpha = 0.5)
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