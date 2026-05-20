"""
Sequential histogram implementation.
Menghitung frekuensi nilai dalam list/array.
"""

def sequential_histogram(data, num_bins=256):
    """
    Menghitung histogram secara sekuensial.
    
    Parameters:
    - data: list of int (nilai diharapkan 0..num_bins-1)
    - num_bins: jumlah bin (default 256 untuk grayscale)
    
    Returns:
    - list of int dengan panjang num_bins
    """
    hist = [0] * num_bins
    for value in data:
        if 0 <= value < num_bins:
            hist[value] += 1
    return hist

def save_golden_output(data, filename="results/golden_hist.txt"):
    """Menyimpan output sequential sebagai golden reference."""
    hist = sequential_histogram(data)
    with open(filename, "w") as f:
        f.write(str(hist))
    print(f"Golden output saved to {filename}")

if __name__ == "__main__":
    # Demo: generate data random dan simpan golden output
    import sys
    import os
    # Tambahkan path parent agar bisa import utils
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from utils import generate_random_data
    
    print("Generating random data...")
    data = generate_random_data(10_000_000)  # 10 juta elemen
    print("Computing sequential histogram...")
    hist = sequential_histogram(data)
    print("First 10 bins:", hist[:10])
    
    # Simpan golden reference
    save_golden_output(data)