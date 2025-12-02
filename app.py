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


# ================================
# APLIKASI STREAMLIT
# ================================

st.title("📊 APBD Analyzer (Format Vertikal) + Rasio Keuangan + Interpretasi AI")

uploaded = st.file_uploader("Upload file APBD (Excel)", type=["xlsx"])

if uploaded:
    df = pd.read_excel(uploaded)

    st.subheader("📌 Data APBD (Format Vertikal)")
    st.dataframe(df)

    # =============================
    # BACA NILAI MENGIKUTI FORMAT EXCEL KAMU
    # =============================

    # Pendapatan
    pad = df.loc[df['Akun'] == 'PAD', 'Realisasi'].sum()

    transfer = df.loc[df['Akun'].isin([
        'TKDD',
        'Pendapatan Transfer Pemerintah Pusat',
        'Pendapatan Transfer Antar Daerah'
    ]), 'Realisasi'].sum()

    pendapatan_daerah = df.loc[df['Akun'] == 'Pendapatan Daerah', 'Realisasi'].sum()

    target_pad = df.loc[df['Akun'] == 'PAD', 'Anggaran'].sum()
    realisasi_pad = df.loc[df['Akun'] == 'PAD', 'Realisasi'].sum()

    # Belanja
    total_belanja = df.loc[df['Akun'] == 'Belanja Daerah', 'Realisasi'].sum()

    belanja_operasi = df.loc[df['Akun'].isin([
        'Belanja Pegawai',
        'Belanja Barang dan Jasa',
        'Belanja Hibah',
        'Belanja Bantuan Sosial',
        'Belanja Lainnya'
    ]), 'Realisasi'].sum()

    belanja_modal = df.loc[df['Akun'] == 'Belanja Modal', 'Realisasi'].sum()

    anggaran_belanja = df.loc[df['Akun'] == 'Belanja Daerah', 'Anggaran'].sum()

    # =============================
    # HITUNG RASIO
    # =============================

    hasil = {
        "Rasio Kemandirian (PAD / Transfer)": rasio_kemandirian(pad, transfer),
        "Rasio Efektivitas PAD": rasio_efektivitas(realisasi_pad, target_pad),
        "Rasio Efisiensi (Realisasi/Anggaran Belanja)": rasio_efisiensi(total_belanja, anggaran_belanja),
        "Rasio Belanja Operasi": rasio_bo(belanja_operasi, total_belanja),
        "Rasio Belanja Modal": rasio_bm(belanja_modal, total_belanja)
    }

    st.subheader("📈 Hasil Rasio Keuangan")
    st.json(hasil)

    # ================================
    # G R O Q  API
    # ================================

    st.subheader("🧠 Interpretasi AI (Groq)")

    groq_api_key = st.text_input("Masukkan Groq API Key", type="password")

    if groq_api_key:
        prompt = f"Berikan analisis profesional terhadap rasio keuangan daerah berikut: {hasil}"

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
            st.error("Kesalahan API. Periksa API Key atau jaringan.")

