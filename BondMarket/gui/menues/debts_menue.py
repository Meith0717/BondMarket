import customtkinter as ctk
from customtkinter import appearance_mode_tracker
from customtkinter.theme_manager import ThemeManager
from app.app_state import AppState, DebtsStrukture
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

PADX = PADY = IPADX = IPADY = 10

# Main Frame Funktions #################################################################


def debts(main_root: ctk.CTk, app_state: AppState) -> None:
    currency = app_state.settings['app_settings']['currency']
    root = ctk.CTkFrame(main_root)
    root.pack(side='left', anchor='nw', padx=PADX,
              pady=PADY, ipadx=IPADX, ipady=IPADY, expand=False)
    ctk.CTkLabel(root, text='Debts',
                 text_font=('Segoe UI', 15)
                 ).pack(side='top', padx=5, pady=5)
    
    row_frames = [ctk.CTkFrame(root, fg_color=None) for _ in range(10)]
    lables = [ctk.CTkLabel(row_frames[i], text='', text_font=('San Francisco', 12)) for i in range(10)]

    for i in range(10):
        row_frames[i].pack(side='top', anchor='w', padx=5, pady=5)
        try:
            debts: DebtsStrukture = app_state.debts_state.debts_array[i]
            lables[i].config(text=f"{debts.sender} must transfer {debts.amount} {currency} to {debts.receiver}")
        except IndexError:
            pass
        lables[i].pack()


def personal_expenses(main_root: ctk.CTk, app_state: AppState) -> None:
    
    root = ctk.CTkFrame(main_root)
    root.pack(side='left', anchor='nw', fill=None, padx=PADX,
              pady=PADY, ipadx=IPADX, ipady=IPADY, expand=False)
    ctk.CTkLabel(root, text='Personal expenses',
                 text_font=('Segoe UI', 15)
                 ).pack(side='top', padx=5, pady=5)
    
    personal_expenses = list(app_state.debts_state.personal_expenses.values())
    user_names = list(app_state.debts_state.personal_expenses.keys())
    bg = ThemeManager.theme['color']['frame_low'][appearance_mode_tracker.AppearanceModeTracker.appearance_mode]
    fg = ThemeManager.theme['color']['text'][appearance_mode_tracker.AppearanceModeTracker.appearance_mode]

    plt.rcParams.update({'axes.facecolor':'black'})
    figure1 = plt.Figure(figsize=(6,6))
    figure1.set_facecolor(bg)
    ax = figure1.add_subplot(111)
    ax.pie(personal_expenses, labels = user_names, autopct='%1.0f%%', textprops={'color':fg})
    
    bar1 = FigureCanvasTkAgg(figure1, root)
    bar1.get_tk_widget().pack(side='left', fill='both', padx=5, pady=5)


def draw_menue_2(main_root: ctk.CTk, app_state: AppState):
    global root
    
    root = ctk.CTkFrame(
        main_root,
        fg_color=ThemeManager.theme['color']['window_bg_color'])
    root.pack(padx=20, pady=20, fill='both', expand=True)
    app_state.get_debts_array()
    personal_expenses(root, app_state)
    debts(root, app_state)


def destroy_menue_2():
    try:
        root.destroy()
    except:
        pass
