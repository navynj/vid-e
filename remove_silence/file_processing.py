import os
import moviepy.editor as mp
import numpy as np
import pandas as pd
from werkzeug.utils import secure_filename
from app import UPLOAD_FOLDER

GCS_BUCKET_NAME = "temp-bucket-stteff-0411"
KEYWORD_SET = ['그렇게 하면', '그=래 가지고', '또', '그러다 보니까', '이런 것처럼', '그럼', 
               '그러다가', '그 다음에', '사실', '혹은', '그러니까', '그니까', '그러면', '그래서',
               '그리고', '여기서', '마지막으로', '따라서', '때문에', '또한','게다가', '결국', 
               '또는', '이러니까', '거기다가', '드디어', '대체로', '먼저', '어쨌든', '단', '근데', 
               '반면에', '그래도', '대신에', '하지만', '그랬더니', '왜냐하면', 
               '무슨 얘기냐면', '자', '즉', '예를 들면', '예를 들어','그런데', '반대로', '그로 인해', '쉽게 말해',
              '이렇게', '물론', '정말로', '절대', '정말', '오로지', '엄청나게', '제일', '결국은', '꼭', '벌써',
               '심지어', '모든', '진짜', '열심히', '실제', '실제로', '거의', '훨씬', '특히', '특히나', '오히려', '바로', 
               '반드시', '어느', '이미', '아마도', '많이', '너무', '주로', '어떻게', '아주', '매우', '몹시', '엄청(난)', 
               '되게', '굉장히', '대단히', '상당히', '무진장', '분명', '분명히', '그런', '혹시', '딱', '막', '계속', '더', 
               '어떤', '무조건', '충분히', '강력', '강력히', '그', '그만큼', '최소', '최대']


def save_video(f):
    """ 영상 정보 반환 """
    file_name = secure_filename(f.filename)
    id = file_name.split('.')[0]
    file_dir = os.path.join(UPLOAD_FOLDER, id)
    file_path = os.path.join(file_dir, file_name)
    if os.path.isdir(file_dir):
        os.mkdir(file_dir)
    f.save(file_path)
    video_data = {
        'name' : file_name,
        'id' : id,
        'ext' : file_name.split('.')[1],
        'path' : file_path.split('static/')[-1]
    }
    return video_data
    
    
def extract_wav(name):
    """ MoviePy : 오디오 추출 후 google cloud storge 업로드 """
    from google.cloud import storage
    # get video and audio
    id = video_name.split('.')[0]
    audio_name = f"{name.split('.')[0]}.wav"
    audio_path = os.path.join(UPLOAD_FOLDER, audio_name)
    clip = mp.VideoFileClip(os.path.join(UPLOAD_FOLDER, name))
    clip.audio.write_audiofile(audio_path)
    # upload to google cloud storage
    print("Storage - Uploading..")
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(audio_name)
    blob.upload_from_filename(audio_path)
    print("Storage - Done.")
    audio_data = {
                'name' : audio_name,
                'path' : audio_path,
                'gcs_uri' : f"gs://{GCS_BUCKET_NAME}/{audio_name}"
        }
    return audio_data



def speech_to_text(gcs_uri):
    """ Google Cloud Speech : 음성 텍스트 변환(타임스탬프 포함) / 전체 텍스트 병합 """
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
    print("Speech - Done.")

    # 키워드 필터링, 타임스탬프 정보 추가
    print("Keyword - filtering..")
    return filter_keyword(response.results)

def filter_keyword(results):
    """ Keyword_set : 숫자/키워드 포함 문장(앞뒤 3단어), 시간(문장 시작끝, 키워드 시작끝) 정보 추출 """
    # 1. word --> dict --> DataFrame
    word_list = []
    for result in results:
        for word_info in result.alternatives[0].words:
            word_list.append({
                'end_time' : word_info.end_time.total_seconds() * 1000.0, # to milliseconds
                'start_time' : word_info.start_time.total_seconds() * 1000.0, # to milliseconds
                'word' :  word_info.word,
                'keyword' : False
            })
    word_df = pd.DataFrame(word_list)
    
    # 2. 키워드 단어 저장 (숫자 / 키워드 포함)
    is_digit = word_df.word.str[0].str.isdigit()
    in_keyword = word_df['word'].isin(KEYWORD_SET)
    mask = is_digit | in_keyword
    word_df['keyword'] = np.where(mask, True,  word_df.word)
    keyword_df = word_df[word_df['keyword']==True]
    
    # 3. 키워드별 정보 저장 (시간 : 문장시작끝/키워드시작끝, 텍스트 : 앞/키워드/뒤)
    sentences_data = []
    end, start, word = 0, 1, 2
    scope = 3 # 앞뒤로 몇 단어까지 포함할지
    for i in range(len(keyword_df)):
        sentence = {}
        # index 설정 (prev, keyword, next)
        key_index = keyword_df.index[i]
        prev_index = key_index - scope
        next_index = key_index + scope + 1
        if prev_index < 0:
            prev_index = 0
        if next_index >= len(word_df):
            next_index = len(word_df)-1

        # 시간 변수 (start, end 튜플)
        sentence_time = (word_df.iloc[prev_index, start], word_df.iloc[next_index, end])
        keyword_time = (word_df.iloc[key_index, start], word_df.iloc[key_index, end])
        # 텍스트 변수 (prev, keyword, next 각각)
        prev_text = word_df.iloc[prev_index : key_index, word]
        keyword_text = word_df.iloc[key_index, word]
        next_text = word_df.iloc[key_index+1 : next_index, word]

        # 시간 data 저장
        sentence['time'] = {'sentence':{}, 'keyword':{}}
        sentence['time']['sentence']['start'] = int(sentence_time[0])
        sentence['time']['sentence']['end'] = int(sentence_time[1])
        sentence['time']['keyword']['start'] = int(keyword_time[0])
        sentence['time']['keyword']['end'] = int(keyword_time[1])
        # 텍스트 data 저장
        sentence['text'] = {}
        sentence['text']['prev'] = ' '.join(prev_text.apply(str).values)
        sentence['text']['keyword'] = keyword_text
        sentence['text']['next'] = ' '.join(next_text.apply(str).values)
        sentences_data.append(sentence)
    return sentences_data
