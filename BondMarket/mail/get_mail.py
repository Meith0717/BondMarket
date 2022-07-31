from time import sleep
from typing import Literal
from app.app_state import AppState
import mail.send_mail as send_mail
import imap_tools


def add_command(app_state: AppState, msg: imap_tools.MailMessage):
    s = msg.subject
    date = msg.date.today().strftime('%Y.%m.%d')
    if 'add' in s:
        if msg.from_ in app_state.settings["app_settings"]["persons_mames"].values():

            person = list(app_state.settings["app_settings"]["persons_mames"].keys())\
                [list(app_state.settings["app_settings"]["persons_mames"].values()).index(msg.from_)]

            s = s.replace('-add ', '')
            s = s.split(',')

            app_state.append_expenditure(person, float(s[0]), f"{s[1]} - Mail Service", date)

            app_state.log.print_(f"{person} has entered new expenses: {float(s[0])}, {s[1]}")


def login_command(app_state: AppState, msg: imap_tools.MailMessage) -> bool:
    s = msg.subject
    if 'login' in s:
        if msg.from_ not in app_state.settings["app_settings"]["persons_mames"].values():
            s = s.replace('-login ', '')
            app_state.settings["app_settings"]["persons_mames"][s] = msg.from_
            send_mail.welcome_mail(msg.from_, s, app_state)
            app_state.log.print_(f"New User Mail Adress: {msg.from_}")
            return True
    return False


def test_connection(server: str, username: str, password: str):
    try:
        imap_tools.MailBox(server).login(username, password)
        return True
    except:
        return False
        

def connect(app_state: AppState, command: Literal["add_command", "login_command"]) -> bool:
    server = f"imap.{app_state.settings['main_service']['server']}"
    username = app_state.settings["main_service"]["user"]
    password = app_state.settings["main_service"]["psw"]
    state: bool = False
    if server == '' or username == '' or password == '':
        return
    if test_connection(server, username, password):
        app_state.log.print_(f"Connected with {username}@{password}")
        try:
            with imap_tools.MailBox(server).login(username, password) as mailbox:
                for msg in list(mailbox.fetch()):
                    if command == "add_command":
                        add_command(app_state, msg)
                    elif command == "login_command":
                        state = login_command(app_state, msg)
                    mailbox.delete(msg.uid)
        except Exception as error:
            app_state.log.print_(error)
    else:
        sleep(5)
    return state
