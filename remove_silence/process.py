import os, sys
import numpy as np
import moviepy.editor as mp
import librosa
from scipy.io.wavfile import write
from app import UPLOAD_FOLDER

GCS_BUCKET_NAME = "temp-bucket-stteff-0411"

def extract_wav(name):
    from google.cloud import storage
    # get video and audio
    file_name = f"{name.split('.')[0]}.wav"
    video = mp.VideoFileClip(os.path.join(UPLOAD_FOLDER, name))
    audio = audio.audio
    # upload to google cloud storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(wav_name)
    blob.upload_from_filename(file_name)
    return f"gs://{GCS_BUCKET_NAME}/{file_name}", file_url, file_name

def speech_to_text(gcs_uri):
    from google.cloud import speech
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # wav 형식
        sample_rate_hertz=44100, # 샘플레이트 맞춰주기
        language_code="ko-KR", # 한국어 코드
        audio_channel_count=2, # 스테레오라서? 채널 수 2
        enable_word_time_offsets=True, # 타임스탬프 표시!
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)
    return response.results

def get_clean_text(results):
    text = ""
    for result in results:
        text += result.alternatives[0].transcript

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