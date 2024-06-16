#!/usr/bin/env python
# coding: utf-8

# In[10]:


import os
import sys
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv


# In[11]:


#폰트 설정
from matplotlib import font_manager, rc
font_path="C:\Windows\\Fonts\\batang.ttc"
font=font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


# In[12]:


# 데이터 읽기
data1 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인지역사회재활시설)_목록.csv', encoding='cp949')
data2 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인직업재활시설)_목록.csv', encoding='cp949')
data3 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인의료재활시설)_목록.csv', encoding='cp949')

#data2.drop([138,139], axis=0, inplace=True)    #잘못 설정된 장애인직업재활시설의 138,139행을 삭제
data2.head()    #장애인적업재활시설 데이터 확인


# In[13]:


# CSV 파일에서 데이터 읽기
data1 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인지역사회재활시설)_목록.csv', encoding='cp949')
data2 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인직업재활시설)_목록.csv', encoding='cp949')
data3 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인의료재활시설)_목록.csv', encoding='cp949')


#시군구명 장애인 사회복지시설 개수 세기
data1 = data1['시군구명'].value_counts()
data2 = data2['시군구명'].value_counts()
data3 = data3['시군구명'].value_counts()

data = pd.concat([data1,data2,data3],axis=1)    #3개의 데이터프레임 합치기
data = data.fillna(0).astype(int)    #결측값을 0으로 설정
data.columns = ['장애인지역사회재활시설', '장애인직업재활시설', '장애인의료재활시설']
data.info()


# In[14]:


#데이터 시군구명 이름순으로으로 정렬
data = data.sort_values(by='시군구명', ascending=True)
data.head()


# In[15]:


# 시군구명 장애인 사회복지시설 수 바 차트 시각화
fig, ax = plt.subplots(figsize=(12, 8))
data.plot(kind='bar', stacked=True, ax=ax)
ax.set_title('서울시 시군구별 사회복지시설 수', fontsize=16, fontweight='bold')
ax.set_xlabel('시군구', fontsize=12)
ax.set_ylabel('사회복지시설 수', fontsize=12)
ax.legend(['장애인지역사회재활시설','장애인직업재활시설', '장애인의료재활시설'], fontsize=10)
ax.tick_params(axis='x', labelrotation=45)
ax.tick_params(axis='both', labelsize=10)
plt.tight_layout()
plt.show()


# In[78]:


#시군구 별 장애인 합계에 대한 장애복지시설 비율
# 서울시등록장애인집계현황 데이터 읽기
df = pd.read_csv('C:/Users/user/BigData/1.서울시등록장애인집계현황(시군구별,정도별).csv', encoding='cp949')

# CSV 파일에서 데이터 읽기
datasu = pd.read_csv('C:/Users/user/BigData/1.서울시등록장애인집계현황(시군구별,정도별).csv', encoding='cp949')

# 필요한 컬럼 선택
datasu = datasu[['시군구별(2)', '합계']]

# '소계' 행 제외
datasu = datasu[datasu['시군구별(2)'] != '소계']

# '합계' 컬럼의 데이터 타입 변환
datasu['합계'] = pd.to_numeric(datasu['합계'], errors='coerce')

# 데이터 내림차순
datasu = datasu.sort_values(by='시군구별(2)', ascending=True)

#인덱스 변경
datasu = datasu.set_index(keys=['시군구별(2)'], inplace=False, drop=True)
datasu.head()

#장애인 사회복지시설 수와 장애인 수 합계 합치기
data_concat = pd.concat([data, datasu['합계']], axis=1)

#컬럼 이름 바꾸기
data_concat = data_concat.rename(columns={'합계':'장애인 수'}) #컬럼 이름 변경

#장애인 수에 대한 장애인사회복지시설의 비율 구하기
count1=data_concat['장애인지역사회재활시설']
count2=data_concat['장애인직업재활시설']
count3=data_concat['장애인의료재활시설']

data_concat['장애인지역사회재활시설 비율']=count1.div(data_concat['장애인 수'],axis=0)*1000
data_concat['장애인직업재활시설 비율']=count2.div(data_concat['장애인 수'],axis=0)*1000
data_concat['장애인의료재활시설 비율']=count3.div(data_concat['장애인 수'],axis=0)*1000

data_concat.head()


# In[79]:


#장애인 수에 대한 장애인사회복지시설의 비율 차트 그리기
from matplotlib import pyplot as plt
from matplotlib import rcParams, style
style.use('ggplot')
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font',family=font_name)

MC_ratio=data_concat[['장애인지역사회재활시설 비율','장애인직업재활시설 비율', '장애인의료재활시설 비율']]
MC_ratio=MC_ratio.sort_index(ascending=True)
plt.rcParams['figure.figsize']=(25,5)
MC_ratio.plot(kind='bar',rot=90,)
plt.show()

