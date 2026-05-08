# Website Pembuatan Surat Flask + MySQL

Fitur:
- Login admin / admin123
- Dashboard seperti admin panel
- SPTJM lengkap 2 halaman + rincian biaya + SPPD rampung
- Laporan Kegiatan
- Nota Dinas
- Surat Pernyataan
- Daftar Pengeluaran Rill
- Arsip surat: preview, edit, hapus, download PDF, print
- Pengaturan akun/reset username dan password tanpa hash
- Tanpa SQLAlchemy, memakai mysql-connector-python

## Cara Install
1. Buat database dengan menjalankan `database.sql` di phpMyAdmin/MySQL.
2. Install dependency:
   pip install -r requirements.txt
3. Edit `DB_CONFIG` di `app.py` sesuai user/password MySQL lokal.
4. Jalankan:
   python app.py
5. Buka browser:
   http://127.0.0.1:5000

## Logo/Kop Surat
Ganti file `static/img/logo.png` dengan logo/kop yang ingin dipakai. Struktur kop surat sudah dibuat di `templates/kop.html`.
