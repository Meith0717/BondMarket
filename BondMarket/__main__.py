__author__ = "Thierry Meiers"
__copyright__ = "Copyright © 2022 Thierry Meiers"
__license__ = "Apache License 2.0"
__version__ = "4.0"

from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk
import Lib.app_lib as app_lib
from Lib.save_data_lib import read_data_from_file, read_settings_from_file
from Interface.gui_lib import *

def main():
    '''This is the main function that creates the window.'''
    # Initializes the main class and loads the data from the files
    app = app_lib.app_state([], {}, True)
    read_settings_from_file(app)
    read_data_from_file(app)
    print(f'\n{app}')
    win = ThemedTk(theme=app.settings.appearance.ttk_theme)
    # Set some window settings 
    win.title('')
    win.iconbitmap('BondMarket\Icons\Transparent.ico')
    win.protocol('WM_DELETE_WINDOW', (lambda : exit(win, app)))
    win.config(bg=app.settings.appearance.bg_color)
    win.geometry(f'{1000}x{650}')
    win.minsize(1000, 650)
    center_window(win, 1000, 650)
    # Define some frames and set preferences
    data_frame = tk.Frame(win, bg=app.settings.appearance.bg_color, relief='flat')
    entry_frame = tk.Frame(win, bg=app.settings.appearance.bg_color, relief='flat')
    more_frame = tk.Frame(win, bg=app.settings.appearance.bg_color, relief='flat')
    button_frame = tk.Frame(win, bg=app.settings.appearance.bg_color, relief='flat')
    tabs = ttk.Notebook(more_frame)
    tab1 = ttk.Frame(tabs, relief='flat')
    tab2 = ttk.Frame(tabs, relief='flat') 
    tab3 = ttk.Frame(tabs, relief='flat') 
    tabs.add(tab1, text ='     Tools     ')
    tabs.add(tab2, text ='    Settings   ')
    tabs.add(tab3, text ='   Help/Info   ')
    tabs.pack(side='left', fill='both', padx=5, pady=5)
    # Set a few keyboard shortcuts
    win.bind('<Control-s>', lambda event: save(app))
    win.bind('<Control-o>', lambda event: get_data_path(win, app))
    win.bind('<Escape>', lambda event: exit(win, app))
    win.bind('<Return>', lambda event: safe_to_dataarray(app))
    win.bind('<Delete>', lambda event: delet_from_dataarray(app))
    # A few functions
    table_(data_frame, app)
    entry_(entry_frame, app)
    tools_(tab1, app)
    settings_(win, tab2, app)
    info_(tab3, app)
    button_(button_frame, app)
    # Place some Frames 
    tk.Label(win, text='Python 3.10.1     %s    Version %s' %(code_copyright,code_version), font=Font(family="Segoe UI", size=8), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.bg_color, width=5000).pack(side='bottom', fill='x')
    button_frame.pack(side='bottom', anchor='se', fill='x')
    more_frame.pack(side='right', padx=2, pady=2, fill='y')
    tk.Label(win, text='BondMarket', font=Font(family="Segoe UI", size=17), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.bg_color).pack(side='top', anchor='sw', padx=2, pady=2)
    entry_frame.pack(side='bottom', anchor='w', padx=2, pady=2, fill='both')
    data_frame.pack(side='top', anchor='nw', padx=2, pady=2, fill='both')
    win.mainloop()

if __name__ == '__main__':
    main()
