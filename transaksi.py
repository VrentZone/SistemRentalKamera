import os
import time
from datetime import datetime
from prettytable import PrettyTable
from utils import clear_screen, load_json, save_json
from kamera import tampilkan_kamera

FILE_TRANSAKSI = 'data/transaksi.json'
FILE_USERS = 'data/users.json'
FILE_KAMERA = 'data/kamera.json'

def perbarui_saldo_user(username, saldo_baru):
    users = load_json(FILE_USERS)
    for u in users:
        if u['username'] == username:
            u['saldo'] = saldo_baru
            break
    save_json(FILE_USERS, users)

def simpan_invoice_txt(trx):
    try:
        os.makedirs("invoices", exist_ok=True)
        file_path = f"invoices/invoice_{trx['id_transaksi']}.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("==========================================\n")
            f.write("          INVOICE RENTAL KAMERA           \n")
            f.write("==========================================\n")
            f.write(f"ID Transaksi   : {trx['id_transaksi']}\n")
            f.write(f"Tanggal Sewa   : {trx['tanggal_sewa']}\n")
            tgl_kembali = trx.get('tanggal_kembali')
            if tgl_kembali and tgl_kembali != "-":
                f.write(f"Tanggal Kembali: {tgl_kembali}\n")
            elif trx.get('status') == "Disewa":
                f.write(f"Tanggal Kembali: - (Sedang Disewa)\n")
            f.write(f"Penyewa        : {trx['username']}\n")
            f.write(f"ID Alat        : {trx['id_kamera']}\n")
            f.write(f"Nama Alat      : {trx['nama_kamera']}\n")
            f.write(f"Harga / Hari   : Rp {trx['harga_sewa']:,}\n")
            f.write(f"Durasi Sewa    : {trx['lama_hari']} Hari\n")
            f.write(f"Total Bayar    : Rp {trx['total_biaya']:,}\n")
            f.write(f"Status Sewa    : {trx['status']}\n")
            f.write(f"Metode Bayar   : Saldo E-Money (LUNAS)\n")
            f.write("==========================================\n")
            f.write("   Terima kasih telah menyewa kamera!     \n")
            f.write("==========================================\n")
        return file_path
    except Exception as e:
        print(f"\n[!] Gagal menyimpan file invoice: {e}")
        return None

def cetak_invoice(trx):
    clear_screen()
    print("------------------------------------------")
    print("          INVOICE RENTAL KAMERA           ")
    print("------------------------------------------")
    print(f"ID Transaksi   : {trx['id_transaksi']}")
    print(f"Tanggal Sewa   : {trx['tanggal_sewa']}")
    tgl_kembali = trx.get('tanggal_kembali')
    if tgl_kembali and tgl_kembali != "-":
        print(f"Tanggal Kembali: {tgl_kembali}")
    elif trx.get('status') == "Disewa":
        print("Tanggal Kembali: - (Sedang Disewa)")
    print(f"Penyewa        : {trx['username']}")
    print(f"ID Alat        : {trx['id_kamera']}")
    print(f"Nama Alat      : {trx['nama_kamera']}")
    print(f"Harga / Hari   : Rp {trx['harga_sewa']:,}")
    print(f"Durasi Sewa    : {trx['lama_hari']} Hari")
    print(f"Total Bayar    : Rp {trx['total_biaya']:,}")
    print(f"Status Sewa    : {trx['status']}")
    print(f"Metode Bayar   : Saldo E-Money (LUNAS)")
    print("------------------------------------------")
    print("   Simpan struk ini sebagai bukti sewa    ")
    print("------------------------------------------")
    
    simpan = input("\nSimpan / Ekspor invoice ke file .txt? (y/n): ").strip().lower()
    if simpan == 'y':
        path = simpan_invoice_txt(trx)
        if path:
            print(f"[✓] Invoice berhasil disimpan di: {path}")

def top_up_saldo(user_aktif):
    clear_screen()
    print("------------------------------------------")
    print("             TOP UP SALDO E-MONEY         ")
    print("------------------------------------------")
    print(f"Saldo saat ini : Rp {user_aktif.get('saldo', 0):,}")
    print("------------------------------------------")
    
    try:
        nominal_str = input("Masukkan nominal Top Up (Rp): ").strip()
        nominal = int(nominal_str)
        if nominal < 10000:
            print("\n[!] Minimal Top Up adalah Rp 10,000!")
            time.sleep(1.5)
            return
            
        konfirm = input(f"Konfirmasi Top Up sebesar Rp {nominal:,}? (y/n): ").strip().lower()
        if konfirm == 'y':
            saldo_baru = user_aktif.get('saldo', 0) + nominal
            user_aktif['saldo'] = saldo_baru
            perbarui_saldo_user(user_aktif['username'], saldo_baru)
            print(f"\n[✓] Top Up berhasil! Saldo baru: Rp {saldo_baru:,}")
        else:
            print("\n[-] Top Up dibatalkan.")
    except ValueError:
        print("\n[!] Input nominal harus berupa angka!")
        
    time.sleep(1.5)

def sewa_kamera(user_aktif):
    clear_screen()
    print("------------------------------------------")
    print("              SEWA KAMERA & ALAT          ")
    print("------------------------------------------")
    tampilkan_kamera()
    kamera_list = load_json(FILE_KAMERA)
    
    if not kamera_list:
        time.sleep(1.5)
        return
        
    id_kamera = input("\nMasukkan ID Alat yang ingin disewa: ").strip().upper()
    kamera_terpilih = None
    for k in kamera_list:
        if k['id'] == id_kamera:
            kamera_terpilih = k
            break
            
    if not kamera_terpilih:
        print("\n[!] ID Alat tidak ditemukan!")
        time.sleep(1.5)
        return
        
    if kamera_terpilih['stok'] <= 0:
        print("\n[!] Maaf, stok alat ini sedang habis!")
        time.sleep(1.5)
        return
        
    try:
        lama_hari = int(input("Masukkan lama sewa (dalam hari): ").strip())
        if lama_hari <= 0:
            print("\n[!] Durasi sewa minimal 1 hari!")
            time.sleep(1.5)
            return
            
        total_biaya = lama_hari * kamera_terpilih['harga_sewa']
        saldo_sekarang = user_aktif.get('saldo', 0)
        
        clear_screen()
        print("------------------------------------------")
        print("           DETAIL PENYEWAAN ALAT          ")
        print("------------------------------------------")
        print(f"Alat Disewa    : {kamera_terpilih['nama']}")
        print(f"Harga / Hari   : Rp {kamera_terpilih['harga_sewa']:,}")
        print(f"Lama Sewa      : {lama_hari} Hari")
        print(f"Total Biaya    : Rp {total_biaya:,}")
        print(f"Saldo Anda     : Rp {saldo_sekarang:,}")
        print("------------------------------------------")
        
        if saldo_sekarang < total_biaya:
            kekurangan = total_biaya - saldo_sekarang
            print(f"\n[!] Saldo tidak mencukupi! Kurang Rp {kekurangan:,}")
            print("[!] Silakan lakukan Top Up saldo terlebih dahulu.")
            input("\nTekan Enter untuk kembali...")
            return
            
        konfirmasi = input("Lanjutkan pembayaran sewa? (y/n): ").strip().lower()
        if konfirmasi != 'y':
            print("\n[-] Transaksi penyewaan dibatalkan.")
            time.sleep(1.5)
            return
            
        saldo_baru = saldo_sekarang - total_biaya
        user_aktif['saldo'] = saldo_baru
        perbarui_saldo_user(user_aktif['username'], saldo_baru)
        
        kamera_terpilih['stok'] -= 1
        save_json(FILE_KAMERA, kamera_list)
        
        transaksi_list = load_json(FILE_TRANSAKSI)
        id_transaksi = f"TRX{int(time.time())}"
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        transaksi_baru = {
            "id_transaksi": id_transaksi,
            "username": user_aktif['username'],
            "id_kamera": kamera_terpilih['id'],
            "nama_kamera": kamera_terpilih['nama'],
            "harga_sewa": kamera_terpilih['harga_sewa'],
            "lama_hari": lama_hari,
            "total_biaya": total_biaya,
            "tanggal_sewa": waktu_sekarang,
            "tanggal_kembali": "-",
            "status": "Disewa"
        }
        transaksi_list.append(transaksi_baru)
        save_json(FILE_TRANSAKSI, transaksi_list)
        
        print("\n[✓] Pembayaran berhasil! Alat resmi disewa.")
        time.sleep(1)
        cetak_invoice(transaksi_baru)
        input("\nTekan Enter untuk kembali ke menu...")
        
    except ValueError:
        print("\n[!] Input durasi sewa harus berupa angka!")
        time.sleep(1.5)

def pengembalian_kamera(user_aktif):
    clear_screen()
    print("------------------------------------------")
    print("           PENGEMBALIAN ALAT SEWA         ")
    print("------------------------------------------")
    transaksi_list = load_json(FILE_TRANSAKSI)
    kamera_list = load_json(FILE_KAMERA)
    
    sewa_aktif = [t for t in transaksi_list if t['username'] == user_aktif['username'] and t['status'] == "Disewa"]
    
    if not sewa_aktif:
        print("\n[i] Anda tidak memiliki alat yang sedang disewa.")
        input("\nTekan Enter untuk kembali...")
        return
        
    tabel = PrettyTable()
    tabel.field_names = ["ID Transaksi", "Nama Alat", "Tgl Sewa", "Durasi", "Total"]
    for t in sewa_aktif:
        tabel.add_row([t['id_transaksi'], t['nama_kamera'], t['tanggal_sewa'], f"{t['lama_hari']} Hari", f"Rp {t['total_biaya']:,}"])
    print(tabel)
    
    id_trx = input("\nMasukkan ID Transaksi yang ingin dikembalikan: ").strip()
    trx_ditemukan = None
    for t in sewa_aktif:
        if t['id_transaksi'] == id_trx:
            trx_ditemukan = t
            break
            
    if not trx_ditemukan:
        print("\n[!] ID Transaksi tidak valid atau tidak ditemukan dalam sewa aktif!")
        time.sleep(1.5)
        return
        
    konfirm = input(f"Konfirmasi pengembalian '{trx_ditemukan['nama_kamera']}'? (y/n): ").strip().lower()
    if konfirm == 'y':
        trx_ditemukan['status'] = "Selesai"
        trx_ditemukan['tanggal_kembali'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_json(FILE_TRANSAKSI, transaksi_list)
        
        for k in kamera_list:
            if k['id'] == trx_ditemukan['id_kamera']:
                k['stok'] += 1
                break
        save_json(FILE_KAMERA, kamera_list)
        
        print("\n[✓] Alat berhasil dikembalikan! Terima kasih.")
    else:
        print("\n[-] Pengembalian dibatalkan.")
        
    time.sleep(1.5)

def riwayat_user(user_aktif):
    clear_screen()
    print("------------------------------------------")
    print("        RIWAYAT TRANSAKSI & INVOICE       ")
    print("------------------------------------------")
    transaksi_list = load_json(FILE_TRANSAKSI)
    user_trx = [t for t in transaksi_list if t['username'] == user_aktif['username']]
    
    if not user_trx:
        print("\n[i] Anda belum memiliki riwayat transaksi.")
        input("\nTekan Enter untuk kembali...")
        return
        
    tabel = PrettyTable()
    tabel.field_names = ["ID Transaksi", "Nama Alat", "Durasi", "Total Bayar", "Status"]
    for t in user_trx:
        tabel.add_row([t['id_transaksi'], t['nama_kamera'], f"{t['lama_hari']} Hari", f"Rp {t['total_biaya']:,}", t['status']])
    print(tabel)
    
    pilihan = input("\nMasukkan ID Transaksi untuk cetak Invoice (Enter untuk kembali): ").strip()
    if pilihan:
        trx_pilih = None
        for t in user_trx:
            if t['id_transaksi'] == pilihan:
                trx_pilih = t
                break
        if trx_pilih:
            cetak_invoice(trx_pilih)
            input("\nTekan Enter untuk kembali...")
        else:
            print("\n[!] ID Transaksi tidak ditemukan!")
            time.sleep(1.5)

def riwayat_admin():
    clear_screen()
    print("------------------------------------------")
    print("         LAPORAN TRANSAKSI RENTAL         ")
    print("------------------------------------------")
    transaksi_list = load_json(FILE_TRANSAKSI)
    
    if not transaksi_list:
        print("\n[i] Belum ada transaksi yang tercatat.")
        input("\nTekan Enter untuk kembali...")
        return
        
    tabel = PrettyTable()
    tabel.field_names = ["ID Transaksi", "Penyewa", "Nama Alat", "Durasi", "Total", "Status"]
    for t in transaksi_list:
        tabel.add_row([t['id_transaksi'], t['username'], t['nama_kamera'], f"{t['lama_hari']} Hari", f"Rp {t['total_biaya']:,}", t['status']])
    print(tabel)
    
    pilihan = input("\nMasukkan ID Transaksi untuk cetak Invoice (Enter untuk kembali): ").strip()
    if pilihan:
        trx_pilih = None
        for t in transaksi_list:
            if t['id_transaksi'] == pilihan:
                trx_pilih = t
                break
        if trx_pilih:
            cetak_invoice(trx_pilih)
            input("\nTekan Enter untuk kembali...")
        else:
            print("\n[!] ID Transaksi tidak ditemukan!")
            time.sleep(1.5)
