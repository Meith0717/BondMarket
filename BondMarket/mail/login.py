from imap_tools import MailBox, AND
from app.app_state import AppState
import imap_tools


def connect(server: str, user: str, password: str, app_state: AppState, try_ = False) -> list:
    try:
        mailbox = MailBox(f"imap.{server}").login(user, password)
        if try_ is False:
            return list(mailbox.fetch(criteria=AND(from_=[key for key in app_state.settings["app_settings"]["persons_mames"].keys()], seen=False)))
        else:
            print('Connected!')
    except:
        if try_:
            print('Connection Failed!')
        else:
            print('Disconnected!')
            connect(server, user, password)


def read_mail(l: list, app_state: AppState):
    for msg in l:
        msg: imap_tools.MailMessage
        sender = msg.from_
        subject = msg.subject
        text = msg.text.replace('\r\n', '')
        date = msg.date.today().strftime('%Y.%m.%d')

        if subject == 'BondMarket: add':
            l = text.split(',')
            amount = float(l[0].encode('ascii', 'ignore'))
            app_state.append_expenditure(app_state.settings["app_settings"]["persons_mames"][sender], amount, f"{l[1]} - Mail Service", date)

        