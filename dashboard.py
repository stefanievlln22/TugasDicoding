# streamlit run D:\BANGKIT\PYTHON\Submission\dashboard\dashboard.py
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for seaborn
sns.set(style="whitegrid")

# Load the data
file_path_day = r"C:\Users\WINDOWS11\Downloads\Bike-sharing-dataset\day.csv"
df_day = pd.read_csv(file_path_day)

# Convert 'dteday' to datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Data untuk musim panas 2011 dan 2012
summer_data_2011 = df_day[(df_day['dteday'] >= '2011-06-01') & (df_day['dteday'] <= '2011-08-31')]
summer_data_2012 = df_day[(df_day['dteday'] >= '2012-06-01') & (df_day['dteday'] <= '2012-08-31')]

# Rata-rata penggunaan bike-sharing
average_usage_weekday = df_day.groupby('workingday')['cnt'].mean().reset_index()
average_usage_weekday['day_type'] = np.where(average_usage_weekday['workingday'] == 1, 'Weekday', 'Weekend')

# Rata-rata penyewaan per bulan
df_day['month'] = df_day['dteday'].dt.month
average_usage_month = df_day.groupby('month')['cnt'].mean().reset_index()

# Streamlit Dashboard
st.title("Dashboard Analisis Data Bike-Sharing")

# Menampilkan data harian 2011
st.subheader("Data Harian 2011")
st.write(summer_data_2011)

# Jumlah data musim panas
st.subheader("Jumlah Data Musim Panas 2011")
st.write(f"Jumlah data musim panas 2011: {len(summer_data_2011)}")
st.write(f"Jumlah data musim panas 2012: {len(summer_data_2012)}")

# Rata-rata Penggunaan Bike-Sharing
st.subheader("Rata-rata Penggunaan Bike-Sharing")
average_usage_2011 = summer_data_2011['cnt'].mean()
average_usage_2012 = summer_data_2012['cnt'].mean()
st.write(f"Rata-rata penggunaan bike-sharing selama musim panas 2011: {average_usage_2011:.2f}")
st.write(f"Rata-rata penggunaan bike-sharing selama musim panas 2012: {average_usage_2012:.2f}")

# Rata-rata penggunaan hari kerja vs akhir pekan
st.subheader("Rata-rata Penggunaan Bike-Sharing Hari Kerja vs Akhir Pekan")
st.bar_chart(average_usage_weekday.set_index('day_type')['cnt'])

# Rata-rata jumlah sepeda yang disewa per bulan
st.subheader("Rata-rata Jumlah Sepeda yang Disewa per Bulan")
st.bar_chart(average_usage_month.set_index('month')['cnt'])

# Distribusi jumlah sepeda yang disewa (harian)
st.subheader("Distribusi Jumlah Sepeda yang Disewa (Harian)")
fig, ax = plt.subplots()
sns.histplot(df_day['cnt'], bins=30, kde=True, ax=ax)
ax.set_title('Distribusi Jumlah Sepeda yang Disewa')
ax.set_xlabel('Jumlah Sepeda yang Disewa')
ax.set_ylabel('Frekuensi')
st.pyplot(fig)

# Conclusion
st.subheader('Conclusion')
st.write("""
Dari analisis di atas, kita dapat melihat tren penggunaan sepeda bike-sharing berdasarkan beberapa kategori seperti musim panas, hari kerja vs akhir pekan, dan distribusi penyewaan harian. 
Secara umum, penggunaan sepeda meningkat pada hari kerja dibandingkan dengan akhir pekan. Selain itu, terdapat pola tertentu selama musim panas.
""")