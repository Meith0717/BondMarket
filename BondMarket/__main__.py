import customtkinter as ctk
import tkinter.messagebox as messagebox
import gui.menue_frame as menue_frame
import gui.status_bar as status_bar
from app.app_state import App_State


def exit(app_state: App_State):
    if messagebox.askokcancel('BondMarket', 'exit_message'):
        main_root.quit()


def mainloop():
    global main_root

    app_state = App_State()
    app_state.load_settings()
    app_state.load_array()
    # Set up main Window
    ctk.set_appearance_mode(app_state.settings["app_settings"]["appearance"])
    ctk.set_default_color_theme(r'Themes\theme.json')
    main_root = ctk.CTk()
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
    mainloop()
