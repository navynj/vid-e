import moviepy.editor as mp

UPLOAD_FOLDER = '/Users/gimjin-a/Desktop/noise/static/upload/'

# 1. Audio extract from video and load librosa
def extract_wav(name):
    wav_path = f"{UPLOAD_FOLDER}{name.split('.')[0]}.wav"
    wav_name = f"{name.split('.')[0]}.wav"
    clip = mp.VideoFileClip(f"{UPLOAD_FOLDER}{name}")
    clip.audio.write_audiofile(wav_path)
    return wav_path, wav_name

