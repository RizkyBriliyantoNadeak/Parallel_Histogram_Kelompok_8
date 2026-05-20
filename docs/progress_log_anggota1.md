# Progress Log – Anggota 1 (Nama: Andi)

## 2026-05-17 (Minggu 3 – Hari 1)
**Dikerjakan:**
- Setup struktur folder proyek di VS Code.
- Membuat file sequential_histogram.py dan menguji dengan data kecil.
- Menulis fungsi generate_random_data di utils.py.

**Kendala:**
- Tidak ada.

**Rencana besok:**
- Implementasi parallel_histogram dengan multiprocessing.
- Membuat unit test pertama (correctness).

**Commit:**
- feat: add sequential histogram and utils
- chore: init project structure

## 2026-05-18 (Hari 2)
**Dikerjakan:**
- Selesai parallel_histogram dengan multiprocessing.
- Membuat test_histogram.py dengan 5 test case.
- Semua test PASS.

**Kendala:**
- Sempat terjadi error karena chunk terakhir tidak terbagi rata. Sudah diperbaiki dengan penanganan sisa data.

**Rencana besok:**
- Menambahkan test edge cases (kosong, satu elemen).
- Membuat benchmark script (run_benchmark.py).

**Commit:**
- feat: implement parallel histogram with multiprocessing
- test: add unit tests for correctness and edge cases

## 2026-05-19 (Hari 3)
**Dikerjakan:**
- Menambahkan test untuk determinism dan berbagai jumlah worker.
- Membuat script benchmark (run_benchmark.py) untuk mengukur speedup.
- Update README dengan instruksi lengkap.

**Kendala:**
- Tidak ada.

**Rencana W4:**
- Visualisasi histogram dengan matplotlib.
- Profiling dan optimasi lebih lanjut.

**Commit:**
- test: add parametrized tests and determinism check
- feat: add benchmark script
- docs: update README and progress log