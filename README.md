# 📷 Sistem Manajemen Rental Kamera & Alat Fotografi (CLI)

> **Project Akhir (PA) Dasar-Dasar Pemrograman Python 2026**  
> *Sistem Rental Kamera Berbasis Modular CLI & JSON Database*

Aplikasi manajemen rental kamera berbasis *Command Line Interface* (CLI) yang dibangun secara modular dalam bahasa pemrograman Python. Sistem ini mendukung *multi-role* (Admin & User), autentikasi aman dengan batas login 3 kali (*lockout system*), pembersih layar otomatis berbasis OS, CRUD penuh inventaris kamera, sistem dompet digital (E-Money), transaksi penyewaan & pengembalian alat dengan pembaruan stok otomatis, ekspor invoice ke file teks, serta penyimpanan data dinamis berbasis file JSON.

---

## 👥 Anggota Kelompok & Pembagian Tugas GitHub

| Nama Anggota | NIM | Username GitHub | Role & Modul Tanggung Jawab |
| :--- | :--- | :--- | :--- |
| **M. Fairuz Firerza Aliushami** | 2609116062 | `@itsraizhu` | **Main Program & System Navigation** (`main.py`, `utils.py`) |
| **Muhammad Fachri Razabi** | 2609116069 | `@Fachri2207` | **Admin & CRUD Inventory Lead** (`kamera.py`, `kamera.json`) |
| **Raisha Achdi Febiandika** | 2609116071 | `@FEBIANDIKA1107` | **Transaction & Billing Lead** (`transaksi.py`, `transaksi.json`, `invoices/`) |
| **Alya Shofa** | 2609116077 | `@alyashofaaa15-cloud` | **Authentication & Documentation Lead** (`auth.py`, `users.json`, Laporan) |

---

## 🚀 Fitur Unggulan Sistem

### 🔑 1. Autentikasi & Keamanan (`auth.py`)
- [x] **Multi-Role Login**: Membedakan hak akses dan antarmuka antara **Admin** dan **User**.
- [x] **Keamanan Password**: Menggunakan library `pwinput` untuk menyembunyikan karakter password saat diketik.
- [x] **Lockout System**: Batas percobaan login maksimal 3 kali jika password/username salah.
- [x] **Registrasi User Baru**: Validasi username tidak boleh duplikat (*case-insensitive*) dan validasi panjang minimal 4 karakter.

### 📷 2. Manajemen Inventaris Kamera / CRUD (`kamera.py`)
- [x] **Create**: Menambahkan data kamera/alat fotografi baru (ID unik, Nama, Kategori, Harga Sewa/hari, Stok) dengan validasi angka > 0.
- [x] **Read**: Menampilkan katalog/tabel inventaris lengkap yang rapi menggunakan `PrettyTable`.
- [x] **Update**: Memperbarui detail harga sewa dan jumlah stok kamera.
- [x] **Delete**: Menghapus data alat dari katalog dengan konfirmasi keamanan (`y/n`).

### 💳 3. Transaksi, Sewa & E-Money (`transaksi.py`)
- [x] **Top Up Saldo E-Money**: Pengisian saldo akun pengguna dengan validasi nominal minimal Rp 10.000.
- [x] **Penyewaan Alat**: Validasi stok alat, perhitungan otomatis total biaya berdasarkan durasi sewa, pemotongan saldo, serta pengurangan stok alat secara *real-time*.
- [x] **Pengembalian Alat**: Mengembalikan alat yang sedang disewa, mengubah status menjadi "Selesai", mencatat waktu pengembalian, dan merestok unit alat secara otomatis.
- [x] **Riwayat Transaksi**: User dapat melihat rekam jejak sewa pribadi, sedangkan Admin dapat memantau seluruh laporan transaksi rental pelanggan.
- [x] **Invoice & Ekspor Struk**: Menampilkan struk pembayaran detail serta fitur ekspor bukti transaksi ke file teks (`.txt`) di folder `invoices/`.

### 🛠️ 4. Navigasi & Utilitas (`main.py` & `utils.py`)
- [x] **Menu Terintegrasi**: Alur menu dinamis yang memisahkan dashboard Admin dan dashboard User.
- [x] **Pembersih Layar OS**: Fungsi `clear_screen()` otomatis (`cls` untuk Windows, `clear` untuk Linux/macOS).
- [x] **Robust Error Handling**: Penanganan `try-except` (`ValueError`, `FileNotFoundError`, `JSONDecodeError`) agar program berjalan stabil tanpa *crash*.
- [x] **Penyimpanan Dinamis JSON**: Otomatis membaca, memvalidasi, dan menyimpan perubahan ke file JSON (`users.json`, `kamera.json`, `transaksi.json`).

---

## 📁 Struktur Repositori Project

```text
SistemRentalKamera/
├── data/
│   ├── kamera.json          # Database inventaris kamera & alat
│   ├── transaksi.json       # Database riwayat transaksi rental
│   └── users.json           # Database akun user & admin beserta saldo
├── invoices/                # Folder penyimpanan file ekspor invoice (.txt)
├── auth.py                  # Modul login, registrasi, & validasi user
├── kamera.py                # Modul CRUD inventaris kamera (Admin)
├── main.py                  # Entry point utama program & navigasi menu
├── transaksi.py             # Modul transaksi, sewa, top up, & invoice
├── utils.py                 # Modul pembersih layar & operasi file JSON
└── README.md                # Dokumentasi lengkap proyek
```

---

## 💻 Akun Pengujian (Default Test Accounts)

| Role | Username | Password | Saldo Awal | Keterangan |
| :--- | :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | - | Akses penuh CRUD kamera & Laporan Transaksi |
| **User** | `user1` | `user1234` | - | Akses sewa, pengembalian, top up & invoice |

---

## 📜 Lisensi & Keterangan
Proyek ini dibuat untuk memenuhi tugas **Project Akhir (PA) Praktikum Dasar-Dasar Pemrograman Python 2026**.
