import pickle
import os
from datetime import date
from app import app_lib

def check_if_dir_exist (path : str):
    if os.path.isdir(f"{path}\BondMarket_test") is False:
        os.mkdir(f"{path}\BondMarket_test")

def save_in_pkl (filename : str, data : list or dict, path : str) -> None:
    file = open(f"{path}\{filename}", "wb")
    pickle.dump(data, file)
    file.close()

def read_from_pkl (filename : str, path : str) -> dict:
    try:
        file = open(f"{path}\{filename}", "rb")
        settings_dict : dict = pickle.load(file)
        file.close()
    except FileNotFoundError:
        return False
    return settings_dict

def save_settings_in_file (app : app_lib.app_state) -> None:
    check_if_dir_exist(os.path.expanduser("~\Documents"))
    save_in_pkl('config.pkl', app.settings, os.path.expanduser('~\Documents\BondMarket_test'))

def read_settings_from_file (app : app_lib.app_state) -> None:
    if read_from_pkl('config.pkl', os.path.expanduser('~\Documents\BondMarket_test')) == False:
        app.settings = app_lib.settings('na', 'white', False, date.today().strftime("%Y"), date.today().strftime("%m"))
    else:
        app.settings = read_from_pkl('config.pkl', os.path.expanduser('~\Documents\BondMarket_test'))

def save_data_in_file (app : app_lib.app_state) -> None:
    check_if_dir_exist(app.settings.data_dir_path)
    save_in_pkl('data.pkl', app.data_array, f"{app.settings.data_dir_path}\BondMarket_test")

def read_data_from_file (app : app_lib.app_state) -> None:
    if read_from_pkl('data.pkl', f"{app.settings.data_dir_path}\BondMarket_test") == False:
        app.data_array = []
    else:
        app.data_array = read_from_pkl('data.pkl', f"{app.settings.data_dir_path}\BondMarket_test")
