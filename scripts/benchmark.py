import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import generate_showroom_data
from src.sequential_analyzer import sequential_analyze
from src.parallel_analyzer import parallel_analyze

def run_benchmark():
    data_sizes = [1_000_000, 5_000_000]
    worker_counts = [1, 2, 4]

    for size in data_sizes:
        print(f"\n{'='*50}")
        print(f"Data size: {size:,} records")
        print(f"{'='*50}")
        data = generate_showroom_data(size)

        start = time.time()
        seq = sequential_analyze(data)
        seq_time = time.time() - start
        print(f"Sequential time: {seq_time:.3f}s")

        for w in worker_counts:
            start = time.time()
            par = parallel_analyze(data, n_workers=w)
            par_time = time.time() - start
            if w == 1:
                assert seq == par
            speedup = seq_time / par_time
            print(f"Parallel ({w} workers): {par_time:.3f}s, speedup: {speedup:.2f}x")

if __name__ == "__main__":
    run_benchmark()