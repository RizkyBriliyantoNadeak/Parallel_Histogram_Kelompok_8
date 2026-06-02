"""
test_stress_w4.py
Menguji apakah program mampu menangani data besar tanpa error memori.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import generate_showroom_data
from src.parallel_analyzer import parallel_analyze

@pytest.mark.slow
def test_large_data_10million():
    data = generate_showroom_data(10_000_000)
    # Cukup pastikan tidak error
    result = parallel_analyze(data, n_workers=4)
    assert len(result[0]) == 10  # jumlah merek
    assert sum(result[0]) == 10_000_000

# Untuk menjalankan test lambat: pytest -m slow