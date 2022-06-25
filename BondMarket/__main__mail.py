from datetime import datetime
from time import sleep
import mail.get_mail as get_mail
from app.app_state import AppState, process_exists, create_all_dir
from log.log_file import Log_file
import threading
import os

MESSAGE = (
    'Mail Serviece is now running. Please do not use the app '
    'and the service at the same time, otherwise conflicts may '
    'occur. You can add new users via the app. You can find'
    'output in the log folder'
)


def check_state():
    input('To Exit press ENTER')


def mainloop():
    create_all_dir()
    os.system('cls' if os.name == 'nt' else 'clear')
    t = threading.Thread(target=check_state)
    app_state = AppState()
    app_state.load_settings()
    log = Log_file()
    server = f"imap.{app_state.settings['main_service']['server']}"
    username = app_state.settings["main_service"]["user"]
    password = app_state.settings["main_service"]["psw"]
    if process_exists('BondMarket.exe'):
        print('Mail service cannot be used when BondMarket is running.')
        t.start()
        while t.is_alive():
            pass
        return
    print('Loading...')
    log.initialize(application='MS')
    if get_mail.test_connection(server, username, password):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(MESSAGE)
        print('User:')
        for user in app_state.settings["app_settings"]["persons_mames"].values():
            print(f'    {user}')
        log.print_('root', f'____Connected!____')
        t.start()
        while True and t.is_alive():
            if int(datetime.today().strftime('%S')) % 15 == 0:
                get_mail.connect(app_state, log)
        log.print_('root', f'__logout__')
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Error! Check your settings in the app')
        log.print_('root', f'____Error!____')
        sleep(5)


if __name__ == '__main__':
    mainloop()
