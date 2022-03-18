from data import save_data_lib
import os
from tkinter import messagebox
from datetime import datetime
from app import app_lib

def create_backup (app : app_lib.app_state):
    path = os.path.expanduser('~\Documents\BondMarket')
    try:
        os.mkdir(f'{path}\BondMarket_Backup')
    except FileExistsError:
        pass
    path = f'{path}\BondMarket_Backup'
    save_data_lib.save_in_pkl(f'{path}/{datetime.now().strftime("%S.%M.%H %d.%m.%Y")} data.pkl', app.data_array)
    messagebox.showinfo(title='Info:', message=f'{datetime.now().strftime("%S.%M.%H %d.%m.%Y")} data.pkl were generated in {path}.')