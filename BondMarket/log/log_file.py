from dataclasses import dataclass
from typing import Literal
from app.app_state import APP_LOG_DIR_PATH, MS_LOG_DIR_PATH
from datetime import datetime
import os
from time import sleep

DATE        = datetime.today().strftime('%Y.%m.%d_%H.%M.%S')
DOC_PATH    = os.path.expanduser('~\\Documents')

@dataclass
class Log_file:
    
    

    def initialize(self, application: Literal['APP', 'MS']):
        if application == 'APP':
            self.file_path  = f"{APP_LOG_DIR_PATH}\\{DATE}.log"
            open(self.file_path, 'a').close()
        elif application == 'MS':
            self.file_path  = f"{MS_LOG_DIR_PATH}\\{DATE}.log"
            open(self.file_path, 'a').close()

    def print_(self, user: str, text: str):
        with open(self.file_path, 'a') as file:
            file.write(f"({datetime.today().strftime('%H:%M:%S')} {user}) : {text}\n")
