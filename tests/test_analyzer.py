"""
Unit tests for AutoFreq correctness, edge cases, determinism.
"""

import sys
import os
import pytest

# Tambahkan path ke root proyek
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sequential_analyzer import sequential_analyze
from src.parallel_analyzer import parallel_analyze
from src.utils import generate_showroom_data, CAR_BRANDS, YEARS, BIN_LABELS

@pytest.fixture
def sample_data_small():
    return [
        ("Toyota", 2020, 150),
        ("Honda", 2019, 200),
        ("Toyota", 2020, 150),
        ("Suzuki", 2018, 80),
        ("BMW", 2022, 600),
        ("Toyota", 2020, 150),
        ("Honda", 2021, 250),
    ]

def test_correctness_small(sample_data_small):
    seq = sequential_analyze(sample_data_small)
    par = parallel_analyze(sample_data_small, n_workers=2)
    assert seq == par

def test_correctness_random():
    data = generate_showroom_data(100_000)
    seq = sequential_analyze(data)
    par = parallel_analyze(data, n_workers=4)
    assert seq == par

def test_empty_data():
    empty = []
    seq = sequential_analyze(empty)
    par = parallel_analyze(empty, n_workers=3)
    assert seq == par
    assert all(v == 0 for v in seq[0])
    assert all(v == 0 for v in seq[1])
    assert all(v == 0 for v in seq[2])

def test_single_record():
    data = [("Mercedes", 2025, 800)]
    seq = sequential_analyze(data)
    par = parallel_analyze(data, n_workers=2)
    assert seq == par
    assert seq[0][CAR_BRANDS.index("Mercedes")] == 1
    assert seq[1][YEARS.index(2025)] == 1
    assert seq[2][-1] == 1

def test_determinism():
    data = generate_showroom_data(50_000)
    r1 = parallel_analyze(data, n_workers=4)
    r2 = parallel_analyze(data, n_workers=4)
    assert r1 == r2

@pytest.mark.parametrize("workers", [1, 2, 4])
def test_different_workers(workers):
    data = generate_showroom_data(20_000)
    seq = sequential_analyze(data)
    par = parallel_analyze(data, n_workers=workers)
    assert seq == par