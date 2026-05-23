"""
Utilities for generating showroom inventory data and mapping functions.
"""

import random

# ========== Konfigurasi Data ==========
CAR_BRANDS = [
    "Toyota", "Honda", "Suzuki", "Mitsubishi", "Daihatsu",
    "Nissan", "Hyundai", "Mazda", "BMW", "Mercedes"
]

YEARS = list(range(2010, 2026))   # 2010 - 2025

PRICE_BINS = [0, 100, 200, 300, 500, 1000]   # dalam juta rupiah
BIN_LABELS = ["<100jt", "100-200jt", "200-300jt", "300-500jt", "500-1000jt"]

def brand_to_index(brand: str) -> int:
    """Mapping merek ke indeks 0..N-1."""
    return CAR_BRANDS.index(brand)

def year_to_index(year: int) -> int:
    """Mapping tahun ke indeks 0..N-1."""
    return YEARS.index(year)

def price_to_bin(price: int) -> int:
    """
    Mapping harga (dalam juta) ke indeks bin.
    """
    for i in range(len(PRICE_BINS) - 1):
        if PRICE_BINS[i] <= price < PRICE_BINS[i+1]:
            return i
    return len(PRICE_BINS) - 2   # jika >= batas tertinggi

def generate_showroom_data(n_samples: int = 1_000_000):
    """
    Generate data showroom sintetis.
    Return: list of tuples (brand, year, price)
    """
    data = []
    for _ in range(n_samples):
        brand = random.choice(CAR_BRANDS)
        year = random.choice(YEARS)
        price = random.randint(20, 900)   # harga 20-900 juta
        data.append((brand, year, price))
    return data

def save_results_to_file(brand_hist, year_hist, price_hist, filename="results/analysis.txt"):
    """Simpan hasil analisis ke file teks."""
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== DISTRIBUSI MEREK ===\n")
        for i, brand in enumerate(CAR_BRANDS):
            f.write(f"{brand}: {brand_hist[i]} unit\n")
        f.write("\n=== DISTRIBUSI TAHUN ===\n")
        for i, year in enumerate(YEARS):
            f.write(f"{year}: {year_hist[i]} unit\n")
        f.write("\n=== DISTRIBUSI HARGA ===\n")
        for i, label in enumerate(BIN_LABELS):
            f.write(f"{label}: {price_hist[i]} unit\n")
    print(f"Hasil disimpan ke {filename}")