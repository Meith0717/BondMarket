import customtkinter as ctk
import gui.menue_frame as menue_frame
import gui.status_bar as status_bar
from app.app_state import AppState, create_all_dir, process_exists
import messagebox.messagebox as msg
import threading



def check_if_ms_is_running(app_state: AppState) -> None:
    """This function checks if the mail service is running

    Args:
        app_state (AppState)
    """
    if process_exists('Mail Service.exe'):
        msg.ms_is_running()
        main_root.quit()


def exit(app_state: AppState) -> None:
    app_state.save_settings()
    if app_state.save_state is False:
        app_state.save_array() if msg.want_to_save(app_state.settings['app_settings']['file_path']) else None
    main_root.quit()


def mainloop() -> None:
    """_summary_
    """
    
    t = threading.Thread(target=(lambda: check_if_ms_is_running(app_state)))

    global main_root
    create_all_dir()
    app_state = AppState()
    # Set up main Window
    app_state.load_settings()
    ctk.set_appearance_mode(app_state.settings["app_settings"]["appearance"])
    app_state.load_array()
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
    t.start()
    main_root.mainloop()


if __name__ == '__main__':
    mainloop()
