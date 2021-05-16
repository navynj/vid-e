import os
import ffmpeg
import pandas as pd
import json
import numpy as np
from app import UPLOAD_FOLDER

long_effect = [['긴_뾰롱_01.mp3', '긴_뾰롱_02.mp3'], # 휙
                ['긴_띠링_01.mp3', '긴_띠링_02.mp3'], # 띵
                ['긴_휙_01.mp3', '긴_휙_02.mp3'], # 뾱
                ['긴_별가루_01.mp3', '긴_별가루_02.mp3'] # 별가루~
                ]
short_effect = [['짧은_뿅_01.mp3', '짧은_뿅_02.mp3'], # 뿅
                ['짧은_띵_01.mp3', '짧은_띵_02.mp3'], # 띵
                ['짧은_휙_01.mp3', '짧은_휙_02.mp3'], # 휙
                ['짧은_별가루_01.mp3', '짧은_별가루_02.mp3'] # 별가루
                ]

def get_effect_from(root):
  # long_effect_file = [os.path.join(root, effect) for effect in long_effect]
  # short_effect_file = [os.path.join(root, effect) for effect in short_effect]
  long_effect_file, short_effect_file = long_effect, short_effect
  return long_effect_file, short_effect_file
  
def add_effect(video_id, key_start_time, effect_list):
  n_list = key_start_time
  e_list = effect_list
  video_name = video_id+".mp4"
  num = len(n_list)

  input_video = ffmpeg.input(os.path.join(UPLOAD_FOLDER, video_id, video_name))
  added_audio = input_video.audio

  for j in range(num):
      
      a = ffmpeg.input(os.path.join("/Users/gimjin-a/Desktop/github/summit/summit-capstone/remove_silence/static/sound-effect", e_list[j])).audio.filter('adelay', f"{n_list[j]}|{n_list[j]}")
      added_audio = ffmpeg.filter([added_audio, a], 'amix')

  (
      ffmpeg
      .concat(input_video, added_audio, v=1, a=1)
      .output(os.path.join(UPLOAD_FOLDER, video_id, video_id+"_OUTPUT.mp4"))
      .run(overwrite_output=True)
  )

  return None



# with open('ts_mask_smell_result.json') as json_file:
#     json_data = json.load(json_file)
    
#     for i in range(len(json_data["response"]["results"])):
#         json_object[i] = json_data["response"]["results"][i]
#         # print(i,"-----------------------------------------------------------------")
#         # print(json_object[i])

# word_set = pd.DataFrame()
# for i in range(len(json_data["response"]["results"])):
#     word_set = word_set.append(pd.DataFrame(json_object[i]['alternatives'][0]['words']), ignore_index=True)

# word_set = word_set.apply(lambda x: x.str.strip("s"), axis = 1)
# word_set = word_set.astype({'endTime': 'float', 'startTime':'float'})
# # word_set

# keyword_set = ['그렇게 하면', '그래 가지고', '또', '그러다 보니까', '이런 것처럼', '그럼', 
#                '그러다가', '그 다음에', '사실', '혹은', '그러니까', '그니까', '그러면', '그래서',
#                '그리고', '여기서', '마지막으로', '따라서', '때문에', '또한','게다가', '결국', 
#                '또는', '이러니까', '거기다가', '드디어', '대체로', '먼저', '어쨌든', '단', '근데', 
#                '반면에', '그래도', '대신에', '하지만', '그랬더니', '왜냐하면', 
#                '무슨 얘기냐면', '자', '즉', '예를 들면', '예를 들어','그런데']

# to_add_word_set = word_set['word'].isin(keyword_set)
# df_isin = word_set[to_add_word_set]

# ### 문장 시작 지점
# start_word = []
# start_time = []

# for i in range(len(df_sentence_all)):  
#   start_word.append(word_set.iloc[df_isin.index[i]-3,2])
#   start_time.append(word_set.iloc[df_isin.index[i]-3,1])

# df_start=list(zip(start_word, start_time))
# # print(df_start)

# ### 문장 마지막 지점
# end_word = []
# end_time = []

# for i in range(len(df_sentence_all)):  
#   end_word.append(word_set.iloc[df_isin.index[i]+3,2])
#   end_time.append(word_set.iloc[df_isin.index[i]+3,0])

# df_end=list(zip(end_word, end_time))
# # print(df_end)

# ### 키워드 시작, 끝 지점
# key_word = []
# key_start_time = []
# key_finish_time = []

# for i in range(len(df_sentence_all)):  
#   # 단어
#   key_word.append(word_set.iloc[df_isin.index[i],2])
#   # 시작 시간
#   key_start_time.append(int(word_set.iloc[df_isin.index[i],1]*1000))
#   # 끝 시간
#   key_finish_time.append(int(word_set.iloc[df_isin.index[i],0]*1000))

# df_key=list(zip(key_start_time, key_finish_time))



# n_list = key_start_time
# e_list = ["MP_Woosh.mp3", "MP_Banana Peel Slip Zip.mp3", "MP_마법의 가루 - 2.mp3", "MP_Ta Da.mp3"]

# num = len(n_list)

# input_video = ffmpeg.input("./temp/Teacher_Moon.mp4")
# added_audio = input_video.audio
# for j in range(num):
#     a = ffmpeg.input("./temp/" + e_list[j]).audio.filter('adelay', f"{n_list[j]}|{n_list[j]}")
#     added_audio = ffmpeg.filter([added_audio, a], 'amix')

# (
#     ffmpeg
#     .concat(input_video, added_audio, v=1, a=1)
#     .output("./temp/OUTPUT_Teacher_Moon.mp4")
#     .run(overwrite_output=True)
# )