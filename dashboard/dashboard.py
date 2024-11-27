import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import streamlit as st
import os


print(os.path.exists("data/day.csv")) 
print(os.path.exists("data/hour.csv"))


day_df = pd.read_csv("C:/Users/danty/Downloads/dicoding/Project/data/day.csv")

day_df.head()


hour_df = pd.read_csv("C:/Users/danty/Downloads/dicoding/Project/data/hour.csv")
hour_df.head()

import os
print("Current working directory:", os.getcwd())

day_file_path = "C:/Users/danty/Downloads/dicoding/Project/data/day.csv"
hour_file_path = "C:/Users/danty/Downloads/dicoding/Project/data/hour.csv"
try:
    day_df = pd.read_csv(day_file_path)
    hour_df = pd.read_csv(hour_file_path)
    print("Data berhasil dimuat!")
except FileNotFoundError as e:
    print("Error: File tidak ditemukan. Periksa kembali path file Anda.")
    raise e


print("C:/Users/danty/Downloads/dicoding/Project/data/day.csv")
print(day_df.info())

day_df.isna().sum()

print("Jumlah duplikasi: ", day_df.duplicated().sum())

day_df.describe()

print("C:/Users/danty/Downloads/dicoding/Project/data/hour.csv")
print(hour_df.info())

hour_df.nunique()

print("Jumlah duplikasi: ", hour_df.duplicated().sum())

hour_df.describe()

day_df.duplicated().sum()

day_df.drop_duplicates(inplace=True)

print("Jumlah duplikasi: ", day_df.duplicated().sum())

print("Missing values sebelum cleansing:")
print("day_df", day_df.isnull().sum())

hour_df.duplicated().sum()

hour_df.drop_duplicates(inplace=True)

print("Jumlah duplikasi: ", hour_df.duplicated().sum())

print("Missing values sebelum cleansing:")
print("hour_df", hour_df.isnull().sum())

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
merged_data = pd.merge(hour_df, day_df, on='dteday', suffixes=('_hour', '_day'))

print("Dataset setelah penggabungan")
print(merged_data.info())
print(merged_data.head())

day_hour_df = pd.merge(
    left=day_df,
    right=hour_df,
    how="outer",
)
day_hour_df.head()
day_hour_df.nunique()
day_hour_df.isna().sum()
day_hour_df[day_hour_df.hr.isna()]
day_hour_df.hr.value_counts()
day_hour_df.fillna(value="hr", inplace=True) 
day_hour_df.isna().sum()

day_df.describe(include="all")
day_df.groupby(['weathersit', 'season', 'workingday'])['cnt'].mean().sort_values(ascending=False)

import seaborn as sns
import pandas as pd


print(day_df.isnull().sum())  
print(hour_df.isnull().sum()) 

day_df = day_df.dropna()  

print(day_df['weathersit'].unique())

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

plt.figure(figsize=(8, 5))
sns.barplot(data=day_df, x="weathersit", y="cnt", palette="Blues_d", ci=None)
plt.title("Pengaruh Cuaca terhadap Penggunaan Sepeda", fontsize=16)
plt.xlabel("Kondisi Cuaca (1=Cerah, 2=Hujan, 3=Badai)", fontsize=12)
plt.ylabel("Rata-Rata Penggunaan Sepeda", fontsize=12)
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(data=day_df, x="season", y="cnt", palette="Set2")
plt.title("Pengaruh Musim terhadap Penggunaan Sepeda", fontsize=16)
plt.xlabel("Musim (1=Dingin, 2=Semi, 3=Panas, 4=Gugur)", fontsize=12)
plt.ylabel("Jumlah Penggunaan Sepeda", fontsize=12)
plt.show()

plt.figure(figsize=(8, 6))
sns.barplot(data=day_df, x="workingday", y="cnt", palette="Pastel1", ci=None)
plt.title("Pengaruh Hari Kerja terhadap Penggunaan Sepeda", fontsize=16)
plt.xlabel("Hari Kerja (0=Libur, 1=Kerja)", fontsize=12)
plt.ylabel("Rata-Rata Penggunaan Sepeda", fontsize=12)
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(data=day_df, x="temp", y="cnt", hue="season", palette="cool", alpha=0.7)
plt.title("Hubungan Suhu terhadap Penggunaan Sepeda", fontsize=16)
plt.xlabel("Suhu (Normalisasi)", fontsize=12)
plt.ylabel("Jumlah Penggunaan Sepeda", fontsize=12)
plt.legend(title="Musim", labels=["Dingin", "Semi", "Panas", "Gugur"], loc="upper left")
plt.show()


total_cnt_by_hour = hour_df.groupby('hr')['cnt'].sum()

plt.figure(figsize=(10, 6))
sns.lineplot(x=total_cnt_by_hour.index.astype(int), y=total_cnt_by_hour.values, marker='o', color='blue')
plt.title('Total Jumlah Penyewaan Sepeda berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Total Jumlah Penyewaan')
plt.xticks(ticks=range(24), rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

import pandas as pd

file_path = ("C:/Users/danty/Downloads/dicoding/Project/data/day.csv")  
df = pd.read_csv(file_path)

print(df.head())

import pandas as pd
file_path = ("data/day.csv")
df = pd.read_csv(file_path)


if 'dteday' in df.columns:
    df['dteday'] = pd.to_datetime(df['dteday'])
else:
    raise ValueError("Kolom 'dteday' tidak ditemukan dalam dataset.")


snapshot_date = df['dteday'].max() + pd.Timedelta(days=1)


required_columns = ['season', 'temp', 'weathersit', 'workingday', 'cnt']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Kolom berikut tidak ditemukan dalam dataset: {missing_columns}")


df['total_rentals'] = df['cnt']  


rfm_df = df.groupby(['season', 'temp', 'weathersit', 'workingday']).agg({
    'dteday': lambda x: (snapshot_date - x.max()).days,  
    'total_rentals': 'count',  
    'cnt': 'sum'  
}).reset_index()


rfm_df.columns = ['season', 'temp', 'weathersit', 'workingday', 'recency', 'frequency', 'monetary']


rfm_df['monetary'] = pd.to_numeric(rfm_df['monetary'], errors='coerce')


try:
    
    rfm_df['r_quartile'] = pd.qcut(rfm_df['recency'], 4, labels=[4, 3, 2, 1])  
    rfm_df['f_quartile'] = pd.qcut(rfm_df['frequency'], 4, labels=[1, 2, 3, 4]) 
    rfm_df['m_quartile'] = pd.qcut(rfm_df['monetary'], 4, labels=[1, 2, 3, 4])  
except ValueError as e:
    print("Terjadi kesalahan pada qcut. Pastikan data cukup bervariasi untuk kuartil. Kesalahan:", e)
    rfm_df['r_quartile'] = pd.cut(rfm_df['recency'], 4, labels=[4, 3, 2, 1])
    rfm_df['f_quartile'] = pd.cut(rfm_df['frequency'], 4, labels=[1, 2, 3, 4])
    rfm_df['m_quartile'] = pd.cut(rfm_df['monetary'], 4, labels=[1, 2, 3, 4])


rfm_df['RFMScore'] = rfm_df['r_quartile'].astype(str) + rfm_df['f_quartile'].astype(str) + rfm_df['m_quartile'].astype(str)


print(rfm_df[['season', 'temp', 'weathersit', 'workingday', 'recency', 'frequency', 'monetary', 'RFMScore']].head())


import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.histplot(rfm_df['monetary'], bins=20, kde=True, color='blue')
plt.title('Distribusi Monetary (Total Penyewaan)', fontsize=16)
plt.xlabel('Monetary (Total Penyewaan)', fontsize=12)
plt.ylabel('Frekuensi', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

plt.figure(figsize=(8, 5))
sns.boxplot(x=rfm_df['monetary'], color='cyan')
plt.title('Boxplot Monetary (Total Penyewaan)', fontsize=16)
plt.xlabel('Monetary (Total Penyewaan)', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(10, 6))
sns.scatterplot(x='recency', y='frequency', hue='RFMScore', data=rfm_df, palette='viridis', s=100, edgecolor='k', alpha=0.7)
plt.title('Distribusi Segmen RFM: Recency vs Frequency', fontsize=16)
plt.xlabel('Recency (Hari Terakhir Penyewaan)', fontsize=12)
plt.ylabel('Frequency (Jumlah Penyewaan)', fontsize=12)
plt.legend(title='RFM Score', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()


rfm_corr = rfm_df[['recency', 'frequency', 'monetary']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(rfm_corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Korelasi antara Recency, Frequency, dan Monetary', fontsize=16)
plt.show()


import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(10, 6))
sns.histplot(rfm_df['RFMScore'], bins=10, kde=False, color='skyblue', discrete=True)
plt.title('Distribusi RFM Score', fontsize=16)
plt.xlabel('RFM Score', fontsize=12)
plt.ylabel('Frekuensi', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()