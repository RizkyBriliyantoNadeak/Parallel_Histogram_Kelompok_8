# tests/test_edge_cases.py
# Test kasus batas yang lebih ekstrim

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from parallel_histogram import parallel_histogram
from sequential_histogram import sequential_histogram

def test_very_large_data():
    # Hati-hati dengan memori: gunakan data 10 juta
    data = [0] * 10_000_000 + [255] * 10_000_000
    seq = sequential_histogram(data)
    par = parallel_histogram(data, n_workers=4)
    assert seq == par
    assert seq[0] == 10_000_000
    assert seq[255] == 10_000_000

def test_num_bins_custom():
    data = [0,1,2,3,0,1]
    # Bins = 4
    seq = sequential_histogram(data, num_bins=4)
    par = parallel_histogram(data, num_bins=4, n_workers=2)
    assert seq == par
    assert seq[0] == 2
    assert seq[3] == 1