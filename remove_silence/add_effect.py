import os
from app import UPLOAD_FOLDER

import ffmpeg

n_list = [5000, 10000, 150000, 20000]
e_list = ["MP_Woosh.mp3", "MP_Banana Peel Slip Zip.mp3", "MP_마법의 가루 - 2.mp3", "MP_Ta Da.mp3"]

num = len(n_list)

input_video = ffmpeg.input("./temp/Teacher_Moon.mp4")
added_audio = input_video.audio
for j in range(num):
    a = ffmpeg.input("./temp/" + e_list[j]).audio.filter('adelay', f"{n_list[j]}|{n_list[j]}")
    added_audio = ffmpeg.filter([added_audio, a], 'amix')

(
    ffmpeg
    .concat(input_video, added_audio, v=1, a=1)
    .output("./temp/OUTPUT_Teacher_Moon.mp4")
    .run(overwrite_output=True)
)