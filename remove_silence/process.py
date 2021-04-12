import os, sys
import numpy as np
import moviepy.editor as mp
import librosa
from scipy.io.wavfile import write
from app import UPLOAD_FOLDER

GCS_BUCKET_NAME = "temp-bucket-stteff-0411"

def extract_wav(name):
    """ MoviePy로 오디오 추출 후 google cloud storge 업로드 """
    from google.cloud import storage
    # get video and audio
    audio_name = f"{name.split('.')[0]}.wav"
    audio_path = os.path.join(UPLOAD_FOLDER, audio_name)
    clip = mp.VideoFileClip(os.path.join(UPLOAD_FOLDER, name))
    clip.audio.write_audiofile(audio_path)
    # upload to google cloud storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(audio_name)
    blob.upload_from_filename(audio_path)
    return f"gs://{GCS_BUCKET_NAME}/{audio_name}", audio_path, audio_name

def speech_to_text(gcs_uri):
    """ google cloud speech 사용하여 음성 텍스트 변환(타임스탬프 포함) / 전체 텍스트 병합 """
    from google.cloud import speech
    from google.protobuf.json_format import MessageToJson
    # stt 변환
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # wav
        sample_rate_hertz=44100, # wav 샘플레이트  44100
        language_code="ko-KR", # 한국어
        audio_channel_count=2, # 스테레오 - 채널 수 2
        enable_word_time_offsets=True, # 타임스탬프 표시
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    print("Speech - Waiting for operation to complete...")
    response = operation.result(timeout=90)
    # 변환 결과 text 병합
    text=""
    for result in response.results:
        text += result.alternatives[0].transcript
    return MessageToJson(response._pb), text

def split(tdb, path):
    """ 오디오 무음 제거 후 해당 구간 타임스탬프 반환 """
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
    """ 영상 무음 구간 제거 """
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