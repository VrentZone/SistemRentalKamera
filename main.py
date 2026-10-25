import time
from utils import clear_screen, load_json
from auth import registrasi_user, login_user
from kamera import tampilkan_kamera, tambah_kamera, ubah_kamera, hapus_kamera
from transaksi import top_up_saldo, sewa_kamera, pengembalian_kamera, riwayat_user, riwayat_admin

def menu_admin(user_aktif):
    while True:
        clear_screen()
        print("------------------------------------------")
        print(f"   MENU ADMIN RENTAL KAMERA ({user_aktif['username']})")
        print("------------------------------------------")
        print("1. Lihat Daftar Kamera")
        print("2. Tambah Data Kamera Baru")
        print("3. Ubah Data Kamera")
        print("4. Hapus Data Kamera")
        print("5. Laporan Transaksi")
        print("6. Logout")
        print("------------------------------------------")
        pilihan = input("Pilih Menu (1-6) > ").strip()
        
        if pilihan == '1':
            clear_screen()
            print("------------------------------------------")
            print("      DAFTAR KAMERA & ALAT FOTOGRAFI      ")
            print("------------------------------------------")
            tampilkan_kamera()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == '2':
            tambah_kamera()
        elif pilihan == '3':
            ubah_kamera()
        elif pilihan == '4':
            hapus_kamera()
        elif pilihan == '5':
            riwayat_admin()
        elif pilihan == '6':
            print("\n[✓] Logout berhasil...")
            time.sleep(1)
            break
        else:
            print("\n[!] Pilihan menu tidak valid!")
            time.sleep(1)

def menu_user(user_aktif):
    while True:
        users = load_json('data/users.json')
        for u in users:
            if u['username'].lower() == user_aktif['username'].lower():
                user_aktif.update(u)
                break

        clear_screen()
        print("------------------------------------------")
        print(f"    MENU USER RENTAL KAMERA ({user_aktif['username']})")
        print(f"    Saldo E-Money: Rp {user_aktif.get('saldo', 0):,}")
        print("------------------------------------------")
        print("1. Lihat Katalog Kamera Tersedia")
        print("2. Sewa Kamera & Alat")
        print("3. Pengembalian Kamera")
        print("4. Top Up Saldo E-Money")
        print("5. Riwayat Transaksi & Cetak Invoice")
        print("6. Logout")
        print("------------------------------------------")
        pilihan = input("Pilih Menu (1-6) > ").strip()
        
        if pilihan == '1':
            clear_screen()
            print("------------------------------------------")
            print("      KATALOG KAMERA & ALAT FOTOGRAFI     ")
            print("------------------------------------------")
            tampilkan_kamera()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == '2':
            sewa_kamera(user_aktif)
        elif pilihan == '3':
            pengembalian_kamera(user_aktif)
        elif pilihan == '4':
            top_up_saldo(user_aktif)
        elif pilihan == '5':
            riwayat_user(user_aktif)
        elif pilihan == '6':
            print("\n[✓] Logout berhasil...")
            time.sleep(1)
            break
        else:
            print("\n[!] Pilihan menu tidak valid!")
            time.sleep(1)

def main():
    while True:
        clear_screen()
        print("------------------------------------------")
        print("  SISTEM MANAGEMENT RENTAL KAMERA (CLI)   ")
        print("  Project Akhir Dasar Pemrograman 2026   ")
        print("------------------------------------------")
        print("1. Login Akun")
        print("2. Registrasi User Baru")
        print("3. Keluar Aplikasi")
        print("------------------------------------------")
        pilihan = input("Pilih Menu (1-3) > ").strip()
        
        if pilihan == '1':
            user = login_user()
            if user:
                if user.get('role') == 'admin':
                    menu_admin(user)
                else:
                    menu_user(user)
        elif pilihan == '2':
            registrasi_user()
        elif pilihan == '3':
            print("\n[✓] Terima kasih telah menggunakan Sistem Rental Kamera CLI!")
            break
        else:
            print("\n[!] Pilihan menu tidak valid!")
            time.sleep(1)

if __name__ == "__main__":
    main()
