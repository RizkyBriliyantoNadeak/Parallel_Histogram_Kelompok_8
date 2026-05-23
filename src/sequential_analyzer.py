"""
Sequential version of AutoFreq analyzer.
"""

import sys
import os
# Tambahkan path parent agar bisa import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import (
    CAR_BRANDS, YEARS, PRICE_BINS, BIN_LABELS,
    brand_to_index, year_to_index, price_to_bin,
    generate_showroom_data, save_results_to_file
)

def sequential_analyze(data):
    """
    Menghitung tiga histogram secara sekuensial.
    data: list of tuples (brand, year, price)
    return: (brand_hist, year_hist, price_hist)
    """
    n_brands = len(CAR_BRANDS)
    n_years = len(YEARS)
    n_price_bins = len(PRICE_BINS) - 1

    brand_hist = [0] * n_brands
    year_hist = [0] * n_years
    price_hist = [0] * n_price_bins

    for brand, year, price in data:
        brand_hist[brand_to_index(brand)] += 1
        year_hist[year_to_index(year)] += 1
        price_hist[price_to_bin(price)] += 1

    return brand_hist, year_hist, price_hist

def save_golden_output(data, filename="results/golden_freq.txt"):
    """Simpan output sequential sebagai golden reference."""
    brand, year, price = sequential_analyze(data)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# GOLDEN OUTPUT - AutoFreq Sequential\n\n")
        f.write("## Merek\n")
        for i, b in enumerate(CAR_BRANDS):
            f.write(f"{b}: {brand[i]}\n")
        f.write("\n## Tahun\n")
        for i, y in enumerate(YEARS):
            f.write(f"{y}: {year[i]}\n")
        f.write("\n## Harga\n")
        for i, label in enumerate(BIN_LABELS):
            f.write(f"{label}: {price[i]}\n")
    print(f"Golden output saved to {filename}")

if __name__ == "__main__":
    print("Generating 5 million records...")
    data = generate_showroom_data(5_000_000)
    print("Analyzing sequentially...")
    brand, year, price = sequential_analyze(data)
    print("First 3 brand counts:", brand[:3])
    print("First 3 year counts:", year[:3])
    print("Price bins:", price)
    save_golden_output(data)
    print("Sequential done.")