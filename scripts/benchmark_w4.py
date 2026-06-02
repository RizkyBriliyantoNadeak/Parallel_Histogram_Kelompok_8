"""
benchmark_w4.py
Benchmark sistematis untuk W4: mengukur speedup dan efisiensi.
Menyimpan hasil ke CSV dan membuat grafik otomatis.
"""

import sys
import os
import time
import csv
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import generate_showroom_data
from src.sequential_analyzer import sequential_analyze
from src.parallel_analyzer import parallel_analyze

# Konfigurasi
DATA_SIZES = [10_000_000, 50_000_000, 100_000_000]  # 10jt, 50jt, 100jt
WORKERS = [1, 2, 4, 8]
REPEAT = 3  # ulang 3 kali lalu rata-rata
OUTPUT_CSV = "results/benchmark_w4.csv"
OUTPUT_PLOT = "results/speedup_w4.png"

def run_benchmark():
    results = []
    for size in DATA_SIZES:
        print(f"\n=== Generate data {size:,} records ===")
        data = generate_showroom_data(size)
        
        for workers in WORKERS:
            print(f"  Testing dengan {workers} worker...")
            times = []
            for r in range(REPEAT):
                start = time.time()
                if workers == 1:
                    # sequential
                    brand, year, price = sequential_analyze(data)
                else:
                    brand, year, price = parallel_analyze(data, n_workers=workers)
                elapsed = time.time() - start
                times.append(elapsed)
            avg_time = sum(times) / REPEAT
            results.append({
                "data_size": size,
                "workers": workers,
                "avg_time": avg_time,
                "min_time": min(times),
                "max_time": max(times)
            })
            print(f"    Rata-rata waktu: {avg_time:.3f}s")

    # Simpan ke CSV
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["data_size", "workers", "avg_time", "min_time", "max_time"])
        writer.writeheader()
        writer.writerows(results)
    print(f"\nHasil benchmark disimpan ke {OUTPUT_CSV}")

    # Hitung speedup berdasarkan sequential (workers=1) untuk tiap ukuran data
    # Buat grafik
    plt.figure(figsize=(10, 6))
    for size in DATA_SIZES:
        subset = [r for r in results if r["data_size"] == size]
        seq_time = next(r["avg_time"] for r in subset if r["workers"] == 1)
        workers = [r["workers"] for r in subset if r["workers"] != 1]
        speedups = [seq_time / r["avg_time"] for r in subset if r["workers"] != 1]
        plt.plot(workers, speedups, marker='o', label=f"{size//1_000_000} juta")
    
    plt.xlabel("Jumlah Worker")
    plt.ylabel("Speedup")
    plt.title("Speedup vs Jumlah Worker (AutoFreq W4)")
    plt.axhline(y=1, color='gray', linestyle='--')
    plt.grid(True)
    plt.legend()
    plt.savefig(OUTPUT_PLOT, dpi=150)
    plt.show()
    print(f"Grafik speedup disimpan ke {OUTPUT_PLOT}")

if __name__ == "__main__":
    run_benchmark()