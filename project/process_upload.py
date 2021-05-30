from werkzeug.utils import secure_filename
from file_path import get_file_path, get_src
from google.cloud import storage
import moviepy.editor as mp
import datetime

GCS_BUCKET_NAME = "temp-bucket-stteff-0411"

def save_video(fname, fb):
    """ static 폴더에 비디오 업로드 """
    now = datetime.datetime.now()
    file_name = secure_filename(fname)
    vid, ext = file_name.split('.')
    file_path = get_file_path(file_name, dir_exits=False)
    with open(file_path, "wb") as video:
        video.write(fb)
    video_data = {
        'name' : file_name,
        'id' : vid,
        'ext' : ext,
        'src' : get_src(file_path),
        'date' : now.strftime("%Y. %m. %d"),
        'time' : now.strftime("%H : %M")
    }
    return video_data, file_name, vid

def extract_audio(video_name, vid):
    """ MoviePy 오디오 추출 """
    audio_name = f"{vid}.wav"
    audio_path = get_file_path(audio_name)
    clip = mp.VideoFileClip(get_file_path(video_name))
    clip.audio.write_audiofile(audio_path)
    audio_data = {
        'name' : audio_name,
        'src' : get_src(audio_path),
        'gcs_uri' : f"gs://{GCS_BUCKET_NAME}/{audio_name}"
    }
    return audio_data