"""
Visualisasi histogram distribusi merek, tahun, dan harga.
"""

import sys
import os
import matplotlib.pyplot as plt

# Tambahkan path ke root proyek
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import CAR_BRANDS, YEARS, BIN_LABELS, generate_showroom_data
from src.sequential_analyzer import sequential_analyze

def create_visualizations(data_size=5_000_000, save_path="results/histograms.png"):
    """
    Generate data, hitung histogram secara sequential, buat 3 subplot.
    Simpan ke file dan tampilkan.
    """
    print(f"Generating {data_size:,} records...")
    data = generate_showroom_data(data_size)
    print("Analyzing...")
    brand_hist, year_hist, price_hist = sequential_analyze(data)

    # Setup figure 1 baris 3 kolom
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"Distribusi Stok Showroom (n={data_size:,} records)", fontsize=14)

    # --- 1. Merek ---
    axes[0].bar(CAR_BRANDS, brand_hist, color='skyblue')
    axes[0].set_title("Distribusi Merek")
    axes[0].set_xlabel("Merek")
    axes[0].set_ylabel("Jumlah unit")
    axes[0].tick_params(axis='x', rotation=45)

    # --- 2. Tahun ---
    axes[1].bar([str(y) for y in YEARS], year_hist, color='lightgreen')
    axes[1].set_title("Distribusi Tahun Produksi")
    axes[1].set_xlabel("Tahun")
    axes[1].set_ylabel("Jumlah unit")
    axes[1].tick_params(axis='x', rotation=90)  # agar label tahun tidak bertumpuk

    # --- 3. Harga ---
    axes[2].bar(BIN_LABELS, price_hist, color='salmon')
    axes[2].set_title("Distribusi Harga (juta rupiah)")
    axes[2].set_xlabel("Rentang Harga")
    axes[2].set_ylabel("Jumlah unit")

    plt.tight_layout()
    # Simpan ke file
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Visualisasi disimpan ke {save_path}")
    plt.show()

if __name__ == "__main__":
    # Bisa ubah ukuran data sesuai keinginan (hati-hati dengan memori)
    create_visualizations(data_size=5_000_000)