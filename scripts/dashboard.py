import sys
import os
import streamlit as st
import plotly.express as px
import pandas as pd
import json

# Tambahkan path ke root proyek
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import CAR_BRANDS, YEARS, BIN_LABELS, generate_showroom_data
from src.sequential_analyzer import sequential_analyze

# Konfigurasi halaman
st.set_page_config(page_title="AutoFreq Dashboard", layout="wide", page_icon="🚗")
st.title("🚗 AutoFreq – Dashboard Distribusi Stok Showroom")
st.markdown("Analisis frekuensi paralel untuk inventaris mobil")

# Sidebar untuk pengaturan
st.sidebar.header("Pengaturan Data")
data_option = st.sidebar.radio(
    "Sumber data:",
    ["Generate data baru (5 juta record)", "Gunakan data dari file golden_freq.txt"]
)

# Load atau generate data
if data_option == "Generate data baru (5 juta record)":
    with st.spinner("Menghasilkan data 5 juta record..."):
        data = generate_showroom_data(5_000_000)
        brand_hist, year_hist, price_hist = sequential_analyze(data)
    st.sidebar.success("Data berhasil digenerate!")
else:
    # Baca dari hasil golden_freq.txt
    try:
        with open("results/golden_freq.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        brand_hist, year_hist, price_hist = [], [], []
        section = None
        for line in lines:
            line = line.strip()
            if line.startswith("## Merek"):
                section = "brand"
            elif line.startswith("## Tahun"):
                section = "year"
            elif line.startswith("## Harga"):
                section = "price"
            elif section == "brand" and ":" in line and not line.startswith("#"):
                val = int(line.split(":")[1].strip().split()[0])
                brand_hist.append(val)
            elif section == "year" and ":" in line and not line.startswith("#"):
                val = int(line.split(":")[1].strip().split()[0])
                year_hist.append(val)
            elif section == "price" and ":" in line and not line.startswith("#"):
                val = int(line.split(":")[1].strip().split()[0])
                price_hist.append(val)
        st.sidebar.success("Data dari golden_freq.txt berhasil dimuat!")
    except FileNotFoundError:
        st.error("File results/golden_freq.txt tidak ditemukan. Silakan generate data baru.")
        st.stop()

# Konversi ke DataFrame untuk Plotly
df_brand = pd.DataFrame({"Merek": CAR_BRANDS, "Jumlah": brand_hist})
df_year = pd.DataFrame({"Tahun": [str(y) for y in YEARS], "Jumlah": year_hist})
df_price = pd.DataFrame({"Rentang Harga": BIN_LABELS, "Jumlah": price_hist})

# Membuat layout 3 kolom (opsional) atau tampil satu per satu
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Distribusi Merek")
    fig_brand = px.bar(df_brand, x="Merek", y="Jumlah", color="Merek", 
                       title="Jumlah mobil per merek", 
                       labels={"Jumlah": "Unit", "Merek": ""},
                       hover_data={"Jumlah": ":,.0f"})
    fig_brand.update_layout(showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig_brand, use_container_width=True)

    st.subheader("💰 Distribusi Harga")
    fig_price = px.bar(df_price, x="Rentang Harga", y="Jumlah", color="Rentang Harga",
                       title="Distribusi harga (juta rupiah)",
                       labels={"Jumlah": "Unit", "Rentang Harga": ""})
    fig_price.update_layout(showlegend=False)
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    st.subheader("📅 Distribusi Tahun Produksi")
    # Plot tahun, filter jika terlalu padat? Tampilkan semua
    fig_year = px.bar(df_year, x="Tahun", y="Jumlah", color="Tahun",
                      title="Jumlah mobil per tahun",
                      labels={"Jumlah": "Unit", "Tahun": ""})
    fig_year.update_layout(showlegend=False, xaxis_tickangle=-90)
    st.plotly_chart(fig_year, use_container_width=True)

# Tabel data tambahan
with st.expander("Lihat data mentah (angka)"):
    st.write("**Distribusi Merek**")
    st.dataframe(df_brand)
    st.write("**Distribusi Tahun**")
    st.dataframe(df_year)
    st.write("**Distribusi Harga**")
    st.dataframe(df_price)

# Footer
st.markdown("---")
st.caption("AutoFreq – Parallel Frequency Analyzer for Showroom Inventory | Dibuat dengan Streamlit & Plotly")