"""
test_correctness_after_optimization.py
Memastikan bahwa setelah optimasi (jika ada), output paralel tetap sama dengan sequential.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sequential_analyzer import sequential_analyze
from src.parallel_analyzer import parallel_analyze
from src.utils import generate_showroom_data

@pytest.fixture(params=[10_000, 100_000, 500_000])
def test_data(request):
    """Data kecil hingga sedang untuk pengujian cepat."""
    return generate_showroom_data(request.param)

@pytest.mark.parametrize("workers", [2, 4, 8])
def test_optimized_parallel_vs_sequential(test_data, workers):
    seq = sequential_analyze(test_data)
    par = parallel_analyze(test_data, n_workers=workers)
    assert seq == par, f"Output berbeda untuk workers={workers}"

def test_consistency_across_runs():
    """Pastikan determinisme setelah optimasi."""
    data = generate_showroom_data(200_000)
    result1 = parallel_analyze(data, n_workers=4)
    result2 = parallel_analyze(data, n_workers=4)
    assert result1 == result2