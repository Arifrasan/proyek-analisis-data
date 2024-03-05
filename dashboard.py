import pandas as pd
import matplotlib as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")


# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df


# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df



# Membuat komponen filter
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()

with st.sidebar:
    # Menambahkan filter tanggal
    start_date = st.date_input(
        label='Pilih Tanggal Awal',
        min_value=min_date,
        max_value=max_date,
        value=min_date
    )

    end_date = st.date_input(
        label='Pilih Tanggal Akhir',
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )

main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)

# Membuat Dashboard secara lengkap

# Membuat judul
st.header('Bike Bike Sharing')
st.subheader('[Pinjam Pinjam Orang Sepeda]', divider='rainbow')

# Membuat jumlah penyewaan harian
st.subheader('Bike Sharing')
col1, col2, col3, col4 = st.columns(4)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual', value=daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered', value=daily_rent_registered)

with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total Peminjam', value=daily_rent_total)

st.subheader('Jumlah Penyewa per Hari')
col4, col5, col6, col7 = st.columns(4)

with col4:
    daily_rent_per_weekday = day_df.groupby('weekday')['count'].sum().reset_index()
    for index, row in daily_rent_per_weekday.iterrows():
        st.metric(row['weekday'], value=row['count'])

    
st.divider()

selected_chart = st.selectbox('Pilih Grafik',
                            ('Jumlah Pengguna Sepeda berdasarkan Hari',
                            'Jumlah Pengguna Sepeda Casual dan Registered berdasarkan tahun',
                            ))

if selected_chart == 'Jumlah Pengguna Sepeda berdasarkan Hari':
    st.subheader('Jumlah Pengguna Sepeda berdasarkan Hari')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=day_df,
        x='weekday',
        y='count',
        hue='weekday',
        palette={"Friday": "#FF3D9A", "Monday": "#F8DB46", "Saturday": "#F8DB46", "Sunday": "#F8DB46", "Thursday": "#F8DB46", "Tuesday": "#F8DB46", "Wednesday": "#F8DB46"},
        ax=ax
    )
    plt.title('Jumlah Pengguna Sepeda berdasarkan Hari')
    plt.xlabel('Hari')
    plt.ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(fig)

elif selected_chart == 'Jumlah Pengguna Sepeda Casual dan Registered berdasarkan tahun':
    st.subheader('Jumlah Pengguna Sepeda Casual dan Registered berdasarkan tahun')
    result_df = day_df.groupby(by="year").agg({
        "registered": ["sum"],
        "casual": ["sum"]
    }).reset_index()

    # Visualisasi menggunakan clustered bar chart
    plt.figure(figsize=(10, 6))

    bar_width = 0.35
    bar_positions_1 = range(len(result_df))
    bar_positions_2 = [pos + bar_width for pos in bar_positions_1]

    plt.bar(bar_positions_1, result_df[("registered", "sum")], width=bar_width, label='Registered')
    plt.bar(bar_positions_2, result_df[("casual", "sum")], width=bar_width, label='Casual')

    plt.xlabel('Year')
    plt.ylabel('Total Count')
    plt.title('Total Registered and Casual Bike Rentals Each Year')
    plt.xticks([pos + bar_width/2 for pos in bar_positions_1], result_df['year'])
    plt.legend()

    # Menampilkan plot menggunakan st.pyplot()
    st.pyplot(plt)

st.markdown('---')
st.caption('Copyright (c) Arifrasan 2024')
