from pickle import APPEND
from tkinter import font
import customtkinter as ctk
from customtkinter.theme_manager import ThemeManager
from app.app_state import AppState

# Main Frame Funktions #################################################################


def draw_menue_2(main_root, app_state: AppState):
    global root

    root = ctk.CTkFrame(
        main_root, fg_color=ThemeManager.theme['color']['window_bg_color'])
    title = ctk.CTkLabel(root, text='Debts', text_font=('Segoe UI', 20))
    title.pack(side='top', anchor='w', padx=5, pady=5)
    root.pack(fill='both', padx=5, pady=5, ipady=500)
    app_state.get_debts_array()



def destroy_menue_2():
    try:
        root.destroy()
    except:
        pass
