from time import sleep
import customtkinter as ctk
from mail.get_mail import connect
import gui.menue_frame as menue_frame
import gui.status_bar as status_bar
from app.app_state import AppState, create_all_dir
import messagebox.messagebox as msg
import threading


def loading_animation(app_state: AppState):
    stage: int = 0
    while connect_.is_alive():
        if stage == 0:
            status.configure(text='Loading.      ')
            stage += 1
        elif stage == 1:
            status.configure(text='Loading..     ')
            stage += 1
        elif stage == 2:
            status.configure(text='Loading...    ')
            stage = 0

        sleep(0.4)
    menue_frame.draw_menue(main_root, app_state)
    main_root.attributes("-disabled", False)


def loading_screen(app_state: AppState) -> None:
    global status, connect_
    """This function checks the mail service

    Args:
        app_state (AppState)
    """
    app_state.load_array()
    connect_ = threading.Thread(target=(lambda: connect(app_state, "add_command")))
    loading_animation_ = threading.Thread(target=(lambda: loading_animation(app_state)))
    status = ctk.CTkLabel(main_root,
                          text='',
                          text_font=('Segoe UI', 30),
                          anchor='center')
    status.place(relx=.5, rely=.5, anchor="center")
    connect_.start()
    loading_animation_.start()
    

def exit(app_state: AppState) -> None:
    app_state.save_settings()
    if app_state.save_state is False:
        app_state.save_array() if msg.want_to_save(app_state.settings['app_settings']['file_path']) else None
    main_root.quit()


def mainloop() -> None:
    """_summary_
    """
    loading_screen_ = threading.Thread(target=(lambda: loading_screen(app_state)))
    global main_root
    create_all_dir()
    
    app_state = AppState()
    # Set up main Window
    app_state.load_settings()
    ctk.set_appearance_mode(app_state.settings["app_settings"]["appearance"])
    ctk.set_default_color_theme(r'themes\theme.json')
    main_root = ctk.CTk()
    main_root.state('zoomed')
    main_root.attributes("-disabled", True)
    loading_screen_.start()
    # Custom up main Window
    main_root.geometry(
        f"{main_root.winfo_screenwidth()}x{main_root.winfo_screenheight()}")
    main_root.title('')
    main_root.iconbitmap(r'icons\BondMarket_Icon.ico')
    main_root.protocol('WM_DELETE_WINDOW', lambda: exit(app_state))
    status_bar.draw_status_bar(main_root)
    main_root.mainloop()


if __name__ == '__main__':
    mainloop()
