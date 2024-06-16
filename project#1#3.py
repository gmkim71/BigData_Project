#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Ignore the warnings
import warnings
warnings.filterwarnings('ignore')

# Data manipulation and visualization
import seaborn as sns
sns.set_style("whitegrid")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.font_manager as fm
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import font_manager, rc
from matplotlib.ticker import FuncFormatter
plt.rcParams['font.family'] = 'AppleGothic'
from matplotlib.ticker import ScalarFormatter

import folium
import json

get_ipython().system('pip install geopandas')
import geopandas


# In[2]:


###1

# 데이터 읽기
df = pd.read_csv('Documents/data/1. 서울시등록장애인집계현황(시군구별,정도별).csv', encoding='cp949')

# 데이터프레임 확인
print(df.head())
print(df.columns)


# In[25]:


import matplotlib.ticker as ticker

# CSV 파일에서 데이터 읽기
data = pd.read_csv('Documents/data/1. 서울시등록장애인집계현황(시군구별,정도별).csv', encoding='cp949')

# 필요한 컬럼 선택 및 데이터 타입 변환
data = data[['시군구별(2)', '합계', '심한장애', '심하지않은장애']]
data[['합계', '심한장애', '심하지않은장애']] = data[['합계', '심한장애', '심하지않은장애']].astype(int)

# '소계' 행 제외
data = data[data['시군구별(2)'] != '소계']

# 데이터 내림차순
data = data.sort_values(by='합계', ascending=False)

# 바 차트
fig, ax = plt.subplots(figsize=(12, 8))
data.plot(x='시군구별(2)', y=['심한장애', '심하지않은장애'], kind='bar', stacked=True, ax=ax)
ax.set_title('서울시 시군구별 장애인 수(2022)', fontsize=16, fontweight='bold')
ax.set_xlabel('시군구명', fontsize=12)
ax.set_ylabel('장애인 수(명)', fontsize=12)
ax.legend(['심한 장애', '심하지 않은 장애'], fontsize=10)
ax.annotate('1-3급: 심한 장애\n4-6급: 심하지 않은 장애', textcoords = 'offset points',
            xy = (19,385), fontsize = 12)
ax.tick_params(axis='x', labelrotation=45)
plt.tight_layout()

# y축 레이블 포맷 지정
formatter = ticker.FuncFormatter(lambda x, p: format(int(x), ','))
plt.gca().yaxis.set_major_formatter(formatter)

plt.show()


# In[2]:


# 데이터 읽기
df = pd.read_csv('Documents/data/2. 서울시등록장애인집계현황(장애유형별).csv', encoding='cp949')

# 데이터프레임 확인
print(df.head())
print(df.columns)


# In[24]:


# CSV 파일에서 데이터 읽기
data = pd.read_csv('Documents/data/2. 서울시등록장애인집계현황(장애유형별).csv', encoding='cp949')

# 필요한 컬럼 선택
data = data[['장애유형별(1)', '총계']]

# '소계' 행 제외
data = data[data['장애유형별(1)'] != '소계']

# '총계' 컬럼의 데이터 타입 변환
data['총계'] = pd.to_numeric(data['총계'], errors='coerce')

# 데이터 내림차순 정렬
data = data.sort_values(by='총계', ascending=False)

# 장애유형별 총계 바 차트 출력
plt.figure(figsize=(12, 8))
plt.bar(data['장애유형별(1)'], data['총계'], width=0.8, color='red')
plt.title('서울시 장애유형별 장애인 수(2022)', fontsize=16)
plt.xlabel('장애유형', fontsize=12)
plt.ylabel('장애인 수(명)', fontsize=12)
plt.xticks(rotation=45)
plt.ylim(0, data['총계'].max() * 1.2)  # y축 범위 조정

# y축 레이블 포맷 지정
formatter = ticker.FuncFormatter(lambda x, p: format(int(x), ','))
plt.gca().yaxis.set_major_formatter(formatter)

# 마지막 x-label 제거 (x-label의 '장애유형별(1)' 제거)
plt.xticks(data['장애유형별(1)'][:-1], rotation=45)

plt.show()


# In[13]:


###3

import folium
import pandas as pd
import json

# CSV 파일에서 데이터 읽기
data = pd.read_csv('Documents/data/1. 서울시등록장애인집계현황(시군구별,정도별).csv', encoding='cp949')

# 필요한 컬럼 선택 및 데이터 타입 변환
data = data[['시군구별(2)', '합계']]
data['합계'] = data['합계'].astype(int)

# '소계' 행 제외
data = data[data['시군구별(2)'] != '소계']

# GeoJSON 파일 읽기
with open('Documents/data/서울시+법정경계(시군구).geojson', encoding='utf-8') as file:
    geo = json.load(file)

# 중심 좌표 설정
center = [37.5665, 126.9780]

# 지도 생성
m = folium.Map(location=center, titles='Maps', zoom_start=11)

# Choropleth 레이어 추가
folium.Choropleth(
    geo_data=geo,
    name='choropleth',
    data=data,
    columns=['시군구별(2)', '합계'],
    key_on='feature.properties.SIG_KOR_NM',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='서울시 시군구별 장애인 수'
).add_to(m)

# 지도 출력
m


# In[23]:


#서울시_사회복지시설(장애인지역사회재활시설)
# CSV 파일에서 데이터 읽기
data = pd.read_csv('Documents/data/1. 서울시등록장애인집계현황(시군구별,정도별).csv', encoding='cp949')

# 필요한 컬럼 선택 및 데이터 타입 변환
data = data[['시군구별(2)', '합계']]
data['합계'] = data['합계'].astype(int)

# '소계' 행 제외
data = data[data['시군구별(2)'] != '소계']

# GeoJSON 파일 읽기
with open('Documents/data/서울시+법정경계(시군구).geojson', encoding='utf-8') as file:
    geo = json.load(file)

# CSV 파일에서 사회복지시설 데이터 읽기
data2 = pd.read_csv('Documents/data/new_geo_서울시_사회복지시설(장애인지역사회재활시설)_목록.csv', encoding='utf-8')

# 필요한 컬럼 선택
data2 = data2[['field1', '_X', '_Y']]

# 중심 좌표 설정
center = [37.5665, 126.9780]

# 지도 생성
m = folium.Map(location=center, zoom_start=11)

# Choropleth 레이어 추가
folium.Choropleth(
    geo_data=geo,
    name='choropleth',
    data=data,
    columns=['시군구별(2)', '합계'],
    key_on='feature.properties.SIG_KOR_NM',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='서울시 시군구별 장애인 수'
).add_to(m)

# 장애인 사회복지시설 좌표 찾기
for index, row in data2.iterrows():
    name = row['field1']
    lat = row['_Y']
    lon = row['_X']
    folium.CircleMarker([lat, lon], radius=5, color='blue', fill=True, fill_color='blue').add_to(m)
    #시설이름 마커에 표시
    #folium.Marker([lat, lon], popup=name).add_to(m)

# 지도 출력
m


# In[21]:


#서울시_사회복지시설(장애인직업재활시설)
# CSV 파일에서 데이터 읽기
data = pd.read_csv('Documents/data/1. 서울시등록장애인집계현황(시군구별,정도별).csv', encoding='cp949')

# 필요한 컬럼 선택 및 데이터 타입 변환
data = data[['시군구별(2)', '합계']]
data['합계'] = data['합계'].astype(int)

# '소계' 행 제외
data = data[data['시군구별(2)'] != '소계']

# GeoJSON 파일 읽기
with open('Documents/data/서울시+법정경계(시군구).geojson', encoding='utf-8') as file:
    geo = json.load(file)

# CSV 파일에서 사회복지시설 데이터 읽기
data2 = pd.read_csv('Documents/data/new_geo_서울시_사회복지시설(장애인직업재활시설)_목록.csv', encoding='utf-8')

# 필요한 컬럼 선택
data2 = data2[['field1', '_X', '_Y']]

# 중심 좌표 설정
center = [37.5665, 126.9780]

# 지도 생성
m = folium.Map(location=center, zoom_start=11)

# Choropleth 레이어 추가
folium.Choropleth(
    geo_data=geo,
    name='choropleth',
    data=data,
    columns=['시군구별(2)', '합계'],
    key_on='feature.properties.SIG_KOR_NM',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='서울시 시군구별 장애인 수'
).add_to(m)

# 장애인 사회복지시설 좌표 찾기
for index, row in data2.iterrows():
    name = row['field1']
    lat = row['_Y']
    lon = row['_X']
    folium.CircleMarker([lat, lon], radius=5, color='blue', fill=True, fill_color='blue').add_to(m)
    #시설이름 마커에 표시
    #folium.Marker([lat, lon], popup=name).add_to(m)

# 지도 출력
m


# In[19]:


#서울시_사회복지시설(장애인의료재활시설)
# CSV 파일에서 데이터 읽기
data = pd.read_csv('Documents/data/1. 서울시등록장애인집계현황(시군구별,정도별).csv', encoding='cp949')

# 필요한 컬럼 선택 및 데이터 타입 변환
data = data[['시군구별(2)', '합계']]
data['합계'] = data['합계'].astype(int)

# '소계' 행 제외
data = data[data['시군구별(2)'] != '소계']

# GeoJSON 파일 읽기
with open('Documents/data/서울시+법정경계(시군구).geojson', encoding='utf-8') as file:
    geo = json.load(file)

# CSV 파일에서 사회복지시설 데이터 읽기
data2 = pd.read_csv('Documents/data/new_geo_서울시_사회복지시설(장애인의료재활시설)_목록.csv', encoding='utf-8')

# 필요한 컬럼 선택
data2 = data2[['field1', '_X', '_Y']]

# 중심 좌표 설정
center = [37.5665, 126.9780]

# 지도 생성
m = folium.Map(location=center, zoom_start=11)

# Choropleth 레이어 추가
folium.Choropleth(
    geo_data=geo,
    name='choropleth',
    data=data,
    columns=['시군구별(2)', '합계'],
    key_on='feature.properties.SIG_KOR_NM',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='서울시 시군구별 장애인 수'
).add_to(m)

# 장애인 사회복지시설 좌표 찾기
for index, row in data2.iterrows():
    name = row['field1']
    lat = row['_Y']
    lon = row['_X']
    folium.CircleMarker([lat, lon], radius=5, color='blue', fill=True, fill_color='blue').add_to(m)
    #시설이름 마커에 표시
    #folium.Marker([lat, lon], popup=name).add_to(m)

# 지도 출력
m

