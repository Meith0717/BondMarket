import customtkinter as ctk
from customtkinter import appearance_mode_tracker
from customtkinter.theme_manager import ThemeManager
from app.app_state import AppState, DebtsStrukture
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

PADX = PADY = IPADX = IPADY = 10
LABLE_TITLE_FONT = ('San Francisco', 20)

# Main Frame Funktions #################################################################


def debts(main_root: ctk.CTk, app_state: AppState) -> None:
    currency = app_state.settings['app_settings']['currency']
    root = ctk.CTkFrame(main_root)
    root.grid(row=0, column=1, sticky='n', padx=PADX,
              pady=PADY, ipadx=IPADX, ipady=IPADY)
    ctk.CTkLabel(root, text='Debts         ',
                 text_font=LABLE_TITLE_FONT
                 ).pack(side='top', anchor='nw', padx=5, pady=5)
    row_frames = [ctk.CTkFrame(root, fg_color=None) for _ in range(10)]
    
    if len(app_state.debts_state.debts_array) == 0:
        ctk.CTkLabel(root,
                     text='Here is nothing to do.',
                     text_font=('San Francisco', 12)
                     ).pack(side='top', anchor='w', padx=5, pady=5)
    else:
        lables = [ctk.CTkLabel(row_frames[i], text='', text_font=('San Francisco', 12)) for i in range(10)]
        for i in range(10):
            row_frames[i].pack(side='top', anchor='w', padx=5, pady=20)
            try:
                debts: DebtsStrukture = app_state.debts_state.debts_array[i]
                lables[i].config(text=f"{debts.sender} must transfer {debts.amount} {currency} to {debts.receiver}")
            except IndexError:
                pass
            lables[i].pack()


def personal_expenses(main_root: ctk.CTk, app_state: AppState) -> None:
    
    average = app_state.debts_state.average_expenses
    total = sum(list(app_state.debts_state.personal_expenses.values()))
    currency = app_state.settings['app_settings']['currency']
    
    def func(pct):
        absolute = int(pct/100.*total)
        return f"{round(pct)}%\n({absolute})"
    
    root = ctk.CTkFrame(main_root)
    root.grid(row=0, column=0, padx=PADX,
              pady=PADY, ipadx=IPADX, ipady=IPADY)
    ctk.CTkLabel(root, text='Personal expenses',
                 text_font=LABLE_TITLE_FONT
                 ).grid(row=0, column=0, columnspan=10, sticky='w', padx=5, pady=5)
    
    personal_expenses = list(app_state.debts_state.personal_expenses.values())
    user_names = list(app_state.debts_state.personal_expenses.keys())
    bg = ThemeManager.theme['color']['frame_low'][appearance_mode_tracker.AppearanceModeTracker.appearance_mode]
    fg = ThemeManager.theme['color']['text'][appearance_mode_tracker.AppearanceModeTracker.appearance_mode]

    plt.rcParams.update({'axes.facecolor':'black'})
    figure1 = plt.Figure(figsize=(9,6))
    figure1.set_facecolor(bg)
    ax = figure1.add_subplot(111)
    ax.pie(personal_expenses, labels = user_names, autopct= func, textprops={'color':fg})
    
    bar1 = FigureCanvasTkAgg(figure1, root)
    bar1.get_tk_widget().grid(row=1, column=0, columnspan=10, sticky='w', padx=5, pady=5)
    ctk.CTkLabel(root,
                     text=f'Average:',
                     text_font=('San Francisco', 12)
                     ).grid(row=2, column=0, sticky='w', padx=5, pady=5)
    ctk.CTkLabel(root,
                     text=f'{average} {currency}',
                     text_font=('San Francisco', 12)
                     ).grid(row=2, column=1, sticky='w', padx=5, pady=5)
    ctk.CTkLabel(root,
                     text=f'Total:',
                     text_font=('San Francisco', 12)
                     ).grid(row=3, column=0, sticky='w', padx=5, pady=5)
    ctk.CTkLabel(root,
                     text=f'{total} {currency}',
                     text_font=('San Francisco', 12)
                     ).grid(row=3, column=1, sticky='w', padx=5, pady=5) 


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
