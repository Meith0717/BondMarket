from cgitb import text
from tkinter import messagebox
import customtkinter as ctk
from customtkinter.theme_manager import ThemeManager
from customtkinter import appearance_mode_tracker
from app.app_state import AppState
from webbrowser import open
import Mail.get_mail as get_mail
import Mail.send_mail as send_mail


def draw_info_frame(main_root) -> None:
    root = ctk.CTkFrame(main_root)
    root.pack(side='top', anchor='w', padx=10, pady=10, ipadx=10, ipady=10)

    ctk.CTkLabel(root, text='Thierry Meiers   ', text_font=('Segoe UI', 18)).grid(
        row=0, columns=2, column=0, padx=5, pady=5, sticky='w')
    ctk.CTkLabel(root, text='Discord:         ').grid(
        row=1, column=0, padx=5, pady=5)
    ctk.CTkButton(root, text='meith0717#8799', command=lambda: open(
        'https://discordapp.com/users/773830054726860811/'), height=15).grid(row=1, column=1, padx=5, pady=5)


def appearance_frame(main_root, app_state: AppState):

    def change_dark_mode_switch(app_state: AppState):
        if dark_mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
            app_state.settings["app_settings"]["appearance"] = "dark"
        else:
            ctk.set_appearance_mode("light")
            app_state.settings["app_settings"]["appearance"] = "light"

    root = ctk.CTkFrame(main_root)
    root.pack(side='top', fill='x', anchor='w',
              padx=10, pady=10, ipadx=10, ipady=10)

    title = ctk.CTkLabel(root, text='Appearance Settings',
                         text_font=('Segoe UI', 15))
    title.pack(side='top', anchor='w', padx=5, pady=5)

    dark_mode_switch = ctk.CTkSwitch(
        master=root, text="Dark Mode", command=lambda: change_dark_mode_switch(app_state))
    if appearance_mode_tracker.AppearanceModeTracker.appearance_mode == 1:
        dark_mode_switch.select()
    dark_mode_switch.pack(side='top', anchor='w', padx=5, pady=5)

    s1 = 'You can personalize the theme of the app by changing the values in the theme/theme.json file but be careful!'
    s2 = "The colors are coded in hexadecimal -> ['light theme', 'dark theme']."
    ctk.CTkLabel(root, text=s1).pack(side='top', anchor='w', padx=5, pady=5)
    ctk.CTkLabel(root, text=s2).pack(side='top', anchor='w', padx=5, pady=5)


def table_settings_frame(main_root, app_state: AppState):

    def change_currency(value, app_state: AppState):
        app_state.settings["app_settings"]["currency"] = value

    def add_user(app_state: AppState):
        name = e2.get()
        mail = e3.get()
        if name == '':
            messagebox.showerror('BondMarket', 'Please enter Name')
        if mail not in app_state.settings['app_settings']['persons_mames'].values()\
            and name not in app_state.settings['app_settings']['persons_mames']:
            if mail != '' and app_state.settings['main_service']['active']:
                if send_mail.login_mail(mail, name, app_state):
                    messagebox.showinfo('BondMarket', 'Mail has been send!')
                else:
                    messagebox.showinfo('BondMarket', 'Error!') 
            else:
                app_state.settings['app_settings']['persons_mames'][name] = ''
                messagebox.showinfo('BondMarket', 'User has been added')
        elif mail not in app_state.settings['app_settings']['persons_mames'].values()\
            and name in app_state.settings['app_settings']['persons_mames']:
            if send_mail.login_mail(mail, name, app_state):
                messagebox.showinfo('BondMarket', 'Mail has been send!')
            else:
                messagebox.showinfo('BondMarket', 'Error!') 
        else:
            messagebox.showerror('BondMarket', 'User already exist!')
        e2.delete(0, 'end')
        e3.delete(0, 'end')

    def remove_user(app_state: AppState):
        name = e2.get()
        mail = e3.get()
        if name == '':
            messagebox.showerror('BondMarket', 'Please enter Name')
        if name in app_state.settings['app_settings']['persons_mames']:
            del app_state.settings['app_settings']['persons_mames'][name]
            messagebox.showinfo('BondMarket', 'User has been removed!')
        else:
            messagebox.showerror('BondMarket', 'User doesent exist!')
        e2.delete(0, 'end')
        e3.delete(0, 'end')

    root = ctk.CTkFrame(main_root)
    root.pack(side='top', fill='x', anchor='w',
              padx=10, pady=10, ipadx=10, ipady=10)

    title = ctk.CTkLabel(root, text='Table Settings',
                        text_font=('Segoe UI', 15))
    title.grid(row=0, column=0, padx=5, pady=5)

    ctk.CTkLabel(root, text='Currency').grid(row=1, column=0, padx=5, pady=5)
    e1 = ctk.CTkComboBox(root, values=['\u20ac', '\uFF04', '\u00A3', '\u00A5'], command=lambda value: change_currency(value, app_state))
    e1.grid(row=2, column=0, padx=5, pady=5)
    e1.set(app_state.settings["app_settings"]["currency"])

    ctk.CTkLabel(root, text='Add User').grid(row=1, column=1, padx=5, pady=5)
    ctk.CTkLabel(root, text='Name:     ').grid(row=2, column=1, padx=5, pady=5)
    ctk.CTkLabel(root, text='e-Mail:     ').grid(row=3, column=1, padx=5, pady=5)
    e2 = ctk.CTkEntry(root, width=200)
    e3 = ctk.CTkEntry(root, width=200)
    e2.grid(row=2, column=2, padx=5, pady=5)
    e3.grid(row=3, column=2, padx=5, pady=5)
    ctk.CTkButton(root, text='Add', command=lambda: add_user(app_state)).grid(row=4, column=2, padx=5, pady=5)
    ctk.CTkButton(root, text='Delete', command=lambda: remove_user(app_state)).grid(row=4, column=3, padx=5, pady=5)


def file_frame(main_root, app_state: AppState):

    root = ctk.CTkFrame(main_root)
    root.pack(side='top', fill='x', anchor='w', padx=10, pady=10)

    title = ctk.CTkLabel(root, text='File Settings',
                         text_font=('Segoe UI', 15), width=100)
    title.grid(row=0, column=0, padx=5, pady=5)

    ctk.CTkButton(root, text='Open File').grid(
        row=1, column=0, pady=5, padx=10, sticky='w')
    ctk.CTkButton(root, text='New File').grid(
        row=1, column=1, pady=5, padx=10, sticky='w')
    ctk.CTkButton(root, text='Create Backup').grid(
        row=1, column=3, pady=5, padx=10, sticky='w')
    ctk.CTkButton(root, text='Restore Backup').grid(
        row=1, column=4, pady=5, padx=10, sticky='w')

    s = app_state.settings["app_settings"]["file_path"]

    ctk.CTkLabel(root, text=f'Data File Path: {s}').grid(
        row=2, columnspan=10, padx=5, pady=5, sticky='w')


def main_service_frame(main_root, app_state: AppState):

    def check_conection():
        if get_mail.test_connection(f"imap.{e1.get()}", e2.get(), e3.get()):
            app_state.settings["main_service"]["server"] = e1.get()
            app_state.settings["main_service"]["user"] = e2.get()
            app_state.settings["main_service"]["psw"] = e3.get()
            b1.config(text='Conneced!', text_color="#2ECC71")
        else:
            b1.config(text='Error!', text_color="#C0392B")

    def change_mail_service_mode(app_state: AppState):
        if mail_service.get() == 1:
            app_state.settings["main_service"]["active"] = 1
        else:
            app_state.settings["main_service"]["active"] = 0

    root = ctk.CTkFrame(main_root)
    root.pack(side='top', fill='x', anchor='w', padx=10, pady=10)

    title = ctk.CTkLabel(root, text='Main Service',
                         text_font=('Segoe UI', 15), width=100)
    title.grid(row=0, column=0, padx=5, pady=5)
    
    ctk.CTkLabel(root, text='         server:'
                 ).grid(row=1, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='         User:'
                 ).grid(row=2, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='     Password:'
                 ).grid(row=3, column=0, pady=5, padx=20, sticky='e')
    e1 = ctk.CTkEntry(root, width=200)
    e2 = ctk.CTkEntry(root, width=200)
    e3 = ctk.CTkEntry(root, width=200, show='*')
    e1.grid(row=1, column=1, pady=5, padx=10)
    e2.grid(row=2, column=1, pady=5, padx=10)
    e3.grid(row=3, column=1, pady=5, padx=10)
    e1.insert(0, app_state.settings["main_service"]["server"])
    e2.insert(0, app_state.settings["main_service"]["user"])
    e3.insert(0, app_state.settings["main_service"]["psw"])

    b1 = ctk.CTkButton(root, text='Check Connection', command=lambda: check_conection())
    b1.grid(row=4, column=1, pady=5, padx=10)

    mail_service = ctk.CTkSwitch(
        master=root, text="Activate Mail Service at Start", command=lambda: change_mail_service_mode(app_state))
    mail_service.grid(row=4, column=0, pady=5, padx=10)

    if app_state.settings["main_service"]["active"]:
        mail_service.select()


def draw_menue_3(main_root, app_state: AppState):

    global root

    root = ctk.CTkFrame(
        main_root, fg_color=ThemeManager.theme['color']['window_bg_color'])
    title = ctk.CTkLabel(root, text='Settings', text_font=('Segoe UI', 20))
    title.pack(side='top', anchor='w', padx=5, pady=5)
    draw_info_frame(root)
    appearance_frame(root, app_state)
    file_frame(root, app_state)
    table_settings_frame(root, app_state)
    main_service_frame(root, app_state)
    root.pack(fill='both', padx=10, pady=10, ipady=500)


def destroy_menue_3():
    try:
        root.destroy()
    except:
        pass
