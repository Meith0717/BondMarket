import customtkinter as ctk
import gui.menues.debts_menue as debts_menue
import gui.menues.expenses_menue as expenses_menue
import gui.menues.help_menue as help_menue
import gui.menues.settings_menue as settings_menue
from tkinter import PhotoImage
from customtkinter.theme_manager import ThemeManager
from app.app_state import App_State

DISABLED = 'disabled'
NORMAL = 'normal'


def show_menue_1(main_root, app_state: App_State) -> None:
    '''Shows menu 1 and destroys
    all other menus
    '''
    menue_1_button.config(state=DISABLED)
    menue_2_button.config(state=NORMAL)
    menue_3_button.config(state=NORMAL)
    menue_4_button.config(state=NORMAL)
    expenses_menue.draw_menue_1(main_root, app_state)
    debts_menue.destroy_menue_2()
    settings_menue.destroy_menue_3()
    help_menue.destroy_menue_4()


def show_menue_2(main_root, app_state: App_State) -> None:
    '''Shows menu 2 and destroys
    all other menus
    '''
    menue_1_button.config(state=NORMAL)
    menue_2_button.config(state=DISABLED)
    menue_3_button.config(state=NORMAL)
    menue_4_button.config(state=NORMAL)
    expenses_menue.destroy_menue_1()
    debts_menue.draw_menue_2(main_root, app_state)
    settings_menue.destroy_menue_3()
    help_menue.destroy_menue_4()


def show_menue_3(main_root, app_state: App_State) -> None:
    '''Shows menu 3 and destroys
    all other menus
    '''
    menue_1_button.config(state=NORMAL)
    menue_2_button.config(state=NORMAL)
    menue_3_button.config(state=DISABLED)
    menue_4_button.config(state=NORMAL)
    expenses_menue.destroy_menue_1()
    debts_menue.destroy_menue_2()
    settings_menue.draw_menue_3(main_root, app_state)
    help_menue.destroy_menue_4()


def show_menue_4(main_root, app_state: App_State) -> None:
    '''Shows menu 4 and destroys
    all other menus
    '''
    menue_1_button.config(state=NORMAL)
    menue_2_button.config(state=NORMAL)
    menue_3_button.config(state=NORMAL)
    menue_4_button.config(state=DISABLED)
    expenses_menue.destroy_menue_1()
    debts_menue.destroy_menue_2()
    settings_menue.destroy_menue_3()
    help_menue.draw_menue_4(main_root, app_state)


def save(app_state: App_State) -> None:
    app_state.save_settings()
    app_state.save_array()


def draw_menue(main_root, app_state: App_State) -> None:
    '''Creates the main menu of the app 
    Location: pack(side='left', fill='y', padx=0, pady=0)
    '''
    global menue_1_button, menue_2_button, menue_3_button, menue_4_button
    # Create Frame
    root = ctk.CTkFrame(main_root, width=60)
    root.pack(side='left', fill='y', padx=10, pady=10)
    # Define some Values
    logo = PhotoImage(file=r"Icons\BondMarket_Icon.png")
    text_color = ThemeManager.theme['color']['text']
    text_color_disabled = ThemeManager.theme['color']['window_bg_color']
    text_font = ('Segoe UI', 15)
    # Create Menue Buttons
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
                                   width=10,
                                   command=lambda: show_menue_2(
                                       main_root, app_state),
                                   fg_color=None,
                                   hover_color=None,
                                   text_font=text_font,
                                   border_width=0
                                   )
    menue_3_button = ctk.CTkButton(root,
                                   text='Settings',
                                   width=10,
                                   command=lambda: show_menue_3(
                                       main_root, app_state),
                                   fg_color=None,
                                   hover_color=None,
                                   text_font=text_font,
                                   border_width=0
                                   )
    menue_4_button = ctk.CTkButton(root,
                                   text='Help',
                                   width=10,
                                   command=lambda: show_menue_4(
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
                               width=10)
    menue_1_button.pack(side='top', padx=5, pady=40, anchor='c')
    menue_2_button.pack(side='top', padx=5, pady=40, anchor='c')
    menue_3_button.pack(side='top', padx=5, pady=40, anchor='c')
    menue_4_button.pack(side='top', padx=5, pady=40, anchor='c')
    PDF_button.pack(side='bottom', padx=5, pady=10)
    save_button.pack(side='bottom', padx=5, pady=10)
    ctk.CTkLabel(root, text='_____________').pack(
        side='bottom', padx=5, pady=2)
    # Shows menu 1 at startup
    show_menue_1(main_root, app_state)
