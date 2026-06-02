"""
test_dashboard.py
Memastikan modul dashboard tidak error saat diimport.
"""

def test_dashboard_import():
    try:
        import scripts.dashboard  # noqa
    except ImportError as e:
        assert False, f"Gagal import dashboard: {e}"