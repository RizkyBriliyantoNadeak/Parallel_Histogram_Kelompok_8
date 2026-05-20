"""
Unit testing untuk sequential dan parallel histogram.
Pastikan hasil paralel == sequential, edge cases, determinism.
"""

import pytest
import random
import sys
import os

# Tambahkan path src agar bisa import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from sequential_histogram import sequential_histogram
from parallel_histogram import parallel_histogram
from utils import generate_random_data

# Fixture untuk data kecil yang konsisten
@pytest.fixture
def small_data():
    return [0, 1, 2, 2, 3, 3, 3, 255, 255, 100, 50]

# Test 1: Correctness dengan data kecil
def test_correctness_small(small_data):
    seq = sequential_histogram(small_data)
    par = parallel_histogram(small_data, n_workers=2)
    assert seq == par, "Parallel result berbeda dengan sequential!"

# Test 2: Data random berukuran sedang
def test_correctness_random():
    data = generate_random_data(100_000)
    seq = sequential_histogram(data)
    par = parallel_histogram(data, n_workers=4)
    assert seq == par

# Test 3: Edge case - data kosong
def test_empty_data():
    empty = []
    seq = sequential_histogram(empty)
    par = parallel_histogram(empty, n_workers=3)
    assert seq == par
    assert all(v == 0 for v in par)  # semua bin 0

# Test 4: Edge case - satu elemen
def test_single_element():
    data = [42]
    seq = sequential_histogram(data)
    par = parallel_histogram(data, n_workers=2)
    assert seq == par
    assert par[42] == 1
    assert sum(par) == 1

# Test 5: Nilai di luar rentang (harus diabaikan)
def test_out_of_range():
    data = [-10, 256, 1000, 5, 5]
    seq = sequential_histogram(data)
    par = parallel_histogram(data, n_workers=2)
    assert seq == par
    # Hanya nilai 5 yang tercatat (2 kali)
    assert seq[5] == 2
    assert sum(seq) == 2

# Test 6: Non-determinism (hasil paralel harus sama tiap run)
def test_determinism():
    data = generate_random_data(10_000)
    r1 = parallel_histogram(data, n_workers=4)
    r2 = parallel_histogram(data, n_workers=4)
    assert r1 == r2

# Test 7: Berbagai jumlah worker (1,2,4,8)
@pytest.mark.parametrize("workers", [1, 2, 4, 8])
def test_different_workers(workers):
    data = generate_random_data(50_000)
    seq = sequential_histogram(data)
    par = parallel_histogram(data, n_workers=workers)
    assert seq == par

# Test 8: Data dengan semua nilai yang sama
def test_uniform_data():
    data = [100] * 1000
    seq = sequential_histogram(data)
    par = parallel_histogram(data, n_workers=4)
    assert seq == par
    assert seq[100] == 1000