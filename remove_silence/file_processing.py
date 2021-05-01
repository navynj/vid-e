import os
import moviepy.editor as mp
# from scipy.io.wavfile import write
from werkzeug.utils import secure_filename
from app import UPLOAD_FOLDER

GCS_BUCKET_NAME = "temp-bucket-stteff-0411"

def save_video(f):
    file_name = secure_filename(f.filename)
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    f.save(file_path)
    video_data = {
        'name' : file_name,
        'id' : file_name.split('.')[0],
        'ext' : file_name.split('.')[1],
        'path' : file_path
    }
    return video_data
    
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
    audio_data = {
                'name' : audio_name,
                'path' : audio_path,
                'gcs_uri' : f"gs://{GCS_BUCKET_NAME}/{audio_name}"
        }
    return audio_data

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
    stt_data = {
        'transcript' : text,
        'json' : MessageToJson(response._pb)
    }
    return stt_data