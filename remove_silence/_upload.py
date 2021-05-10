from werkzeug.utils import secure_filename
from path import get_path, get_src

GCS_BUCKET_NAME = "temp-bucket-stteff-0411"

def save_video(f):
    """ static 폴더에 비디오 업로드 """
    file_name = secure_filename(f.filename)
    vid, ext = file_name.split('.')
    file_path = get_path(file_name, dir_exits=False)
    f.save(file_path)
    video_data = {
        'name' : file_name,
        'id' : vid,
        'ext' : ext,
        'src' : get_src(file_path)
    }
    return video_data, file_name, vid

def extract_audio(video_name, vid):
    """ MoviePy 오디오 추출  -->  Google Cloud Storge 업로드 """
    from google.cloud import storage
    # extract audio from video
    audio_name = f"{vid}.wav"
    audio_path = get_path(audio_name)
    clip = mp.VideoFileClip(get_path(video_name))
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
                'src' : get_src(audio_path),
                'gcs_uri' : f"gs://{GCS_BUCKET_NAME}/{audio_name}"
        }
    return audio_data