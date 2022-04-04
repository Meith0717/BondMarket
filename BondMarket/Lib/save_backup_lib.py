import Lib.save_data_lib as save_data_lib 
import app.app_lib as app_lib
import os
from tkinter import messagebox
from datetime import datetime

def create_backup (app : app_lib.app_state):
    if app.safe_state_data is False:
        return
    path = os.path.expanduser('~\Documents\BondMarket')
    try:
        os.mkdir(f'{path}\BondMarket_Backup')
    except FileExistsError:
        pass
    path = f'{path}\BondMarket_Backup'
    save_data_lib.save_in_pkl(f'{path}/{datetime.now().strftime("%S.%M.%H %d.%m.%Y")} data.pkl', app.data_array)
    messagebox.showinfo('BondMarket',f'{datetime.now().strftime("%S.%M.%H %d.%m.%Y")} data.pkl were generated in {path}.')