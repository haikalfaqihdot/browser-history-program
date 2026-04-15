from data_structures.stack import Stack
from features.file_handler import register, login, save_history, load_history
from controllers.show import show_history
from controllers.delete import go_back, clear_history


class Browser:
    def __init__(self, username):
        self.username = username
        self.history = Stack()

# ================= LOGIN =================
def start_menu():

    while True:
        print("\n===== LOGIN MENU =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        pilih = input("Pilih: ")

        if pilih == "1":
            user = input("Username: ")
            if register(user):
                print("Register berhasil!")
            else:
                print("User sudah ada!")

        elif pilih == "2":
            user = input("Username: ")
            if login(user):
                print("Login berhasil!")
                return user
            else:
                print("User tidak ditemukan!")

        elif pilih == "3":
            exit()

# ================= MAIN =================
def main():

    username = start_menu()
    browser = Browser(username)

    load_history(username, browser.history)

    while True:

        print("\n===== MAIN MENU =====")
        print("1. Visit")
        print("2. View History")
        print("3. Clear History")
        print("4. Exit")

        pilih = input("Pilih: ")

        if pilih == "1":
            url, title = choose_url()
            if url:
                open_page(browser, url, title)

        elif pilih == "2":
            show_history(browser)

        elif pilih == "3":
            clear_history(browser)

        elif pilih == "4":
            print("Program selesai")
            break

if __name__ == "__main__":
    main()