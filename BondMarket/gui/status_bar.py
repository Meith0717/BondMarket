import customtkinter as ctk


def draw_status_bar(main_root: ctk.CTk) -> None:
    '''
    Creates the status bar of the app with the version description, 
    the copyright and the programming languages version
    location: pack(side='bottom', fill='x') 
    '''
    root = ctk.CTkFrame(main_root,
                        height=20,
                        )
    root.pack(side='bottom', fill='x', pady=4, padx=4)
    ctk.CTkLabel(root,
                 text=f'Python 3.10.1  |  Copyright © 2022 Thierry Meiers  |  Version _Beta_',
                 width=80,
                 height=20,
                 ).pack()
