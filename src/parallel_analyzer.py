"""
Parallel version of AutoFreq analyzer using multiprocessing.
"""

import sys
import os
import time
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import (
    CAR_BRANDS, YEARS, PRICE_BINS,
    brand_to_index, year_to_index, price_to_bin,
    generate_showroom_data
)
from src.sequential_analyzer import sequential_analyze

def _worker_analyze(chunk):
    """
    Worker: hitung histogram lokal untuk satu chunk data.
    """
    n_brands = len(CAR_BRANDS)
    n_years = len(YEARS)
    n_price_bins = len(PRICE_BINS) - 1

    brand_hist = [0] * n_brands
    year_hist = [0] * n_years
    price_hist = [0] * n_price_bins

    for brand, year, price in chunk:
        brand_hist[brand_to_index(brand)] += 1
        year_hist[year_to_index(year)] += 1
        price_hist[price_to_bin(price)] += 1

    return brand_hist, year_hist, price_hist

def parallel_analyze(data, n_workers=4):
    """
    Menghitung histogram secara paralel.
    """
    if not data:
        return ([0]*len(CAR_BRANDS), [0]*len(YEARS), [0]*(len(PRICE_BINS)-1))

    # Bagi data menjadi n_workers chunk
    chunk_size = len(data) // n_workers
    chunks = []
    for i in range(n_workers):
        start = i * chunk_size
        end = (i+1) * chunk_size if i < n_workers-1 else len(data)
        chunks.append(data[start:end])

    # Map: proses paralel
    with Pool(processes=n_workers) as pool:
        results = pool.map(_worker_analyze, chunks)

    # Reduce: jumlahkan semua histogram
    total_brand = [0] * len(CAR_BRANDS)
    total_year = [0] * len(YEARS)
    total_price = [0] * (len(PRICE_BINS)-1)

    for brand_h, year_h, price_h in results:
        for i in range(len(total_brand)):
            total_brand[i] += brand_h[i]
        for i in range(len(total_year)):
            total_year[i] += year_h[i]
        for i in range(len(total_price)):
            total_price[i] += price_h[i]

    return total_brand, total_year, total_price

if __name__ == "__main__":
    print("Generating 5 million records for comparison...")
    data = generate_showroom_data(5_000_000)

    # Sequential
    start = time.time()
    seq_brand, seq_year, seq_price = sequential_analyze(data)
    seq_time = time.time() - start
    print(f"Sequential time: {seq_time:.3f}s")

    # Parallel with 4 workers
    start = time.time()
    par_brand, par_year, par_price = parallel_analyze(data, n_workers=4)
    par_time = time.time() - start
    speedup = seq_time / par_time

    # Verifikasi
    assert seq_brand == par_brand, "Brand histogram mismatch!"
    assert seq_year == par_year, "Year histogram mismatch!"
    assert seq_price == par_price, "Price histogram mismatch!"
    print(f"Parallel (4 workers) time: {par_time:.3f}s, speedup: {speedup:.2f}x")
    print("Verification PASSED: Parallel output == Sequential output")