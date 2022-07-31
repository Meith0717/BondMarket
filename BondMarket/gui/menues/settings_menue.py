from json import load
from time import sleep
from tkinter import filedialog
import messagebox.messagebox as msg
import tkinter
import customtkinter as ctk
from customtkinter.theme_manager import ThemeManager
from customtkinter import appearance_mode_tracker
from app.app_state import AppState, APP_VERSION
from webbrowser import open
import mail.get_mail as get_mail
import requests
import threading
from mail.get_mail import connect
import mail.send_mail as send_mail

#### Main Settings ####

def author_frame(main_root: ctk.CTk) -> None:
    root = ctk.CTkFrame(main_root)
    root.pack(side='top', anchor='w', padx=10, pady=10)

    ctk.CTkLabel(root, text='Author: Thierry Meiers', text_font=('Segoe UI', 15)).grid(
        row=0, columns=2, column=0, padx=5, pady=5, sticky='w')
    ctk.CTkLabel(root, text='Discord:         ').grid(
        row=1, column=0, padx=5, pady=5)
    ctk.CTkButton(root, text='meith0717#8799', command=lambda: open(
        'https://discordapp.com/users/773830054726860811/'), height=15).grid(row=1, column=1, padx=5, pady=5)
    
    
def file_settings(main_root: ctk.CTk, app_state: AppState) -> None:
    
    def open_file(app_state: AppState) -> None:
        old_path: str = app_state.settings['app_settings']['file_path']
        path: str = filedialog.askopenfilename(title='BondMarket', filetypes=[('Pickle', '*.pkl')])
        if app_state.save_state is False:
            app_state.save_array() if msg.want_to_save(app_state.settings['app_settings']['file_path']) else None
        app_state.settings['app_settings']['file_path'] = path if path != '' else old_path
        app_state.load_array()

    def new_file() -> None:
        old_path: str = app_state.settings['app_settings']['file_path']
        path: str = filedialog.asksaveasfilename(title='BondMarket', filetypes=[('Pickle', '*.pkl')])
        if app_state.save_state is False:
            app_state.save_array() if msg.want_to_save(app_state.settings['app_settings']['file_path']) else None
        app_state.settings['app_settings']['file_path'] = path if path != '' else old_path

        app_state.data_array=[]
        app_state.save_array()

    
    root = ctk.CTkFrame(main_root)
    root.pack(side='top', padx=10, pady=10, fill='x')

    ctk.CTkLabel(root, text='File Settings',
                 text_font=('Segoe UI', 15),
                 width=100
                 ).grid(row=0, column=0, padx=5, pady=5)

    ctk.CTkButton(root, text='Open File', command=lambda: open_file(app_state)).grid(
        row=1, column=0, pady=10, padx=10, sticky='w')
    ctk.CTkButton(root, text='New File', command=new_file).grid(
        row=1, column=1, pady=10, padx=10, sticky='w')
    ctk.CTkButton(root, text='Create Backup', command=lambda: app_state.save_backup()).grid(
        row=2, column=0, pady=10, padx=10, sticky='w')
    ctk.CTkButton(root, text='Restore Backup', state=tkinter.DISABLED).grid(
        row=2, column=1, pady=10, padx=10, sticky='w')


def appearance_settings(app_root: ctk.CTk, main_root: ctk.CTk, app_state: AppState) -> None:

    def change_dark_mode_switch(app_state: AppState):
        if dark_mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
            app_state.settings["app_settings"]["appearance"] = "dark"
        else:
            ctk.set_appearance_mode("light")
            app_state.settings["app_settings"]["appearance"] = "light"
        app_root.state('zoomed')

    root = ctk.CTkFrame(main_root)
    root.pack(side='top', fill='x', anchor='w',
              padx=10, pady=10, ipadx=10, ipady=10)

    ctk.CTkLabel(root, text='Appearance Settings',
                 text_font=('Segoe UI', 15)
                 ).pack(side='top', anchor='w', padx=5, pady=5)

    dark_mode_switch = ctk.CTkSwitch(root,
                                     text="Dark Mode",
                                     command=lambda: change_dark_mode_switch(app_state))
    dark_mode_switch.pack(side='top', anchor='w', padx=5, pady=5)
    
    if appearance_mode_tracker.AppearanceModeTracker.appearance_mode == 1:
        dark_mode_switch.select()


def appearance_notes(main_root: ctk.CTk) -> None:
    s1 = '''You can personalize the theme of the app
by changing the values in the
theme/theme.json file but be careful!'''
    s2 = '''The colors are coded in hexadecimal
['light theme', 'dark theme'].'''
    ctk.CTkLabel(main_root, text=s1).pack(side='top', padx=5, pady=5)
    ctk.CTkLabel(main_root, text=s2).pack(side='top', padx=5, pady=5)


def currency_settings(main_root: ctk.CTk, app_state: AppState) -> None:
    
    def change_currency(value, app_state: AppState) -> None:
        app_state.settings["app_settings"]["currency"] = value
    
    root = ctk.CTkFrame(main_root)
    root.pack(side='top', padx=10, pady=10, fill='x')
    
    ctk.CTkLabel(root, text='Currency Settings',
                 text_font=('Segoe UI', 15)
                 ).pack(side='top', anchor='w', padx=5, pady=5)
    
    e1 = ctk.CTkComboBox(root, values=['\u20ac', '\u0024', '\u00A3', '\u00A5'], command=lambda value: change_currency(value, app_state))
    e1.pack(side='top', anchor='w', padx=10, pady=10)
    e1.set(app_state.settings["app_settings"]["currency"])


def user_settings(main_root: ctk.CTk, app_state: AppState) -> None:

    def show_mail(app_state: AppState, name: str) -> None:
        if name == '':
            linked_mail.configure(text='Select Person')
        else:
            mail = app_state.settings['app_settings']['persons_mames'][name]
            if mail == '':
                linked_mail.configure(text='No mail found!')
            else:
                linked_mail.configure(text=app_state.settings['app_settings']['persons_mames'][name])
            
    def add_user(app_state: AppState):
        name = e1.get()
        if name == '':
            msg.enter_name()
            return
        if name not in app_state.settings['app_settings']['persons_mames'].keys():
            app_state.settings['app_settings']['persons_mames'][name] = ''
            msg.was_added(name)
            e1.configure(values=list(app_state.settings['app_settings']['persons_mames'].keys()))
            e1.set('')
        elif name in app_state.settings['app_settings']['persons_mames'].keys():
            msg.name_exist()
    
    def remove_user(app_state: AppState):
        name = e1.get()
        if name == '':
            msg.enter_name()
        if name in app_state.settings['app_settings']['persons_mames']:
            del app_state.settings['app_settings']['persons_mames'][name]
            msg.was_removed(name)
            e1.configure(values=list(app_state.settings['app_settings']['persons_mames'].keys()))
            e1.set('')
        else:
            msg.name_does_not_exist()
            
    root = ctk.CTkFrame(main_root)
    root.pack(side='top', padx=10, pady=10, fill='x')
    
    ctk.CTkLabel(root, text='User Settings',
                 text_font=('Segoe UI', 15)
                 ).grid(row=0, column=0, columns=1, padx=5, pady=5)
    
    linked_mail = ctk.CTkLabel(root, text='', width=160)
    linked_mail.grid(row=2, column=0)
    
    e1 = ctk.CTkComboBox(root, values=list(app_state.settings['app_settings']['persons_mames'].keys()),
                         command=lambda value : show_mail(app_state, value), width=160)
    e1.grid(row=1, column=0, columns=1, padx=10, pady=10)
    e1.set('')
    
    ctk.CTkButton(root, text='add',
                  command=lambda : add_user(app_state)
                  ).grid(row=1, column=1, padx=10, pady=10)
    ctk.CTkButton(root, text='delete',
                  command=lambda : remove_user(app_state)
                  ).grid(row=2, column=1, padx=10, pady=10)
    
    ctk.CTkLabel(root, text='Add a new user without email, the email can be entered\nlater under the setting Mail Service -> User.'
                 ).grid(row=3, column=0, columns=2, padx=5, pady=5)
    
#### Mail Service Settings ####


def mail_user_settings(main_root: ctk.CTk, app_state: AppState) -> None:
    
    def loading_animation():
        stage: int = 0
        while t1.is_alive():
            if stage == 0:
                add_user_.configure(text='Loading.      ')
                stage += 1
            elif stage == 1:
                add_user_.configure(text='Loading..     ')
                stage += 1
            elif stage == 2:
                add_user_.configure(text='Loading...    ')
                stage += 1
            elif stage == 3:
                add_user_.configure(text='Loading....   ')
                stage = 0
            sleep(0.4)
        add_user_.configure(text='Add')

    def wait_for_answer() -> None:
        counter: int = 0
        while connect(app_state, "login_command") is False:
            sleep(10)
            counter += 1
            if counter == 6:
                break
    
    def add_user(app_state: AppState):
        name = e1.get()
        mail = e2.get()
        if mail == '':
            t1.start()
            t2.start()
            return
        if mail not in app_state.settings['app_settings']['persons_mames'].values():
            if send_mail.login_mail(mail, name, app_state):
                msg.send_mail(mail)
                t1.start()
                t2.start()
                e2.delete(0, 'end')
            else:
                msg.invalide_mail()
        elif mail in app_state.settings['app_settings']['persons_mames'].values():
            msg.mail_exist()
        else:
            msg.unknown_error() 
            
    root = ctk.CTkFrame(main_root)
    root.pack(side='top', padx=10, pady=10, fill='x')
    t1 = threading.Thread(target=(lambda: wait_for_answer()))
    t2 = threading.Thread(target=(lambda: loading_animation()))

    ctk.CTkLabel(root, text='User Settings',
                 text_font=('Segoe UI', 15)
                 ).grid(row=0, column=0, columns=1, padx=5, pady=5)
    
    ctk.CTkLabel(root, text='E-Mail:').grid(row=2, column=0, padx=10, pady=10)
    ctk.CTkLabel(root, text='Name:').grid(row=1, column=0, padx=10, pady=10)

    e1 = ctk.CTkComboBox(root, width=200, values=list(list(app_state.settings['app_settings']['persons_mames'].keys())))
    e1.grid(row=1, column=1, padx=10, pady=10)
    e1.set("")
    e2 = ctk.CTkEntry(root, width=200)
    e2.grid(row=2, column=1, padx=10, pady=10)
    add_user_ = ctk.CTkButton(root, text='Add/Check for login', command=lambda: add_user(app_state))
    add_user_.grid(row=3, column=0, padx=10, pady=10)
    
    ctk.CTkLabel(root, text='Send a confirmation mail to a user or not user.\nFor this an email account must be given below.'
                 ).grid(row=4, column=0, columns=2, padx=5, pady=5)
    

def mail_service_settings(main_root: ctk.CTk, app_state: AppState) -> None:

    def check_conection():
        server = f"imap.{e1.get()}"
        username = e2.get()
        password = e3.get()
        print(server, username, password)
        if get_mail.test_connection(server, username, password):
            app_state.settings["main_service"]["server"] = e1.get()
            app_state.settings["main_service"]["user"] = e2.get()
            app_state.settings["main_service"]["psw"] = e3.get()
            b1.configure(text='Conneced!', text_color="#2ECC71")
        else:
            b1.configure(text='Error!', text_color="#C0392B")

    root = ctk.CTkFrame(main_root)
    root.pack(side='top', padx=10, pady=10, fill='x')
    
    ctk.CTkLabel(root, text='Test Conection',
                 text_font=('Segoe UI', 15)
                 ).grid(row=0, column=0, columns=1, padx=5, pady=5)
    
    ctk.CTkLabel(root, text='Server:'
                 ).grid(row=1, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='User:'
                 ).grid(row=2, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='Password:'
                 ).grid(row=3, column=0, pady=5, padx=20, sticky='e')
    
    e1 = ctk.CTkEntry(root, width=200)
    e2 = ctk.CTkEntry(root, width=200)
    e3 = ctk.CTkEntry(root, width=200, show='*')
    
    e1.grid(row=1, column=1, pady=5, padx=10)
    e2.grid(row=2, column=1, pady=5, padx=10)
    e3.grid(row=3, column=1, pady=5, padx=10)
    
    if app_state.settings["main_service"]["server"] != '':
        e1.insert(0, app_state.settings["main_service"]["server"])
    else:
        e1.insert(0, 'gmail.com')
    e2.insert(0, app_state.settings["main_service"]["user"])
    e3.insert(0, app_state.settings["main_service"]["psw"])

    b1 = ctk.CTkButton(root, text='Check Connection', command=lambda: check_conection())
    b1.grid(row=4, column=1, pady=5, padx=10)
    
    s = '''Do not enter your personal email account.
Please create an email only for this app.
(The mailbox will be deleted regularly)
Gmail is best choice'''
    ctk.CTkLabel(root, text=s
                 ).grid(row=5, column=0, columns=2, padx=5, pady=5)
    
    
def main_service_notes(main_root: ctk.CTk) -> None:
    s1 = 'Please do not use the mail service and bondmarked\nat the same time as this may cause conflicts.'
    ctk.CTkLabel(main_root, text=s1).pack(side='top', padx=10, pady=10, fill='x')


def check_for_update() -> None:
    request: str = requests.get("https://api.github.com/repos/MeiTh0717/BondMarket/releases/latest").json()['tag_name']
    request = request.removeprefix('v')
    print(APP_VERSION, request)
    if APP_VERSION < request:
        msg.older_version()
    else:
        msg.newest_version()


def draw_menue_3(main_root, app_state: AppState):

    global root
    
    root = ctk.CTkFrame(main_root,
        fg_color=ThemeManager.theme['color']['window_bg_color'])
    author_frame(root)
    
    column1 = ctk.CTkFrame(root,
                           fg_color=ThemeManager.theme['color']['window_bg_color'])
    ctk.CTkLabel(column1, text='Main Settings',
                 text_font=('Segoe UI', 15)
                 ).pack(side='top', padx=5, pady=5)
    
    column2 = ctk.CTkFrame(root,
                           fg_color=ThemeManager.theme['color']['window_bg_color'])
    ctk.CTkLabel(column2, text='Mail Service Settings',
                 text_font=('Segoe UI', 15)
                 ).pack(side='top', padx=5, pady=5)
    
    column3 = ctk.CTkFrame(root,
                           fg_color=ThemeManager.theme['color']['window_bg_color'])
    ctk.CTkLabel(column3, text='',
                 text_font=('Segoe UI', 15)
                 ).pack(side='top', padx=5, pady=5)

    column4 = ctk.CTkFrame(root,
                           fg_color=ThemeManager.theme['color']['window_bg_color'])
    ctk.CTkLabel(column4, text='',
                 text_font=('Segoe UI', 15)
                 ).pack(side='top', padx=5, pady=5)
    
    column1.pack(side='left', anchor='w', fill='both', padx=5, pady=5)
    column2.pack(side='left', anchor='w', fill='both', padx=5, pady=5)
    column3.pack(side='left', anchor='w', fill='both', padx=5, pady=5)
    column4.pack(side='left', anchor='w', fill='both', padx=5, pady=5)
    
    ctk.CTkButton(root, text="Check for Update", command=check_for_update).pack(side='bottom', anchor='e', padx=10, pady=10)
    
    user_settings(column1, app_state)
    file_settings(column1, app_state)
    currency_settings(column1, app_state)
    appearance_settings(main_root, column1, app_state)
    appearance_notes(column1)
    
    mail_user_settings(column2, app_state)
    mail_service_settings(column2, app_state)
    main_service_notes(column2)
    
    root.pack(padx=20, pady=20, fill='both', expand=True)


def destroy_menue_3():
    try:
        root.destroy()
    except:
        pass
