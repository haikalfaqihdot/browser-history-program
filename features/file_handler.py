import os

DATA_FOLDER = "data"
USER_FILE = os.path.join(DATA_FOLDER, "users.txt")


def init():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    if not os.path.exists(USER_FILE):
        open(USER_FILE, 'w').close()


def register(username):
    init()

    with open(USER_FILE, 'r') as f:
        users = [u.strip() for u in f]

    if username in users:
        return False

    with open(USER_FILE, 'a') as f:
        f.write(username + "\n")

    open(os.path.join(DATA_FOLDER, f"{username}.txt"), 'w').close()
    return True


def login(username):
    if not os.path.exists(USER_FILE):
        return False

    with open(USER_FILE, 'r') as f:
        users = [u.strip() for u in f]

    return username in users

def load_history(username, stack):
    path = os.path.join(DATA_FOLDER, f"{username}.txt")

    if not os.path.exists(path):
        return

    with open(path, 'r') as f:
        for line in f:
            if "|" in line:
                url, title = line.strip().split("|")
                stack.push_unique((url, title))