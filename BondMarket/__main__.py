import customtkinter as ctk
import gui.menue_frame as menue_frame
import gui.status_bar as status_bar
from app.app_state import AppState

from tkinter import messagebox
from Mail import get_mail


def exit(app_state: AppState):
    app_state.save_settings()
    if app_state.save_state is False:
        app_state.save_array() if messagebox.askokcancel('BondMarket', 'exit_message') else None
    app_state.active = False
    main_root.quit()


def mainloop(app_state: AppState):
    global main_root, t, running_

    # Set up main Window
    ctk.set_appearance_mode(app_state.settings["app_settings"]["appearance"])
    ctk.set_default_color_theme(r'Themes\theme.json')
    ctk.deactivate_automatic_dpi_awareness()
    running_ = True
    main_root = ctk.CTk()
    if app_state.settings["main_service"]["active"]:
        get_mail.loader(main_root, app_state)
    app_state.load_array()
    # Custom up main Window
    main_root.geometry(
        f"{main_root.winfo_screenwidth()}x{main_root.winfo_screenheight()}")
    main_root.state('zoomed')
    main_root.title('')
    main_root.iconbitmap(r'Icons\BondMarket_Icon.ico')
    main_root.protocol('WM_DELETE_WINDOW', lambda: exit(app_state))
    status_bar.draw_status_bar(main_root)
    menue_frame.draw_menue(main_root, app_state)
    main_root.mainloop()


if __name__ == '__main__':
    app_state = AppState()
    app_state.load_settings()
    mainloop(app_state)
