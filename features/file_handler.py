import os

# ─── PATHS ──────────────────────────────────────────────────────────────────────
DATA_DIR   = os.path.join(os.path.dirname(__file__), "..", "data")
USERS_FILE = os.path.join(DATA_DIR, "users.txt")

os.makedirs(DATA_DIR, exist_ok=True)


def _history_path(username: str) -> str:
    return os.path.join(DATA_DIR, f"{username}.txt")


# ─── AUTH ───────────────────────────────────────────────────────────────────────
def _load_users() -> set:
    if not os.path.exists(USERS_FILE):
        return set()
    with open(USERS_FILE, "r") as f:
        # Simpan dalam lowercase agar perbandingan case-insensitive
        return {line.strip().lower() for line in f if line.strip()}


def register(username: str) -> bool:
    users = _load_users()
    # Cek duplikat tanpa memperhatikan huruf besar/kecil
    if username.lower() in users:
        return False
    with open(USERS_FILE, "a") as f:
        f.write(username + "\n")
    return True


def login(username: str) -> bool:
    # Login juga case-insensitive
    return username.lower() in _load_users()


# ─── HISTORY PERSISTENCE ────────────────────────────────────────────────────────
def save_history(username: str, stack) -> None:
    path = _history_path(username)
    with open(path, "w") as f:
        for url, title, timestamp in stack.get_all():
            f.write(f"{url}|{title}|{timestamp}\n")


def load_history(username: str, stack) -> None:
    path = _history_path(username)
    if not os.path.exists(path):
        return
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # File ditulis terbaru di baris pertama (karena get_all() urutan terbaru dulu)
    # Untuk restore ke stack dengan index 0 = terbaru,
    # kita baca dari baris TERAKHIR (terlama) dan push satu per satu
    # → setiap push insert ke index 0, jadi yang terakhir di-push = terbaru = index 0 ✅
    for line in reversed(lines):
        parts = line.split("|")
        if len(parts) == 3:
            url, title, timestamp = parts
            stack.push((url, title, timestamp))
