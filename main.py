import os
import time
from datetime import datetime
from data_structures.stack import Stack
from data_structures.linked_list import LinkedList
from features.file_handler import register, login, save_history, load_history
from features.search import search_history
from features.sort import sort_history
from controllers.show import show_history
from controllers.delete import go_back, clear_history
from utils.display import (
    clear_screen, print_banner, print_header, print_menu,
    print_box, print_success, print_error, print_info,
    print_page_header, print_separator, loading_animation,
    color, CYAN, GREEN, YELLOW, RED, MAGENTA, BLUE, RESET, BOLD, DIM
)


class Browser:
    def __init__(self, username):
        self.username = username
        self.history = Stack()
        self.bookmarks = LinkedList()
        # Index posisi halaman yang sedang aktif di dalam stack
        # 0 = paling atas (terbaru). Naik saat back, turun saat visit baru.
        self.current_index = 0


# ================= AUTH =================
def start_menu():
    clear_screen()
    print_banner()

    while True:
        print_header("AUTHENTICATION")
        options = [
            ("1", "Register", "Buat akun baru"),
            ("2", "Login", "Masuk ke akun"),
            ("3", "Exit", "Keluar program"),
        ]
        print_menu(options)

        pilih = input(f"\n  {CYAN}›{RESET} Pilihan: ").strip()

        if pilih == "1":
            print(f"\n  {BOLD}[ REGISTER ]{RESET}")
            user = input(f"  {DIM}Username:{RESET} ").strip()
            if not user:
                print_error("Username tidak boleh kosong!")
            elif register(user):
                print_success(f"Akun '{user}' berhasil dibuat!")
                time.sleep(1)
            else:
                print_error(f"Username '{user}' sudah digunakan!")

        elif pilih == "2":
            print(f"\n  {BOLD}[ LOGIN ]{RESET}")
            user = input(f"  {DIM}Username:{RESET} ").strip()
            if login(user):
                loading_animation(f"Memuat profil {user}")
                print_success(f"Selamat datang kembali, {BOLD}{user}{RESET}!")
                time.sleep(0.8)
                return user
            else:
                print_error(f"Username '{user}' tidak ditemukan!")

        elif pilih == "3":
            clear_screen()
            print(f"\n  {DIM}Sampai jumpa! 👋{RESET}\n")
            exit()
        else:
            print_error("Pilihan tidak valid!")


# ================= PILIH URL =================
def choose_url():
    print_header("PILIH DESTINASI")

    PRESETS = [
        ("1", "Google",    "google.com",    "Google Search"),
        ("2", "Spotify",   "spotify.com",   "Spotify"),
        ("3", "YouTube",   "youtube.com",   "YouTube"),
        ("4", "Instagram", "instagram.com", "Instagram"),
        ("5", "GitHub",    "github.com",    "GitHub"),
        ("6", "Twitter/X", "x.com",         "Twitter / X"),
        ("7", "Custom URL", None,           None),
    ]

    for num, label, _, _ in PRESETS:
        print(f"  {CYAN}{num}.{RESET} {label}")

    print(f"\n  {DIM}(Enter untuk batal){RESET}")
    pilih = input(f"\n  {CYAN}›{RESET} Pilihan: ").strip()

    for num, label, url, title in PRESETS:
        if pilih == num:
            if url is None:
                print(f"\n  {BOLD}[ CUSTOM URL ]{RESET}")
                url   = input(f"  {DIM}URL   :{RESET} ").strip()
                title = input(f"  {DIM}Judul :{RESET} ").strip()
                if not url:
                    print_error("URL tidak boleh kosong!")
                    return None, None
                if not title:
                    title = url
                return url, title
            return url, title

    return None, None


# ================= CREATE PAGE =================
def create_page(url, title):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return (url, title, timestamp)


# ================= OPEN PAGE =================
def open_page(browser, url, title):
    # Saat visit halaman baru dari posisi tengah, potong forward history
    browser.history.data = browser.history.data[browser.current_index:]
    current_page = create_page(url, title)
    browser.history.push(current_page)
    browser.current_index = 0
    save_history(browser.username, browser.history)

    while True:
        clear_screen()

        all_history = browser.history.get_all()
        current_page = all_history[browser.current_index]

        print_page_header(current_page[1], current_page[0], current_page[2])

        can_go_back = browser.current_index < len(all_history) - 1

        print_header("NAVIGASI")

        if can_go_back:
            prev = all_history[browser.current_index + 1]
            options = [
                ("1", f"Back", f"Kembali ke {prev[1]}"),
                ("2", "Main Menu", "Kembali ke menu utama"),
                ("3", "Visit URL Baru", "Buka halaman baru"),
                ("4", "Simpan Bookmark", "Tambah ke bookmark"),
            ]
        else:
            options = [
                ("1", "Main Menu", "Kembali ke menu utama"),
                ("2", "Visit URL Baru", "Buka halaman baru"),
                ("3", "Simpan Bookmark", "Tambah ke bookmark"),
            ]

        print_menu(options)
        pilih = input(f"\n  {CYAN}›{RESET} Pilihan: ").strip()

        if can_go_back:
            if pilih == "1":  # BACK
                # Ambil halaman tujuan sebelum mengubah apapun
                target = all_history[browser.current_index + 1]

                # Buat entri baru dengan timestamp saat ini
                new_entry = create_page(target[0], target[1])

                # Insert di posisi 0 tanpa memotong stack
                # → semua history lama tetap ada
                browser.history.data.insert(0, new_entry)

                # Cursor tetap di 0 karena halaman ini sekarang paling atas
                browser.current_index = 0

                save_history(browser.username, browser.history)

            elif pilih == "2":  # Main Menu
                browser.current_index = 0
                return

            elif pilih == "3":  # Visit URL baru
                new_url, new_title = choose_url()
                if new_url:
                    # Potong dari current_index, push halaman baru
                    browser.history.data = browser.history.data[browser.current_index:]
                    new_page = create_page(new_url, new_title)
                    browser.history.push(new_page)
                    browser.current_index = 0
                    save_history(browser.username, browser.history)

            elif pilih == "4":  # Bookmark
                browser.bookmarks.add(current_page[0], current_page[1])
                print_success(f"'{current_page[1]}' ditambahkan ke bookmark!")
                time.sleep(1)

        else:  # Tidak bisa back (halaman pertama)
            if pilih == "1":  # Main Menu
                browser.current_index = 0
                return

            elif pilih == "2":  # Visit URL baru
                new_url, new_title = choose_url()
                if new_url:
                    browser.history.data = browser.history.data[browser.current_index:]
                    new_page = create_page(new_url, new_title)
                    browser.history.push(new_page)
                    browser.current_index = 0
                    save_history(browser.username, browser.history)

            elif pilih == "3":  # Bookmark
                browser.bookmarks.add(current_page[0], current_page[1])
                print_success(f"'{current_page[1]}' ditambahkan ke bookmark!")
                time.sleep(1)


# ================= BOOKMARK MENU =================
def bookmark_menu(browser):
    clear_screen()
    print_header("BOOKMARKS")

    bookmarks = browser.bookmarks.get_all()
    if not bookmarks:
        print_info("Belum ada bookmark tersimpan.")
        input(f"\n  {DIM}Tekan Enter untuk kembali...{RESET}")
        return

    for i, (url, title) in enumerate(bookmarks, 1):
        print(f"  {CYAN}{i:2}.{RESET} {BOLD}{title:<20}{RESET}  {DIM}{url}{RESET}")

    print_separator()
    print(f"  {DIM}(Enter untuk kembali / ketik nomor untuk mengunjungi){RESET}")
    pilih = input(f"\n  {CYAN}›{RESET} Pilihan: ").strip()

    if pilih.isdigit():
        idx = int(pilih) - 1
        if 0 <= idx < len(bookmarks):
            url, title = bookmarks[idx]
            open_page(browser, url, title)
        else:
            print_error("Nomor tidak valid!")
            time.sleep(1)


# ================= MAIN MENU =================
def main():
    username = start_menu()
    browser = Browser(username)
    load_history(username, browser.history)

    while True:
        clear_screen()
        print_banner()
        print(f"  {DIM}Logged in as:{RESET} {BOLD}{CYAN}{username}{RESET}\n")

        history_count = len(browser.history.get_all())
        bookmark_count = len(browser.bookmarks.get_all())

        print_header("MAIN MENU")
        options = [
            ("1", "Visit URL",        "Buka halaman baru"),
            ("2", "Riwayat Browsing", f"{history_count} halaman tercatat"),
            ("3", "Cari History",     "Cari berdasarkan judul/URL"),
            ("4", "Urutkan History",  "Sort by waktu / judul / URL"),
            ("5", "Bookmarks",        f"{bookmark_count} tersimpan"),
            ("6", "Hapus History",    "Bersihkan semua riwayat"),
            ("7", "Logout / Exit",    "Keluar program"),
        ]
        print_menu(options)

        pilih = input(f"\n  {CYAN}›{RESET} Pilihan: ").strip()

        if pilih == "1":
            url, title = choose_url()
            if url:
                open_page(browser, url, title)

        elif pilih == "2":
            clear_screen()
            show_history(browser)
            input(f"\n  {DIM}Tekan Enter untuk kembali...{RESET}")

        elif pilih == "3":
            clear_screen()
            print_header("CARI HISTORY")
            keyword = input(f"  {CYAN}›{RESET} Kata kunci: ").strip()
            if keyword:
                search_history(browser, keyword)
            input(f"\n  {DIM}Tekan Enter untuk kembali...{RESET}")

        elif pilih == "4":
            clear_screen()
            print_header("URUTKAN HISTORY")
            options_sort = [
                ("1", "Terbaru Dulu",   "Sort by waktu descending"),
                ("2", "Terlama Dulu",   "Sort by waktu ascending"),
                ("3", "Judul A-Z",      "Sort by nama halaman"),
                ("4", "Judul Z-A",      "Sort by nama halaman terbalik"),
            ]
            print_menu(options_sort)
            s = input(f"\n  {CYAN}›{RESET} Pilihan: ").strip()
            sort_history(browser, s)
            input(f"\n  {DIM}Tekan Enter untuk kembali...{RESET}")

        elif pilih == "5":
            bookmark_menu(browser)

        elif pilih == "6":
            clear_screen()
            print_header("HAPUS HISTORY")
            print_info(f"Terdapat {history_count} item di riwayat browsing Anda.")
            konfirm = input(f"\n  {RED}Yakin ingin menghapus semua? (y/n):{RESET} ").strip().lower()
            if konfirm == "y":
                clear_history(browser)
                save_history(browser.username, browser.history)
            else:
                print_info("Penghapusan dibatalkan.")
            time.sleep(1)

        elif pilih == "7":
            clear_screen()
            print(f"\n  {DIM}Sampai jumpa, {username}! {RESET}\n")
            break

        else:
            print_error("Pilihan tidak valid!")
            time.sleep(0.8)


if __name__ == "__main__":
    main()