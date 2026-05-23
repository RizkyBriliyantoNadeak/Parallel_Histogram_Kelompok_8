import sys
import os
import matplotlib.pyplot as plt

# Tambahkan path ke root proyek (folder di atas scripts)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import CAR_BRANDS, YEARS, BIN_LABELS

def parse_golden_file(filename="results/golden_freq.txt"):
    with open(filename, 'r', encoding='utf-8') as f:
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
    return brand_hist, year_hist, price_hist

if __name__ == "__main__":
    brand, year, price = parse_golden_file()
    fig, axes = plt.subplots(1, 3, figsize=(15,5))
    axes[0].bar(CAR_BRANDS, brand, color='skyblue')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].set_title("Merek")
    axes[1].bar([str(y) for y in YEARS], year, color='lightgreen')
    axes[1].tick_params(axis='x', rotation=90)
    axes[1].set_title("Tahun")
    axes[2].bar(BIN_LABELS, price, color='salmon')
    axes[2].set_title("Harga")
    plt.tight_layout()
    plt.savefig("results/from_golden.png", dpi=150)
    plt.show()