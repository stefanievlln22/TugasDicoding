import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for seaborn
sns.set(style="whitegrid")

# Load the data
df_day = pd.read_csv("day.csv")

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
average_usage_2011 = summer_data_2011['cnt'].mean()
average_usage_2012 = summer_data_2012['cnt'].mean()
st.write(f"Rata-rata penggunaan bike-sharing selama musim panas 2011: {average_usage_2011:.2f}")
st.write(f"Rata-rata penggunaan bike-sharing selama musim panas 2012: {average_usage_2012:.2f}")

# Rata-rata penggunaan hari kerja vs akhir pekan
st.subheader("Rata-rata Penggunaan Bike-Sharing Hari Kerja vs Akhir Pekan")
weekday_usage = average_usage_weekday.loc[average_usage_weekday['day_type'] == 'Weekday', 'cnt'].values[0]
weekend_usage = average_usage_weekday.loc[average_usage_weekday['day_type'] == 'Weekend', 'cnt'].values[0]

# Menghitung persentase peningkatan
percentage_increase = ((weekday_usage - weekend_usage) / weekend_usage) * 100

fig1, ax1 = plt.subplots()
sns.barplot(x='day_type', y='cnt', data=average_usage_weekday, ax=ax1, color='Blue')
ax1.set_title('Rata-rata Penggunaan Bike-Sharing: Hari Kerja vs Akhir Pekan')
ax1.set_xlabel('Tipe Hari')
ax1.set_ylabel('Rata-rata Jumlah Sepeda yang Disewa')
ax1.annotate(f'Persentase Peningkatan: {percentage_increase:.2f}%', 
             xy=(0.5, weekday_usage), 
             xytext=(0.5, weekday_usage + 5),
             ha='center', 
             fontsize=12, 
             color='black',
             arrowprops=dict(arrowstyle='->', lw=1.5))
st.pyplot(fig1)

# Rata-rata jumlah sepeda yang disewa per bulan
st.subheader("Rata-rata Jumlah Sepeda yang Disewa per Bulan")
fig2, ax2 = plt.subplots()
sns.barplot(x='month', y='cnt', data=average_usage_month, ax=ax2)
ax2.set_title('Rata-rata Jumlah Sepeda yang Disewa per Bulan')
ax2.set_xlabel('Bulan')
ax2.set_ylabel('Rata-rata Jumlah Sepeda yang Disewa')
st.pyplot(fig2)

# Visualisasi Tren Penggunaan Bike-Sharing Musim Panas 2011 vs 2012
st.subheader("Tren Penggunaan Bike-Sharing Musim Panas 2011 vs 2012")
daily_usage_2011 = summer_data_2011.groupby('dteday')['cnt'].sum()
daily_usage_2012 = summer_data_2012.groupby('dteday')['cnt'].sum()

fig3, ax3 = plt.subplots(figsize=(14, 7))
ax3.plot(daily_usage_2011.index, daily_usage_2011, label='Musim Panas 2011', color='blue')
ax3.plot(daily_usage_2012.index, daily_usage_2012, label='Musim Panas 2012', color='red')

ax3.set_title('Tren Penggunaan Bike-Sharing Musim Panas 2011 vs 2012')
ax3.set_xlabel('Tanggal')
ax3.set_ylabel('Jumlah Sepeda yang Disewa')
ax3.legend()
ax3.grid()
st.pyplot(fig3)

# Conclusion
st.subheader('Kesimpulan')
st.write(""" 
Dari analisis di atas, kita dapat melihat tren penggunaan sepeda bike-sharing berdasarkan beberapa kategori seperti hari kerja vs akhir pekan dan perbandingan antara musim panas 2011 dan 2012. 
Penggunaan sepeda cenderung lebih tinggi pada hari kerja dibandingkan dengan akhir pekan. Selain itu, terdapat variasi penggunaan sepeda antara musim panas di tahun yang berbeda.
""")
