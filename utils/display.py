import os
import sys
import time

# ─── ANSI COLOR CODES ───────────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
ITALIC  = "\033[3m"
UNDER   = "\033[4m"

BLACK   = "\033[30m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"

BG_BLACK  = "\033[40m"
BG_BLUE   = "\033[44m"
BG_CYAN   = "\033[46m"

def color(text, *codes):
    return "".join(codes) + text + RESET


# ─── CLEAR SCREEN ───────────────────────────────────────────────────────────────
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ─── BANNER ─────────────────────────────────────────────────────────────────────
def print_banner():
    banner = f"""
{CYAN}{BOLD}  ██████╗ ██████╗  ██████╗ ██╗    ██╗███████╗███████╗██████╗
  ██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔════╝██╔══██╗
  ██████╔╝██████╔╝██║   ██║██║ █╗ ██║███████╗█████╗  ██████╔╝
  ██╔══██╗██╔══██╗██║   ██║██║███╗██║╚════██║██╔══╝  ██╔══██╗
  ██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝███████║███████╗██║  ██║
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝{RESET}
  {DIM}{'─' * 58}{RESET}
"""
    print(banner)


# ─── SECTION HEADER ─────────────────────────────────────────────────────────────
def print_header(title: str):
    width = 54
    pad = (width - len(title) - 2) // 2
    left = pad
    right = width - len(title) - 2 - left
    print(f"\n  {CYAN}┌{'─' * width}┐{RESET}")
    print(f"  {CYAN}│{RESET}{' ' * left}{BOLD}{WHITE}{title}{RESET}{' ' * right}{CYAN}│{RESET}")
    print(f"  {CYAN}└{'─' * width}┘{RESET}\n")


# ─── MENU ITEMS ─────────────────────────────────────────────────────────────────
def print_menu(options: list):
    """options = list of (key, label, hint)"""
    for key, label, hint in options:
        print(f"  {CYAN}{BOLD}[{key}]{RESET}  {label:<26} {DIM}{hint}{RESET}")


# ─── SEPARATOR ──────────────────────────────────────────────────────────────────
def print_separator(char="─", width=56):
    print(f"  {DIM}{char * width}{RESET}")


# ─── BOX ────────────────────────────────────────────────────────────────────────
def print_box(lines: list, color_code=CYAN):
    width = max(len(l) for l in lines) + 4
    print(f"  {color_code}┌{'─' * width}┐{RESET}")
    for line in lines:
        pad = width - len(line) - 2
        print(f"  {color_code}│ {RESET}{line}{' ' * pad} {color_code}│{RESET}")
    print(f"  {color_code}└{'─' * width}┘{RESET}")


# ─── STATUS MESSAGES ────────────────────────────────────────────────────────────
def print_success(msg: str):
    print(f"\n  {GREEN}{BOLD}✓{RESET}  {msg}")

def print_error(msg: str):
    print(f"\n  {RED}{BOLD}✗{RESET}  {msg}")

def print_info(msg: str):
    print(f"\n  {YELLOW}{BOLD}ℹ{RESET}  {msg}")

def print_warning(msg: str):
    print(f"\n  {YELLOW}{BOLD}⚠{RESET}  {msg}")


# ─── PAGE HEADER ────────────────────────────────────────────────────────────────
def print_page_header(title: str, url: str, timestamp: str):
    print(f"\n  {BG_CYAN}{BLACK}{BOLD}  {'BROWSER':^52}  {RESET}")
    print(f"  {CYAN}{'═' * 56}{RESET}")
    print(f"  {BOLD}{WHITE}  {title}{RESET}")
    print(f"  {DIM}  🌐  {url}{RESET}")
    print(f"  {DIM}  🕒  {timestamp}{RESET}")
    print(f"  {CYAN}{'═' * 56}{RESET}\n")


# ─── LOADING ANIMATION ──────────────────────────────────────────────────────────
def loading_animation(msg: str = "Loading", steps: int = 12):
    frames = ["⠋", "⠙", "⠸", "⠴", "⠦", "⠇"]
    for i in range(steps):
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r  {CYAN}{frame}{RESET}  {msg}...")
        sys.stdout.flush()
        time.sleep(0.07)
    sys.stdout.write(f"\r  {GREEN}✓{RESET}  {msg}... selesai\n")
    sys.stdout.flush()


# ─── TABLE ──────────────────────────────────────────────────────────────────────
def print_table(headers: list, rows: list):
    """Simple fixed-width table"""
    col_w = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_w[i] = max(col_w[i], len(str(cell)))

    sep = "  +" + "+".join("-" * (w + 2) for w in col_w) + "+"
    header_row = "  |" + "|".join(
        f" {BOLD}{CYAN}{h:<{col_w[i]}}{RESET} " for i, h in enumerate(headers)
    ) + "|"

    print(sep)
    print(header_row)
    print(sep)
    for row in rows:
        line = "  |" + "|".join(
            f" {str(cell):<{col_w[i]}} " for i, cell in enumerate(row)
        ) + "|"
        print(line)
    print(sep)