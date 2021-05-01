import pandas as pd
import json
import numpy as np

with open('ts_mask_smell_result.json') as json_file:
    json_data = json.load(json_file)
    
    for i in range(len(json_data["response"]["results"])):
        json_object[i] = json_data["response"]["results"][i]
        print(i,"-----------------------------------------------------------------")
        print(json_object[i])


word_set = pd.DataFrame()
for i in range(len(json_data["response"]["results"])):
    word_set = word_set.append(pd.DataFrame(json_object[i]['alternatives'][0]['words']), ignore_index=True)

word_set = word_set.apply(lambda x: x.str.strip("s"), axis = 1)
word_set = word_set.astype({'endTime': 'float', 'startTime':'float'})
word_set


keyword_set = ['그렇게 하면', '그래 가지고', '또', '그러다 보니까', '이런 것처럼', '그럼', 
               '그러다가', '그 다음에', '사실', '혹은', '그러니까', '그니까', '그러면', '그래서',
               '그리고', '여기서', '마지막으로', '따라서', '때문에', '또한','게다가', '결국', 
               '또는', '이러니까', '거기다가', '드디어', '대체로', '먼저', '어쨌든', '단', '근데', 
               '반면에', '그래도', '대신에', '하지만', '그랬더니', '왜냐하면', 
               '무슨 얘기냐면', '자', '즉', '예를 들면', '예를 들어','그런데']


to_add_word_set = word_set['word'].isin(keyword_set)
df_isin = word_set[to_add_word_set]
df_isin

list_from_df = df_isin.values.tolist()
list_from_df

"""수도 있습니다 그런데 생각보다 많은  
되면서 마스크 때문에 자신의 입냄새를
나는 걸까요 그리고 마스크를 있으면
때문이라고 생각합니다 그래서 이 냄새가"""

df_sentence_all = []
for i in range(len(df_isin)):
    df_sentence = []
    for j in range(3):
        df_sentence.append(word_set.iloc[df_isin.index[i]-3+j,2])
        
    df_sentence.append(word_set.iloc[df_isin.index[i],2])
    
    for j in range(3):
        df_sentence.append(word_set.iloc[df_isin.index[i]+1+j,2])
    
    df_sentence_all.append(df_sentence)
    
df_sentence_all
#각 리스트끼리 컨캣시키는게 나으려나?