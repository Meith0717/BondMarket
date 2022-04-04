from msilib.schema import Error
import pickle
import os
from datetime import date
from typing import Any
from app.theme_lib import LIGHT
import app.app_lib as app_lib

def check_if_dir_exist (path : str):
    if os.path.isdir(f"{path}/BondMarket") is False:
        os.mkdir(f"{path}/BondMarket")

def save_in_pkl (file_path : str, data : list or dict,) -> None:
    file = open(file_path, "wb")
    pickle.dump(data, file)
    file.close()

def read_from_pkl (file_path : str) -> Any:
    try:
        if os.stat(file_path).st_size == 0:
            print('File is empty')
            return False 
        file = open(file_path, "rb")
        data : dict = pickle.load(file)
        file.close()
    except FileNotFoundError:
        return False
    except ModuleNotFoundError:
        return 'Error'
    except AttributeError:
        return 'Error'
    return data

def save_settings_in_file (app : app_lib.app_state) -> None:
    save_in_pkl(f"{os.path.expanduser('~/Documents/BondMarket')}/config_V4.1.pkl", app.settings)

def read_settings_from_file (app : app_lib.app_state) -> None:
    if read_from_pkl(f"{os.path.expanduser('~/Documents/BondMarket')}/config_V4.1.pkl")  == 'Error':
        return 'Error'
    if read_from_pkl(f"{os.path.expanduser('~/Documents/BondMarket')}/config_V4.1.pkl") == False:
        check_if_dir_exist(os.path.expanduser("~/Documents"))
        app.settings = app_lib.settings(f"{os.path.expanduser('~/Documents/BondMarket')}/data.pkl".replace('/', '\\'), LIGHT, date.today().strftime("%Y"), date.today().strftime("%m"), True)
    else:
        app.settings = read_from_pkl(f"{os.path.expanduser('~/Documents/BondMarket')}/config_V4.1.pkl")

def save_data_in_file (app : app_lib.app_state) -> None:
    save_in_pkl(app.settings.data_path, app.data_array)

def read_data_from_file (app : app_lib.app_state) -> None:
    if read_from_pkl(app.settings.data_path) == 'Error':
        return 'Error'
    if read_from_pkl(app.settings.data_path) == False:
        app.data_array = []
    else:
        app.data_array = read_from_pkl(app.settings.data_path)
