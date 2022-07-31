from dataclasses import dataclass
from datetime import datetime
import os

DATE        = datetime.today().strftime('%Y.%m.%d_%H.%M.%S')
DOC_PATH    = os.path.expanduser('~\\Documents')

@dataclass
class Log_file:

    def initialize(self, path: str):
        self.file_path  = f"{path}\\{DATE}.log"
        open(self.file_path, 'a').close()


    def print_(self, text: str):
        with open(self.file_path, 'a') as file:
            file.write(f"({datetime.today().strftime('%H:%M:%S')}) : {text}\n")
