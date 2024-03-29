import customtkinter as ctk
from app.app_state import APP_AUTHOR, APP_VERSION, LANGUAGE_VERSION


def draw_status_bar(main_root: ctk.CTk) -> None:
    '''
    Creates the status bar of the app with the version description, 
    the copyright and the programming languages version
    location: pack(side='bottom', fill='x') 
    '''
    root = ctk.CTkFrame(main_root, corner_radius=0, height=25)
    root.pack(side='bottom', fill='x')
    ctk.CTkLabel(root,
                 text=f'Python {LANGUAGE_VERSION}  |  Copyright © 2022 {APP_AUTHOR}  | v{APP_VERSION}',
                 width=80,
                 height=20,
                 ).pack()
