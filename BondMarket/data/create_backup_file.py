from data import save_data_lib
import os
from datetime import datetime
from app import app_lib

def create_backup (app : app_lib.app_state):
    path = os.path.expanduser('~/Documents')
    try:
        os.mkdir(f'{path}/BondMarked_Backup')
    except FileExistsError:
        pass
    path = f'{path}/BondMarked_Backup'
    save_data_lib.save_in_pkl(f'{datetime.now().strftime("%S.%M.%H %d.%m.%Y")} data.pkl', app.data_array, path)
    save_data_lib.save_in_pkl(f'{datetime.now().strftime("%S.%M.%H %d.%m.%Y")} config.pkl', app.settings, path)