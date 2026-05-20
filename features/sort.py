from utils.display import (
    print_success, print_info, print_error,
    CYAN, BOLD, DIM, RESET, print_separator
)


# ─── BUBBLE SORT ────────────────────────────────────────────────────────────────
def _bubble_sort(data: list, key_fn, reverse: bool = False) -> list:
   
    arr = list(data)        
    n   = len(arr)

    for i in range(n):
        swapped = False       # hentikan lebih awal jika sudah terurut

        # Setiap putaran, elemen terbesar ke posisi paling akhir
        # sehingga panjang bagian yang perlu diperiksa berkurang 1 tiap putaran (- i)
        for j in range(0, n - 1 - i):
            a = key_fn(arr[j])
            b = key_fn(arr[j + 1])

            # menentukan apakah perlu swap berdasarkan arah sort
            should_swap = (a > b) if not reverse else (a < b)

            if should_swap:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:       # tidak ada swap → seluruh list sudah terurut
            break

    return arr



def _parse_time(ts: str) -> tuple:
    
    #Konversi 'DD-MM-YYYY HH:MM:SS' → tuple integer agar bisa dibandingkan.
    #Contoh: '13-05-2026 10:30:00' → (2026, 5, 13, 10, 30, 0)
    
    try:
        date_part, time_part = ts.split(" ")
        d, m, y  = date_part.split("-")
        h, mi, s = time_part.split(":")
        return (int(y), int(m), int(d), int(h), int(mi), int(s))
    except Exception:
        return (0, 0, 0, 0, 0, 0)


# ─── MAIN SORT FUNCTION ─────────────────────────────────────────────────────────
def sort_history(browser, mode: str):
    """
    Urutkan history menggunakan Bubble Sort.
    mode:
      "1" → waktu terbaru dulu  (desc timestamp)
      "2" → waktu terlama dulu  (asc  timestamp)
      "3" → judul A–Z           (asc  string)
      "4" → judul Z–A           (desc string)
    """
    history = browser.history.get_all()

    if not history:
        print_info("History kosong, tidak ada yang bisa diurutkan.")
        return

    if mode == "1":
        sorted_data = _bubble_sort(history, key_fn=lambda x: _parse_time(x[2]), reverse=True)
        label = "Terbaru Dulu"
    elif mode == "2":
        sorted_data = _bubble_sort(history, key_fn=lambda x: _parse_time(x[2]), reverse=False)
        label = "Terlama Dulu"
    elif mode == "3":
        sorted_data = _bubble_sort(history, key_fn=lambda x: x[1].lower(), reverse=False)
        label = "Judul A–Z"
    elif mode == "4":
        sorted_data = _bubble_sort(history, key_fn=lambda x: x[1].lower(), reverse=True)
        label = "Judul Z–A"
    else:
        print_error("Pilihan sort tidak valid!")
        return

    # Tulis hasil kembali ke stack (index 0 = elemen pertama hasil sort)
    browser.history.clear()
    browser.current_index = 0
    for item in sorted_data:
        browser.history.push(item)
    # push() menyisipkan di depan, jadi balik urutannya agar index 0 = sorted_data[0]
    browser.history.data = sorted_data

    print_success(f"History diurutkan dengan Bubble Sort: {label}")

    print()
    print_separator()
    for i, (url, title, ts) in enumerate(browser.history.get_all(), 1):
        print(f"  {CYAN}{i:2}.{RESET}  {BOLD}{title:<22}{RESET}  {DIM}{ts}{RESET}")
    print_separator()