from getpass import getpass
from time import sleep
from mail.login import connect, read_mail
from app.app_state import AppState


def main(): 
    app_state = AppState()
    app_state.load_settings()

    server = input("Server Domain : ")
    username = input("Username : ")
    password = getpass("Password : ")

    connect(server, username, password, app_state, True)
    while True:
        sleep(10)
        l = connect(server, username, password, app_state)
        if l != []:
            app_state.load_array()
            read_mail(l, app_state)
            app_state.save_array()
            print(app_state.data_array)
        

if __name__ == '__main__':
    main()