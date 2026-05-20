"""
Utility functions: generate data, load from file, etc.
"""

import random
import numpy as np

def generate_random_data(size=10_000_000, min_val=0, max_val=255):
    """
    Generate list of random integers between min_val and max_val (inclusive).
    """
    return [random.randint(min_val, max_val) for _ in range(size)]

def generate_numpy_data(size=10_000_000, min_val=0, max_val=255):
    """Generate numpy array random (lebih hemat memori)."""
    return np.random.randint(min_val, max_val+1, size=size, dtype=np.uint8)

def load_data_from_image(path):
    """
    (Optional) Baca gambar grayscale dan ubah ke list of int.
    Memerlukan PIL atau OpenCV.
    """
    try:
        from PIL import Image
        img = Image.open(path).convert('L')  # grayscale
        data = list(img.getdata())
        return data
    except ImportError:
        raise ImportError("PIL (Pillow) not installed. Install with: pip install Pillow")

def save_histogram_to_file(hist, filename):
    """Simpan histogram ke file teks (satu baris)."""
    with open(filename, "w") as f:
        f.write(str(hist))

def load_histogram_from_file(filename):
    """Load histogram dari file yang disimpan."""
    with open(filename, "r") as f:
        content = f.read()
        # eval aman karena isinya list of int
        return eval(content)