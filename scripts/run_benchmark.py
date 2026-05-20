"""
Benchmark untuk mengukur speedup parallel histogram.
Akan digunakan di minggu 4, tapi bisa dicoba sekarang.
"""

import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from sequential_histogram import sequential_histogram
from parallel_histogram import parallel_histogram
from utils import generate_random_data

def run_benchmark(data_sizes=[1_000_000, 5_000_000, 10_000_000], 
                  worker_counts=[1,2,4,8]):
    """
    Jalankan benchmark untuk berbagai ukuran data dan jumlah worker.
    """
    results = {}
    for size in data_sizes:
        print(f"\n=== Data size: {size} ===")
        data = generate_random_data(size)
        
        # Sequential
        start = time.time()
        seq_hist = sequential_histogram(data)
        seq_time = time.time() - start
        print(f"Sequential: {seq_time:.3f}s")
        
        for workers in worker_counts:
            start = time.time()
            par_hist = parallel_histogram(data, n_workers=workers)
            par_time = time.time() - start
            speedup = seq_time / par_time if par_time > 0 else 0
            print(f"Parallel ({workers} workers): {par_time:.3f}s, speedup: {speedup:.2f}x")
            
            # Verifikasi
            assert seq_hist == par_hist, f"Wrong result for workers={workers}"
            
            results[(size, workers)] = {
                "seq_time": seq_time,
                "par_time": par_time,
                "speedup": speedup
            }
    return results

if __name__ == "__main__":
    print("Starting benchmark...")
    run_benchmark()