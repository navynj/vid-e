import os
import ffmpeg
import pandas as pd
import json
import numpy as np
from app import UPLOAD_FOLDER

long_effect = [['long1-1.mp3', 'long1-2.mp3'], # 휙
                ['whoosh1.mp3', 'whoosh2.mp3'], # 띵
                ['whoosh1.mp3', 'whoosh2.mp3'], # 뾱
                ['whoosh1.mp3', 'whoosh2.mp3'] # 별가루~
                ]
short_effect = [['short1.mp3', 'short2.mp3'], # 휙
                ['whoosh1.mp3', 'whoosh2.mp3'], # 띵
                ['whoosh1.mp3', 'whoosh2.mp3'], # 뾱
                ['whoosh1.mp3', 'whoosh2.mp3'] # 별가루~
                ]

def get_effect_list():
    return long_effect, short_effect

def export(video_name, data):
  n_list, e_list = data
  num = len(n_list)
  input_video = ffmpeg.input(os.path.join(UPLOAD_FOLDER, video_name))
  added_audio = input_video.audio
  for j in range(num):
      a = ffmpeg.input(os.path.join(UPLOAD_FOLDER, e_list[j]).audio.filter('adelay', f"{n_list[j]}|{n_list[j]}"))
      added_audio = ffmpeg.filter([added_audio, a], 'amix')

  (
      ffmpeg
      .concat(input_video, added_audio, v=1, a=1)
      .output(os.path.join(UPLOAD_FOLDER, video_name))
      .run(overwrite_output=True)
  )
  return os.path.join(UPLOAD_FOLDER, video_name)