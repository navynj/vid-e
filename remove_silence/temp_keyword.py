import pandas as pd
import json
import numpy as np

with open('ts_mask_smell_result.json') as json_file:
    json_data = json.load(json_file)
    
    for i in range(len(json_data["response"]["results"])):
        json_object[i] = json_data["response"]["results"][i]
        print(i,"-----------------------------------------------------------------")
        print(json_object[i])

#결과 데이트프레임으로 저장
word_set = pd.DataFrame()
for i in range(len(json_data["response"]["results"])):
    word_set = word_set.append(pd.DataFrame(json_object[i]['alternatives'][0]['words']), ignore_index=True)
#초에서 s 빼주기
word_set = word_set.apply(lambda x: x.str.strip("s"), axis = 1)
word_set = word_set.astype({'endTime': 'float', 'startTime':'float'})
word_set

#키워드 셋
keyword_set = ['그렇게 하면', '그래 가지고', '또', '그러다 보니까', '이런 것처럼', '그럼', 
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


#키워드에 해당하는 값 추출 후 저장 
#숫자 부분 추출!
is_digit = word_set.word.str[0].str.isdigit()
in_keyword = word_set['word'].isin(keyword_set)
mask = is_digit | in_keyword
word_set['O/X'] = np.where(mask, "keyword",  word_set.word)

df_isin = word_set[word_set['O/X']=="keyword"]

#list_from_df = df_isin.values.tolist()

# 해당 인덱스 +3 -3 문장들 붙여서 이중리스트로 저장
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

#각 문장 list to dict 후 json으로 저장
sentence_all_dict = {(i): df_sentence_all[i] for i in range(0, len(df_sentence_all))}
with open('sentence_all.json','w') as f:
    json.dump(sentence_all_dict,f)