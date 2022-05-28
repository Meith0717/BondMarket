from tkinter import font
import customtkinter as ctk
from customtkinter.theme_manager import ThemeManager
from app.app_state import App_State

# Main Frame Funktions #################################################################


def draw_menue_2(main_root, app_state: App_State):
    global root

    root = ctk.CTkFrame(
        main_root, fg_color=ThemeManager.theme['color']['window_bg_color'])
    title = ctk.CTkLabel(root, text='Debts', text_font=('Segoe UI', 20))
    title.pack(side='top', anchor='w', padx=5, pady=5)
    root.pack(fill='both', padx=5, pady=5, ipady=500)


def destroy_menue_2():
    try:
        root.destroy()
    except:
        pass
