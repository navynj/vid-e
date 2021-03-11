import moviepy.editor as mp
import librosa
import librosa.display
import numpy as np
import IPython.display
import matplotlib.pyplot as plt

INPUT = "/static/upload/"
fnames = os.listdir(INPUT)

# 1. Audio extract from video
def extract_wav(fnames):
    clip = mp.VideoFileClip(f"{INPUT}/{fname}") for fname in fnames]
for i, clip in enumerate(clips):
  clip.audio.write_audiofile(audio_inputs[i])


def load_audio(audio_path):
  y, sr = librosa.core.load(audio_path, sr=None)
  return y, sr


"""def show_plt(signal)
    plt.figure(figsize=(8,4))
    librosa.display.waveplot(signal, 44100 , alpha = 0.5)
    plt.xlabel("time(s)")
    plt.grid()
    plt.show()
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