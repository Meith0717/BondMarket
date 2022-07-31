from time import sleep
import tkinter
import customtkinter as ctk
import gui.menues.debts_menue as debts_menue
import gui.menues.expenses_menue as expenses_menue
import gui.menues.settings_menue as settings_menue
import pdf.pdf as pdf
from tkinter import PhotoImage
from customtkinter.theme_manager import ThemeManager
from app.app_state import AppState

DISABLED = 'disabled'
NORMAL = 'normal'


def show_menue_1(main_root, app_state: AppState) -> None:
    '''Shows menu 1 and destroys
    all other menus
    '''
    menue_1_button.configure(state=DISABLED)
    menue_2_button.configure(state=NORMAL)
    menue_3_button.configure(state=NORMAL)
    expenses_menue.draw_menue_1(main_root, app_state)
    debts_menue.destroy_menue_2()
    settings_menue.destroy_menue_3()


def show_menue_2(main_root, app_state: AppState) -> None:
    '''Shows menu 2 and destroys
    all other menus
    '''
    menue_1_button.configure(state=NORMAL)
    menue_2_button.configure(state=DISABLED)
    menue_3_button.configure(state=NORMAL)
    expenses_menue.destroy_menue_1()
    debts_menue.draw_menue_2(main_root, app_state)
    settings_menue.destroy_menue_3()


def show_menue_3(main_root, app_state: AppState) -> None:
    '''Shows menu 3 and destroys
    all other menus
    '''
    menue_1_button.configure(state=NORMAL)
    menue_2_button.configure(state=NORMAL)
    menue_3_button.configure(state=DISABLED)
    expenses_menue.destroy_menue_1()
    debts_menue.destroy_menue_2()
    settings_menue.draw_menue_3(main_root, app_state)


def save(app_state: AppState) -> None:
    app_state.save_state = True
    app_state.save_array()


def draw_menue(main_root: ctk.CTk, app_state: AppState) -> None:
    '''Creates the main menu of the app 
    Location: pack(side='left', fill='y', padx=0, pady=0)
    '''
    global menue_1_button, menue_2_button, menue_3_button, menue_4_button
    # Create Frame
    root = ctk.CTkFrame(main_root, width=200)
    root.pack(side='left', fill='y', padx=10, pady=5)
    # Define some Values
    logo = PhotoImage(file=r"Icons\BondMarket_Icon.png")
    settings = PhotoImage(file=r"Icons\settings.png")
    expenses = PhotoImage(file=r"Icons\finance.png")
    debts = PhotoImage(file=r"Icons\debts.png")
    text_color = ThemeManager.theme['color']['text']
    text_font = ('Segoe UI', 15)
    # Create Menue Buttons
    
    main_root.bind('<Control-s>', lambda _: save(app_state))
    
    ctk.CTkButton(root,
                  image=logo,
                  state='disabled',
                  text='BondMarked',
                  bg_color=None,
                  fg_color=None,
                  text_color_disabled=text_color,
                  text_font=text_font,
                  hover_color=None,
                  border_width=0
                  ).pack(side='top', padx=5, pady=20)
    menue_1_button = ctk.CTkButton(root,
                                   text='Expenses',
                                   image=expenses,
                                   width=20,
                                   command=lambda: show_menue_1(
                                       main_root, app_state),
                                   fg_color=None,
                                   hover_color=None,
                                   text_font=text_font,
                                   border_width=0
                                   )
    menue_2_button = ctk.CTkButton(root,
                                   text='Debts',
                                   image=debts,
                                   width=20,
                                   command=lambda: show_menue_2(
                                       main_root, app_state),
                                   fg_color=None,
                                   hover_color=None,
                                   text_font=text_font,
                                   border_width=0
                                   )
    menue_3_button = ctk.CTkButton(root,
                                   text='Settings',
                                   image=settings,
                                   width=20,
                                   command=lambda: show_menue_3(
                                       main_root, app_state),
                                   fg_color=None,
                                   hover_color=None,
                                   text_font=text_font,
                                   border_width=0
                                   )
    save_button = ctk.CTkButton(root,
                                text='Save',
                                width=10,
                                command=lambda: save(app_state))
    PDF_button = ctk.CTkButton(root,
                               text='PDF',
                               width=10,
                               command=lambda: pdf.export(app_state))
    menue_1_button.pack(side='top', padx=5, pady=50, anchor='w')
    menue_2_button.pack(side='top', padx=5, pady=50, anchor='w')
    menue_3_button.pack(side='top', padx=5, pady=50, anchor='w')
    PDF_button.pack(side='bottom', padx=5, pady=10)
    save_button.pack(side='bottom', padx=5, pady=10)
    ctk.CTkLabel(root, text='_____________').pack(
        side='bottom', padx=5, pady=2)
    # Shows menu 1 at startup
    sleep(1)
    show_menue_1(main_root, app_state)
