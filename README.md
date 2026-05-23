# AutoFreq – Analisis Frekuensi Paralel Stok Showroom Mobil

## Deskripsi
AutoFreq adalah sistem untuk menganalisis inventaris showroom mobil secara **paralel** menggunakan teknik **parallel histogram**. Program menghitung distribusi frekuensi berdasarkan:
- Merek mobil
- Tahun produksi
- Rentang harga

Dengan data besar (jutaan record), proses paralel memanfaatkan multi-core CPU sehingga analisis menjadi cepat (speedup > 3x pada 4 core).

## Cara Instalasi
1. Pastikan Python 3.8+ terinstal.
2. Clone repositori atau buat folder proyek.
3. Buka terminal di folder root proyek.
4. (Opsional) Buat virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows