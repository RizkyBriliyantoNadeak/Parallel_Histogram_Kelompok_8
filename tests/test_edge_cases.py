import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parallel_analyzer import parallel_analyze
from src.sequential_analyzer import sequential_analyze
from src.utils import CAR_BRANDS, YEARS

def test_out_of_range_price():
    data = [("Toyota", 2020, 1200)]
    seq = sequential_analyze(data)
    par = parallel_analyze(data, n_workers=2)
    assert seq == par
    # bin terakhir (500-1000) seharusnya dapat 1
    assert seq[2][-1] == 1

def test_all_same_brand():
    data = [("Honda", 2022, 250)] * 1000
    seq = sequential_analyze(data)
    par = parallel_analyze(data, n_workers=4)
    assert seq == par
    assert seq[0][CAR_BRANDS.index("Honda")] == 1000
    assert seq[1][YEARS.index(2022)] == 1000