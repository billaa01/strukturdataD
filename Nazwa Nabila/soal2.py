import streamlit as st
import pandas as pd

st.title("Social Media Word Count")

# Input Komentar
user_input = st.text_area("Masukkan komentar sosial media di sini:", 
                         "belajar python itu seru, python sangat powerful untuk data science dan belajar streamlit.")

if user_input:
    # Preprocessing sederhana: kecilkan huruf dan bersihkan tanda baca
    words = user_input.lower().replace(",", "").replace(".", "").split()
    
    # Menghitung frekuensi (Key: Kata, Value: Frekuensi)
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Konversi ke DataFrame untuk visualisasi
    df = pd.DataFrame(list(word_freq.items()), columns=['Kata', 'Frekuensi'])
    df = df.sort_values(by='Frekuensi', ascending=False)

    # Tampilkan Data
    st.subheader("Tabel Frekuensi Kata")
    st.dataframe(df)

    # Visualisasi Bar Chart
    st.subheader("Grafik Frekuensi")
    st.bar_chart(data=df, x='Kata', y='Frekuensi')