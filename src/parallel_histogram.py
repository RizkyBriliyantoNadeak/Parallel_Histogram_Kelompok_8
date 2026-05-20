"""
Parallel histogram using Python's multiprocessing.
Strategi: bagi data menjadi chunk, setiap worker hitung histogram lokal,
          lalu gabungkan (merge) di master.
"""

from multiprocessing import Pool
import numpy as np

def _worker_histogram(chunk, num_bins=256):
    """
    Worker: menghitung histogram untuk satu chunk data.
    Dijalankan di proses terpisah.
    """
    local_hist = [0] * num_bins
    for val in chunk:
        if 0 <= val < num_bins:
            local_hist[val] += 1
    return local_hist

def parallel_histogram(data, num_bins=256, n_workers=4):
    """
    Menghitung histogram secara paralel.
    
    Parameters:
    - data: list of int
    - num_bins: jumlah bin
    - n_workers: jumlah proses paralel
    
    Returns:
    - list of int (histogram global)
    """
    if not data:
        return [0] * num_bins
    
    # Bagi data menjadi n_workers bagian (approx sama rata)
    chunk_size = len(data) // n_workers
    chunks = []
    for i in range(n_workers):
        start = i * chunk_size
        end = (i+1) * chunk_size if i < n_workers-1 else len(data)
        chunks.append(data[start:end])
    
    # Map: jalankan worker secara paralel
    with Pool(processes=n_workers) as pool:
        results = pool.starmap(_worker_histogram, 
                               [(chunk, num_bins) for chunk in chunks])
    
    # Reduce: jumlahkan semua histogram lokal
    final_hist = [0] * num_bins
    for local in results:
        for i in range(num_bins):
            final_hist[i] += local[i]
    
    return final_hist

if __name__ == "__main__":
    import sys
    import os
    import time
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from utils import generate_random_data
    from sequential_histogram import sequential_histogram
    
    print("Generating data...")
    data = generate_random_data(5_000_000)
    
    # Sequential
    start = time.time()
    seq_hist = sequential_histogram(data)
    seq_time = time.time() - start
    
    # Parallel dengan 4 worker
    start = time.time()
    par_hist = parallel_histogram(data, n_workers=4)
    par_time = time.time() - start
    
    # Verifikasi
    assert seq_hist == par_hist, "Parallel result != sequential!"
    print(f"Sequential time: {seq_time:.3f}s")
    print(f"Parallel (4 workers) time: {par_time:.3f}s")
    print(f"Speedup: {seq_time/par_time:.2f}x")