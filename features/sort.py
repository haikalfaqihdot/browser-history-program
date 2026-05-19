from utils.display import print_success, print_info, print_error


def sort_history(browser, mode: str):
    """
    Urutkan history di dalam stack.
    mode:
      "1" → waktu terbaru dulu   (desc timestamp)
      "2" → waktu terlama dulu   (asc  timestamp)
      "3" → judul A–Z
      "4" → judul Z–A
    """
    history = browser.history.get_all()

    if not history:
        print_info("History kosong, tidak ada yang bisa diurutkan.")
        return

    if mode == "1":
        # Format DD-MM-YYYY HH:MM:SS → sortable
        sorted_data = sorted(history, key=lambda x: _parse_time(x[2]), reverse=True)
        label = "Terbaru Dulu"
    elif mode == "2":
        sorted_data = sorted(history, key=lambda x: _parse_time(x[2]))
        label = "Terlama Dulu"
    elif mode == "3":
        sorted_data = sorted(history, key=lambda x: x[1].lower())
        label = "Judul A–Z"
    elif mode == "4":
        sorted_data = sorted(history, key=lambda x: x[1].lower(), reverse=True)
        label = "Judul Z–A"
    else:
        print_error("Pilihan sort tidak valid!")
        return

    # Update stack
    browser.history.clear()
    for item in sorted_data:
        browser.history.push(item)

    print_success(f"History diurutkan: {label}")

    # Tampilkan hasil
    from utils.display import CYAN, BOLD, DIM, RESET, print_separator
    print()
    print_separator()
    for i, (url, title, ts) in enumerate(browser.history.get_all(), 1):
        print(f"  {CYAN}{i:2}.{RESET}  {BOLD}{title:<22}{RESET}  {DIM}{ts}{RESET}")
    print_separator()


def _parse_time(ts: str):
    """
    Konversi 'DD-MM-YYYY HH:MM:SS' ke tuple integer agar bisa dibandingkan.
    """
    try:
        date_part, time_part = ts.split(" ")
        d, m, y = date_part.split("-")
        h, mi, s = time_part.split(":")
        return (int(y), int(m), int(d), int(h), int(mi), int(s))
    except Exception:
        return (0, 0, 0, 0, 0, 0)