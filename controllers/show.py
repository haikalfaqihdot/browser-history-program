from utils.display import (
    print_separator, print_info, print_header,
    CYAN, BOLD, DIM, GREEN, YELLOW, RESET, WHITE, RED
)


def show_history(browser):
    """Tampilkan seluruh riwayat browsing dalam format tabel ringkas."""
    history = browser.history.get_all()

    print_header("RIWAYAT BROWSING")

    if not history:
        print_info("History kosong.")
        return

    print(f"  {DIM}Total: {len(history)} halaman tercatat{RESET}\n")

    for i, (url, title, timestamp) in enumerate(history, 1):
        marker = f"{GREEN}●{RESET}" if i == 1 else f"{DIM}○{RESET}"
        tag    = f"  {CYAN}{BOLD}SEKARANG{RESET}" if i == 1 else ""

        print(f"  {marker}  {CYAN}{i:2}.{RESET}  {BOLD}{title:<22}{RESET}{tag}")
        print(f"        {DIM}🌐 {url}{RESET}")
        print(f"        {DIM}🕒 {timestamp}{RESET}")
        print()

    print_separator()
    print(f"  {DIM}● = Halaman terakhir dikunjungi{RESET}")