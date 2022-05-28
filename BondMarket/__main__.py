__author__ = "Thierry Meiers"
__copyright__ = "Copyright © 2022 Thierry Meiers"
__license__ = "Apache License 2.0"
__version__ = "4.1"

from ttkthemes import ThemedStyle
from tkinter import ttk
from PIL import ImageTk, Image
import lib.save_backup_lib as save_backup_lib 
from interface.gui_lib import *
from interface.welcome_lib import *

def main():
    '''This is the main function that creates the window.'''
    # Initializes the main class and loads the data from the files
    app = app_lib.app_state([], {}, True)
    if read_settings_from_file(app) == 'Error' or read_data_from_file(app) == 'Error':
        messagebox.showerror('BondMarket', 'An error occurred while reading the file.\n\nProbably the files are not compatible!')
        exit(win, app)
    if app.settings.first_start is True:
        welcome_window()
    win = tk.Tk() #theme=app.settings.appearance.ttk_theme
    # Set some window settings 
    style = ThemedStyle(win)
    style.theme_use(app.settings.appearance.ttk_theme)
    win.title('')
    try:
        win.iconbitmap('Icons\BondMarket_Icon.ico')
    except:
        win.iconbitmap('BondMarket\Icons\BondMarket_Icon.ico')
    win.protocol('WM_DELETE_WINDOW', (lambda : exit(win, app)))
    win.config(bg=app.settings.appearance.bg_color)
    win.geometry(f'{1000}x{650}')
    win.minsize(1000, 650)
    center_window(win, 1000, 650)
    # Define some frames and set preferences
    data_frame = tk.Frame(win, bg=app.settings.appearance.bg_color, relief='flat')
    entry_frame = tk.Frame(win, bg=app.settings.appearance.bg_color, relief='flat')
    notebook = tk.Frame(win, bg=app.settings.appearance.bg_color, relief='flat')
    button_frame = tk.Frame(win, bg=app.settings.appearance.bg_color, relief='flat')
    tabs = ttk.Notebook(notebook)
    tab1 = ttk.Frame(tabs, relief='flat')
    tab2 = ttk.Frame(tabs, relief='flat') 
    tab3 = ttk.Frame(tabs, relief='flat') 
    tab4 = ttk.Frame(tabs, relief='flat')
    tabs.add(tab1, text ='   Expenses    ')
    tabs.add(tab2, text = '     Debts     ')
    tabs.add(tab3, text ='    Settings   ')
    tabs.add(tab4, text ='   Help/Info   ')
    tabs.pack(side='left', fill='both', padx=5, pady=5, ipadx=25)
    # Define an Munuebar
    menuebar = tk.Menu(win)
    app_menue = tk.Menu(menuebar, relief='flat', tearoff=0)
    app_menue.add_command(label='Save', command=(lambda : save(app)))
    app_menue.add_separator()
    app_menue.add_command(label='Exit', command=(lambda : exit(win, app)))
    menuebar.add_cascade(label='App', menu=app_menue)
    file_menue = tk.Menu(menuebar, relief='flat', tearoff=0)
    file_menue.add_command(label='Open File', command=(lambda : open_file(app)))
    file_menue.add_command(label='New File', command=(lambda : open_new_file(app)))
    file_menue.add_separator()
    file_menue.add_command(label='Create Backup', command=(lambda : save_backup_lib.create_backup(app)))
    file_menue.add_command(label='Restore Backup', command=(lambda : restore_backup(app)))
    menuebar.add_cascade(label='File', menu=file_menue)
    # Set a few keyboard shortcuts
    win.bind('<Control-s>', lambda event: save(app))
    win.bind('<Control-o>', lambda event: open_file(app))
    win.bind('<Control-n>', lambda event: open_new_file(app))
    win.bind('<Escape>', lambda event: exit(win, app))
    win.bind('<Return>', lambda event: safe_to_dataarray(app))
    win.bind('<Delete>', lambda event: delet_from_dataarray(app))
    # A few functions
    table_(data_frame, app)
    entry_(entry_frame, app)
    expenses_(tab1, app)
    debts_(tab2, app)
    settings_(win, tab3, app, main)
    info_(tab4, app)
    button_(button_frame, app)
    # Import Logo
    if app.settings.appearance.name == 'LIGHT':
        try:
            logo = Image.open("Icons\BondMarket_Logo_dark.png")
        except:
            logo = Image.open("BondMarket\Icons\BondMarket_Logo_dark.png")
    if app.settings.appearance.name == 'DARK':
        try:
            logo = Image.open("Icons\BondMarket_Logo_white.png")
        except:
            logo = Image.open("BondMarket\Icons\BondMarket_Logo_white.png")
    logo = logo.resize((256, 50))
    logo = ImageTk.PhotoImage(logo)
    # Place some Frames 
    win.config(menu=menuebar)
    tk.Label(win, text='Python 3.10.1     %s    Version %s' %(code_copyright,code_version), font=tkinter.font.Font(family="Segoe UI", size=8), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.bg_color, width=5000).pack(side='bottom', fill='x')
    button_frame.pack(side='bottom', anchor='se', fill='x')
    notebook.pack(side='right', padx=2, pady=2, fill='y')
    tk.Label(win, image=logo, bg=app.settings.appearance.bg_color).pack(side='top', anchor='sw', padx=5, pady=5)
    entry_frame.pack(side='bottom', anchor='w', padx=2, pady=2, fill='both')
    data_frame.pack(side='top', anchor='nw', padx=2, pady=2, fill='both')
    win.mainloop()

if __name__ == '__main__':
    main()
