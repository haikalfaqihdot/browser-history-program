from utils.display import (
    print_separator, print_info,
    CYAN, BOLD, DIM, GREEN, YELLOW, RED, RESET, WHITE
)


def search_history(browser, keyword: str):
    """
    Cari history berdasarkan judul atau URL (case-insensitive).
    Mendukung pencarian multi-kata (semua kata harus ada).
    """
    history = browser.history.get_all()

    if not history:
        print_info("History kosong, tidak ada yang bisa dicari.")
        return

    kw_lower = keyword.lower()
    words    = kw_lower.split()

    results = []
    for url, title, timestamp in history:
        haystack = (url + " " + title).lower()
        if all(w in haystack for w in words):
            results.append((url, title, timestamp))

    print_separator()
    print(f"  {BOLD}Hasil pencarian untuk:{RESET} {CYAN}\"{keyword}\"{RESET}")
    print_separator()

    if not results:
        print_info(f"Tidak ada hasil untuk \"{keyword}\".")
        return

    print(f"  {DIM}Ditemukan {len(results)} item:{RESET}\n")

    for i, (url, title, timestamp) in enumerate(results, 1):
        # Highlight keyword dalam judul & url
        h_title = _highlight(title, words)
        h_url   = _highlight(url,   words)

        print(f"  {CYAN}{i:2}.{RESET}  {BOLD}{h_title}{RESET}")
        print(f"        {DIM}🌐 {h_url}{RESET}")
        print(f"        {DIM}🕒 {timestamp}{RESET}")
        print()


def _highlight(text: str, words: list) -> str:
    """Bungkus kata yang cocok dengan warna kuning."""
    result = text
    for w in words:
        idx = result.lower().find(w)
        while idx != -1:
            original = result[idx: idx + len(w)]
            replacement = f"{YELLOW}{BOLD}{original}{RESET}"
            result = result[:idx] + replacement + result[idx + len(w):]
            # Lanjut pencarian setelah replacement (lebih panjang dari aslinya)
            idx = result.lower().find(w, idx + len(replacement))
    return result