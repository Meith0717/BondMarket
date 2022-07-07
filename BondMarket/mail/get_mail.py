from time import sleep
from app.app_state import AppState
from log.log_file import Log_file
import mail.send_mail as send_mail
import imap_tools



def get_commands(app_state: AppState, msg: imap_tools.MailMessage, log: Log_file):
    s = msg.subject
    date = msg.date.today().strftime('%Y.%m.%d')
    app_state.load_array()
    if '-add ' in s:
        if msg.from_ in app_state.settings["app_settings"]["persons_mames"].values():
            person = list(app_state.settings["app_settings"]["persons_mames"].keys())\
                [list(app_state.settings["app_settings"]["persons_mames"].values()).index(msg.from_)]
            s = s.replace('-add ', '')
            s = s.split(',')
            app_state.append_expenditure(person, float(s[0]), f"{s[1]} - Mail Service", date)
            log.print_(msg.from_, f'-add {s[0]},{s[1]}')
            send_mail.confirmation_mail(msg.from_, person, s[0], s[1], date, app_state)
            log.print_('root', f'Mail send to {msg.from_}')
    elif '-login ' in s:
        if msg.from_ not in app_state.settings["app_settings"]["persons_mames"].values():
            s = s.replace('-login ', '')
            app_state.settings["app_settings"]["persons_mames"][s] = msg.from_
            log.print_(msg.from_, f'-login {s}')
            send_mail.welcome_mail(msg.from_, s, app_state)
            log.print_('root', f'Mail send to {msg.from_}')
    elif '-help' in s:
        if msg.from_ in app_state.settings["app_settings"]["persons_mames"].values():
            log.print_('root', f'{msg.from_} need help ...')
    else:
        log.print_('root', f'{msg.from_} unknown command {s}')
    app_state.save_array()
    app_state.save_settings()


def test_connection(server: str, username: str, password: str):
    try:
        imap_tools.MailBox(server).login(username, password)
        return True
    except:
        return False
        

def connect(app_state: AppState, log: Log_file):
    server = f"imap.{app_state.settings['main_service']['server']}"
    username = app_state.settings["main_service"]["user"]
    password = app_state.settings["main_service"]["psw"]
    if test_connection(server, username, password):
        try:
            with imap_tools.MailBox(server).login(username, password) as mailbox:
                for msg in mailbox.fetch():
                    get_commands(app_state, msg, log)
                    mailbox.delete(msg.uid)
        except Exception as e:
            log.print_('root', f'{e}')
    else:
        sleep(5)
