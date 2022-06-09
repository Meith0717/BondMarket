from app.app_state import AppState
import Mail.send_mail as send_mail
from gui.menues.expenses_menue import update_combox, update_table
from tkinter import messagebox
import imap_tools
import customtkinter as ctk
import threading


def get_commands(app_state: AppState, msg: imap_tools.MailMessage):
    s = msg.subject
    date = msg.date.today().strftime('%Y.%m.%d')
    if 'BondMarket: ' in s:
        s = s.replace('BondMarket: ', '')
        if 'add ' in s:
            if msg.from_ in app_state.settings["app_settings"]["persons_mames"].values():
                person = app_state.settings["app_settings"]["persons_mames"].keys()\
                    [app_state.settings["app_settings"]["persons_mames"].values().index(msg.from_)]
                s = s.replace('add ', '')
                s = s.split(',')
                app_state.append_expenditure(person, float(s[0]), f"{s[1]} - Mail Service", date)
                state.config(text=f'Adding Data...')
                send_mail.confirmation_mail(msg.from_, person, s[0], s[1], date, app_state)
                state.config(text=f'Sending Mail...')
        if 'login ' in s:
            s = s.replace('login ', '')
            if msg.from_ not in app_state.settings["app_settings"]["persons_mames"].values():
                app_state.settings["app_settings"]["persons_mames"][s] = msg.from_
                state.config(text=f'Adding User...')
                send_mail.welcome_mail(msg.from_, s, app_state)
                state.config(text=f'Sending Mail...')
                update_combox(app_state)


def test_connection(server: str, username: str, password: str):
    try:
        imap_tools.MailBox(server).login(username, password)
        return True
    except:
        return False
        

def connect(main_root: ctk.CTk, top_root: ctk.CTkToplevel, app_state: AppState):
    server = f"imap.{app_state.settings['main_service']['server']}"
    username = app_state.settings["main_service"]["user"]
    password = app_state.settings["main_service"]["psw"]
    state.config(text='Try To Connect...')
    if test_connection(server, username, password):
        state.config(text='Connected!')
        app_state.load_array()
        with imap_tools.MailBox(server).login(username, password) as mailbox:
            for msg in mailbox.fetch():
                state.config(text='Loading Mails...')
                get_commands(app_state, msg)
                mailbox.delete(msg.uid)
    else:
        state.config(text='Check your Mail Service Settings!')
        app_state.settings["main_service"]["active"] = False
    top_root.destroy()
    main_root.wm_attributes('-disabled', False)
    app_state.save_array()
    update_table(app_state)
    if app_state.check_names()  is False:
        messagebox.showwarning('BondMarket', 'A user was detected in the table which was not registered ')
 

def loader(main_root: ctk.CTk, app_state: AppState):
    global state
    loading = threading.Thread(target=lambda: connect(main_root, root, app_state))
    root = ctk.CTkToplevel(main_root)
    root.title("BondMarked Mail Serviec")
    root.wm_attributes('-topmost', True)
    main_root.wm_attributes('-disabled', True)
    root.wm_attributes('-disabled', True)
    ctk.CTkLabel(root, text='Mail Service     ', text_font=('Segoe UI', 20)
                 ).grid(row=0, column=0, pady=5, padx=20, sticky='w')
    root.overrideredirect(1)
    window_width = 200
    window_height = 75
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    state = ctk.CTkLabel(root, text='Loading...')
    state.place(rely=0.7, anchor='w')
    loading.start()
