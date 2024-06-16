#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Ignore the warnings
import warnings
warnings.filterwarnings('ignore')

# Data manipulation and visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.font_manager as fm
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import font_manager, rc
from matplotlib.ticker import FuncFormatter
plt.rcParams['font.family'] = 'AppleGothic'
from matplotlib.ticker import ScalarFormatter


# In[64]:


# CSV 파일에서 데이터 읽기
data1 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인지역사회재활시설)_목록.csv', encoding='cp949')
data2 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인직업재활시설)_목록.csv', encoding='cp949')
data3 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인의료재활시설)_목록.csv', encoding='cp949')

#print(data1.isnull().sum()) #결측값 확인
#print(data2.isnull().sum()) #결측값 확인
#print(data3.isnull().sum()) #결측값 확인

#각 시설의 정원(수용인원)의 결측값을 평균값으로 채우기
data1['정원(수용인원)']=data1['정원(수용인원)'].fillna(data1['정원(수용인원)'].mean()).astype(int)
data2['정원(수용인원)']=data2['정원(수용인원)'].fillna(data2['정원(수용인원)'].mean()).astype(int)
data3['정원(수용인원)']=data3['정원(수용인원)'].fillna(data3['정원(수용인원)'].mean()).astype(int)

#각 시설의 정원(수용인원)의 0값을 중앙값으로 채우기
data1.loc[data1['정원(수용인원)'] == 0, '정원(수용인원)'] = data1['정원(수용인원)'].mean().astype(int)
data2.loc[data2['정원(수용인원)'] == 0, '정원(수용인원)'] = data2['정원(수용인원)'].mean().astype(int)
data3.loc[data3['정원(수용인원)'] == 0, '정원(수용인원)'] = data3['정원(수용인원)'].mean().astype(int)

#시군구별 모든 시설의 정원 합치기
data1=data1.groupby('시군구명')['정원(수용인원)'].sum()
data2=data2.groupby('시군구명')['정원(수용인원)'].sum()
data3=data3.groupby('시군구명')['정원(수용인원)'].sum()
data_total=pd.concat([data1,data2,data3],axis=1)    #3개의 데이터프레임 합치기
data_total.columns = ['장애인지역사회재활시설 정원', '장애인직업재활시설 정원', '장애인의료재활시설 정원']
data_total['장애인지역사회재활시설 정원']=data_total['장애인지역사회재활시설 정원'].fillna(0).astype(int)
data_total['장애인직업재활시설 정원']=data_total['장애인직업재활시설 정원'].fillna(0).astype(int)
data_total['장애인의료재활시설 정원']=data_total['장애인의료재활시설 정원'].fillna(0).astype(int)

data_total.head()


# In[72]:


#장애인 수와 합치기
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
data_concat = pd.concat([data_total, datasu['합계']], axis=1)
data_concat.columns = ['장애인지역사회재활시설 정원', '장애인직업재활시설 정원', '장애인의료재활시설 정원','시군구별 장애인 수 합계']
hap1=data_concat['장애인지역사회재활시설 정원']
hap2=data_concat['장애인직업재활시설 정원']
hap3=data_concat['장애인의료재활시설 정원']
data_concat['장애인복지시설 정원 총 합계']=hap1+hap2+hap3
data_concat.head()


# In[78]:


#확충해야하는 시설 수 제안
data1 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인지역사회재활시설)_목록.csv', encoding='cp949')
data2 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인직업재활시설)_목록.csv', encoding='cp949')
data3 = pd.read_csv('C:/Users/user/BigData/서울시_사회복지시설(장애인의료재활시설)_목록.csv', encoding='cp949')

#각 시설의 정원(수용인원)의 결측값을 평균값으로 채우기
data1['정원(수용인원)']=data1['정원(수용인원)'].fillna(data1['정원(수용인원)'].mean()).astype(int)
data2['정원(수용인원)']=data2['정원(수용인원)'].fillna(data2['정원(수용인원)'].mean()).astype(int)
data3['정원(수용인원)']=data3['정원(수용인원)'].fillna(data3['정원(수용인원)'].mean()).astype(int)

#각 시설의 정원(수용인원)의 0값을 평균값으로 채우기
data1.loc[data1['정원(수용인원)'] == 0, '정원(수용인원)'] = data1['정원(수용인원)'].mean().astype(int)
data2.loc[data2['정원(수용인원)'] == 0, '정원(수용인원)'] = data2['정원(수용인원)'].mean().astype(int)
data3.loc[data3['정원(수용인원)'] == 0, '정원(수용인원)'] = data3['정원(수용인원)'].mean().astype(int)

#시설 정원 평균값
data_mean=data1['정원(수용인원)'].mean().astype(int)+data2['정원(수용인원)'].mean().astype(int)+data3['정원(수용인원)'].mean().astype(int)
print(data_mean)

#(장애인 수 - 시설 정원 총합) / 시설 정원 평균값
disabled=data_concat['시군구별 장애인 수 합계']
total=data_concat['장애인복지시설 정원 총 합계']
data=disabled-total
data_concat['확충해야하는 시설 수']=round(data.div(data_mean)).astype(int)
data_concat


# In[83]:


#시군구별 확충해야하는 장애인사회복지시설 수
from matplotlib import pyplot as plt
from matplotlib import rcParams, style
style.use('ggplot')
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font',family=font_name)

MC_total=data_concat[['확충해야하는 시설 수']]
MC_total=MC_total.sort_values('확충해야하는 시설 수',ascending=False)
plt.rcParams['figure.figsize']=(25,5)
MC_total.plot(kind='bar',rot=45,)
plt.show()

