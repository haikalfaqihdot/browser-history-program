from utils.display import print_success, print_info, print_warning


def go_back(browser):
    """
    Navigasi mundur satu halaman.
    Hapus halaman teratas (current), kembalikan halaman sebelumnya.
    Stack tidak menyimpan duplikat URL, jadi pop saja item teratas.
    """
    history = browser.history.get_all()

    if len(history) <= 1:
        print_info("Tidak ada halaman sebelumnya.")
        return None

    # Hapus current page
    browser.history.pop()

    # Peek halaman sebelumnya (sekarang jadi top)
    prev = browser.history.peek()
    return prev


def clear_history(browser):
    """Hapus seluruh riwayat browsing."""
    count = browser.history.size()
    browser.history.clear()
    print_success(f"{count} item riwayat berhasil dihapus!")