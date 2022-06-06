import tkinter as tk
import customtkinter as ctk
from customtkinter.theme_manager import ThemeManager
from customtkinter import appearance_mode_tracker
from app.app_state import AppState
from webbrowser import open


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


def currency_frame(main_root, app_state: AppState):

    def change_currency(value, app_state: AppState):
        app_state.settings["app_settings"]["currency"] = value

    root = ctk.CTkFrame(main_root)
    root.pack(side='top', fill='x', anchor='w',
              padx=10, pady=10, ipadx=10, ipady=10)

    title = ctk.CTkLabel(root, text='Currency', text_font=('Segoe UI', 15))
    title.grid(row=0, column=0, padx=5, pady=5)

    e1 = ctk.CTkComboBox(root, values=['\u20ac', '\uFF04', '\u00A3', '\u00A5'], command=lambda value: change_currency(value, app_state))
    e1.grid(row=1, column=0, padx=5, pady=5)
    e1.set(app_state.settings["app_settings"]["currency"])


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


def draw_menue_3(main_root, app_state: AppState):

    global root

    root = ctk.CTkFrame(
        main_root, fg_color=ThemeManager.theme['color']['window_bg_color'])
    title = ctk.CTkLabel(root, text='Settings', text_font=('Segoe UI', 20))
    title.pack(side='top', anchor='w', padx=5, pady=5)
    draw_info_frame(root)
    appearance_frame(root, app_state)
    file_frame(root, app_state)
    currency_frame(root, app_state)
    root.pack(fill='both', padx=10, pady=10, ipady=500)


def destroy_menue_3():
    try:
        root.destroy()
    except:
        pass
