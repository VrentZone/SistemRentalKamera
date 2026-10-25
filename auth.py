import time
import pwinput
from utils import clear_screen, load_json, save_json

FILE_USERS = 'data/users.json'

def registrasi_user():
    clear_screen()
    print("----------------------------------------")
    print("         REGISTRASI AKUN USER           ")
    print("----------------------------------------")
    users = load_json(FILE_USERS)
    
    username = input("Masukkan Username Baru (min 4 karakter): ")
    if len(username) < 4:
        print("\n[!] Username terlalu pendek! Minimal 4 karakter.")
        time.sleep(1.5)
        return False

    for user in users:
        if user['username'].lower() == username.lower():
            print("\n[!] Username sudah terdaftar! Gunakan username lain.")
            time.sleep(1.5)
            return False

    password = pwinput.pwinput("Masukkan Password (min 4 karakter): ")
    if len(password) < 4:
        print("\n[!] Password terlalu pendek! Minimal 4 karakter.")
        time.sleep(1.5)
        return False

    user_baru = {
        "username": username,
        "password": password,
        "role": "user",
        "saldo": 0
    }
    users.append(user_baru)
    if save_json(FILE_USERS, users):
        print("\n[✓] Registrasi Berhasil! Silakan Login.")
    else:
        print("\n[!] Gagal menyimpan data user baru.")
    time.sleep(1.5)
    return True

def login_user():
    users = load_json(FILE_USERS)
    percobaan = 0
    
    while percobaan < 3:
        clear_screen()
        print("----------------------------------------")
        print("             LOGIN SISTEM               ")
        print("----------------------------------------")
        username = input("Username: ")
        password = pwinput.pwinput("Password: ")
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                print(f"\n[✓] Login Berhasil! Selamat datang, {username}.")
                time.sleep(1)
                return user
        
        percobaan += 1
        sisa = 3 - percobaan
        if sisa > 0:
            print(f"\n[!] Username atau Password salah! Sisa percobaan: {sisa}")
            time.sleep(1.5)
    
    print("\n[!] Anda telah salah memasukkan akun 3 kali. Akses terkunci sementara.")
    time.sleep(2)
    return None
