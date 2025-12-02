import streamlit as st
import pandas as pd
import requests
import os

# ============================
# GUNAKAN API KEY TANPA INPUT
# ============================

groq_api_key = "ISI_API_KEY_KAMU_DI_SINI"  
# ATAU pakai environment:
# groq_api_key = os.getenv("GROQ_API_KEY")

# ================================
# FUNGSI PERHITUNGAN RASIO
# ================================

def rasio_kemandirian(pad, transfer):
    return pad / transfer if transfer != 0 else 0

def rasio_efektivitas(realisasi_pad, target_pad):
    return realisasi_pad / target_pad if target_pad != 0 else 0
    
def rasio_efisiensi(realisasi_belanja, anggaran_belanja):
    return realisasi_belanja / anggaran_belanja if anggaran_belanja != 0 else 0

def rasio_bo(bo, total):
    return bo / total if total != 0 else 0

def rasio_bm(bm, total):
    return bm / total if total != 0 else 0


# ================================
# APLIKASI
# ================================

st.title("📊 APBD Analyzer + AI Interpretasi Groq (Tanpa Input API Key)")

uploaded = st.file_uploader("Upload file APBD (Excel)", type=["xlsx"])

if uploaded:
    df = pd.read_excel(uploaded)
    st.dataframe(df)

    # Ambil nilai
    pad = df.loc[df['Akun'] == 'PAD', 'Realisasi'].sum()
    transfer = df.loc[df['Akun'] == 'TKDD', 'Realisasi'].sum()
    target_pad = df.loc[df['Akun'] == 'PAD', 'Anggaran'].sum()
    realisasi_pad = pad
    total_belanja = df.loc[df['Akun'] == 'Belanja Daerah', 'Realisasi'].sum()
    belanja_operasi = df.loc[df['Akun'].isin([
        'Belanja Pegawai', 'Belanja Barang dan Jasa',
        'Belanja Hibah', 'Belanja Bantuan Sosial'
    ]), 'Realisasi'].sum()

    belanja_modal = df.loc[df['Akun'] == 'Belanja Modal', 'Realisasi'].sum()
    anggaran_belanja = df.loc[df['Akun'] == 'Belanja Daerah', 'Anggaran'].sum()

    hasil = {
        "Rasio Kemandirian": pad / transfer,
        "Rasio Efektivitas": realisasi_pad / target_pad,
        "Rasio Efisiensi": total_belanja / anggaran_belanja,
        "Rasio Belanja Operasi": belanja_operasi / total_belanja,
        "Rasio Belanja Modal": belanja_modal / total_belanja
    }

    st.subheader("📌 Hasil Rasio")
    st.json(hasil)

    # ===========================
    # ANALISIS AI OTOMATIS
    # ===========================

    prompt = f"""
    Berikan analisis profesional dan lengkap terhadap rasio keuangan berikut:
    {hasil}
    """

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

    ai_output = response.json()["choices"][0]["message"]["content"]
    st.subheader("🧠 Analisis AI (Groq)")
    st.write(ai_output)


