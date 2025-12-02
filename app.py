import streamlit as st
import pandas as pd
import requests

# ================================
# FUNGSI PERHITUNGAN RASIO
# ================================

def rasio_kemandirian(pad, transfer):
    return pad / transfer if transfer != 0 else 0

def rasio_efektivitas(realisasi_pad, target_pad):
    return realisasi_pad / target_pad if target_pad != 0 else 0
    
def rasio_efisiensi(realisasi_belanja, anggaran_belanja):
    return realisasi_belanja / anggaran_belanja if anggaran_belanja != 0 else 0

def rasio_bo(belanja_operasi, total_belanja):
    return belanja_operasi / total_belanja if total_belanja != 0 else 0

def rasio_bm(belanja_modal, total_belanja):
    return belanja_modal / total_belanja if total_belanja != 0 else 0

def pertumbuhan(nilai_sekarang, nilai_lalu):
    return (nilai_sekarang - nilai_lalu) / nilai_lalu if nilai_lalu != 0 else 0


# ================================
# APLIKASI STREAMLIT
# ================================

st.title("📊 APBD Analyzer + Rasio Keuangan + Interpretasi AI ")

uploaded = st.file_uploader("Upload file APBD (Excel)", type=["xlsx"])

if uploaded:

    try:
        df = pd.read_excel(uploaded)
        st.success("File berhasil dibaca!")
    except Exception as e:
        st.error(f"Gagal membaca file Excel: {e}")
        st.stop()

    st.subheader("📌 Data APBD")
    st.dataframe(df)

    # Validasi kolom
    required_cols = [
        "PAD", "Dana_Transfer", "Belanja_Operasi", "Belanja_Modal",
        "Total_Belanja", "Pendapatan_Daerah", "Target_PAD",
        "Realisasi_PAD", "Anggaran_Belanja"
    ]

    for col in required_cols:
        if col not in df.columns:
            st.error(f"Kolom '{col}' tidak ditemukan di Excel.")
            st.stop()

    # Baca nilai
    pad = df['PAD'].sum()
    transfer = df['Dana_Transfer'].sum()
    belanja_operasi = df['Belanja_Operasi'].sum()
    belanja_modal = df['Belanja_Modal'].sum()
    total_belanja = df['Total_Belanja'].sum()
    pendapatan_daerah = df['Pendapatan_Daerah'].sum()
    target_pad = df['Target_PAD'].sum()
    realisasi_pad = df['Realisasi_PAD'].sum()
    anggaran_belanja = df['Anggaran_Belanja'].sum()

    # Hitung rasio
    hasil = {
        "Rasio Kemandirian": rasio_kemandirian(pad, transfer),
        "Rasio Efektivitas PAD": rasio_efektivitas(realisasi_pad, target_pad),
        "Rasio Efisiensi": rasio_efisiensi(total_belanja, anggaran_belanja),
        "Rasio Belanja Operasi": rasio_bo(belanja_operasi, total_belanja),
        "Rasio Belanja Modal": rasio_bm(belanja_modal, total_belanja)
    }

    st.subheader("📈 Hasil Perhitungan Rasio")
    st.json(hasil)

    # ================================
    # G R O Q  API
    # ================================

    st.subheader("🧠 Interpretasi AI (Groq)")

    groq_api_key = st.text_input("Masukkan Groq API Key", type="password")

    if groq_api_key:
        prompt = f"Buatkan analisis profesional terhadap rasio keuangan daerah berikut: {hasil}"

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {groq_api_key}"},
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        try:
            ai_output = response.json()["choices"][0]["message"]["content"]
            st.write(ai_output)
        except:
            st.error("Kesalahan API. Periksa API Key dan jaringan.")
