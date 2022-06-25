from tkinter import font
import customtkinter as ctk
from customtkinter.theme_manager import ThemeManager
from app.app_state import AppState

# Main Frame Funktions #################################################################


def draw_menue_4(main_root, app_state: AppState):
    global root

    root = ctk.CTkFrame(
        main_root,
        fg_color=ThemeManager.theme['color']['window_bg_color'])
    root.pack(padx=20, pady=20, fill='both', expand=True)


def destroy_menue_4():
    try:
        root.destroy()
    except:
        pass
