"""System module."""
from dataclasses import dataclass
from datetime import date as datetime
import os
import json
import pickle
import subprocess

APP_VERSION = 'b.5.0.1'
APP_AUTHOR = 'Thierry Meiers'
LANGUAGE_VERSION = 3.10

DOC_PATH = os.path.expanduser('~\\Documents')
APP_DIR_PATH = f"{DOC_PATH}\\BondMarket {APP_VERSION}"
DATA_DIR_PATH = f"{APP_DIR_PATH}\\BondMarket Data"
SETTINGS_DIR_PATH = f"{APP_DIR_PATH}\\Settings"
APP_LOG_DIR_PATH = f"{APP_DIR_PATH}\\BondMarket Log"
MS_LOG_DIR_PATH = f"{APP_DIR_PATH}\\Mail Service Log"
BACKUP_DIR_PATH = f"{APP_DIR_PATH}\\BondMarket Backup"
DIRECTORIES = [APP_DIR_PATH,
         DATA_DIR_PATH,
         SETTINGS_DIR_PATH,
         APP_LOG_DIR_PATH,
         MS_LOG_DIR_PATH,
         BACKUP_DIR_PATH]

SETTINGS = {
    "app_settings":
    { 
        "appearance": "light",
        "file_path": f"{DATA_DIR_PATH}\\data.pkl",
        "currency": "\u20ac",
        "persons_mames": {}
    },
    "main_service":
    {
        "server": '',
        "user": '',
        "psw": ''
    }
}


def process_exists(process_name: str) -> bool:
    """Ts true if the process exists, if not then false.

    Args:
        process_name (str): Name of an Prozess

    Returns:
        bool
    """
    call = 'TASKLIST', '/FI', f'imagename eq {process_name}'
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().rsplit('\r\n', maxsplit=1)[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())


def average(dictionarry: dict) -> float:
    """Returns the average of the values of
    the dictionary

    Args:
        d (dict): A dictionary with str as
        key and int/float as value

    Returns:
        float: average of the values of
        the dictionary
    """
    dict_len: int = len(dictionarry)
    if dict_len == 0:
        return 0
    sum_: int = 0
    for value in dictionarry.values():
        sum_ += value
    return round(sum_/dict_len, 2)


@dataclass
class ExpenditureStrukture:
    """Structure of Expenses.
    """
    person_name: str
    amount: float
    comment: str
    date: str


@dataclass
class TableState:
    """Structure of the Table State.
    """
    table_array = []
    sort_argument = "Amount up"
    index = 0
    month_filter = datetime.today().strftime('%m')
    year_filter = datetime.today().strftime('%Y')


@dataclass
class DebtsStrukture:
    """Structure of the Debts.
    """
    sender: str
    receiver: str
    amount: float


@dataclass
class DebtsState:
    """Structure of the Debts State.
    """
    personal_expenses = {}
    debts_array = []
    average_expenses = 0


def create_all_dir() -> None:
    """Creates all needed folders
    """
    for dir in DIRECTORIES:
        if not os.path.isdir(dir):
            os.mkdir(dir)
    

@dataclass
class AppState:
    """Structure of the App State.
    """
    data_array = []
    settings = {}
    table_state = TableState()
    debts_state = DebtsState()
    save_state = True

    def load_settings(self) -> None:
        """Loads the data from the file settings.json.
        """
        try:
            with open(f"{SETTINGS_DIR_PATH}\\settings.json", "r",
                      encoding="UTF-8") as file:

                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = SETTINGS

    def save_settings(self) -> None:
        """Saves the data to the file settings.json.
        """
        if not os.path.isdir('Settings'):

            os.mkdir('Settings')
        with open(f"{SETTINGS_DIR_PATH}\\settings.json", "w",
                  encoding="UTF-8") as file:

            json.dump(self.settings, file)

    def load_array(self) -> None:
        """Loads the data from the file data.pkl.
        """
        try:
            with open(self.settings['app_settings']['file_path'], "rb",
                      encoding=None) as file:

                self.data_array = pickle.load(file)
        except FileNotFoundError:
            pass
        except TypeError:
            print('Filepath: None')

    def save_array(self) -> None:
        """Saves the data to the file data.pkl.
        """
        with open(self.settings['app_settings']['file_path'], "wb",
                  encoding=None) as file:

            pickle.dump(self.data_array, file)

    def sort_data_array(self) -> None:
        """Sorts the data_array according to the argument.
        """
        if self.table_state.sort_argument == 'Date up':
            self.data_array.sort(
                key=lambda expenditure: expenditure.date)
        elif self.table_state.sort_argument == 'Date down':
            self.data_array.sort(
                key=lambda expenditure: expenditure.date, reverse=True)
        elif self.table_state.sort_argument == 'Amount up':
            self.data_array.sort(
                key=lambda expenditure: expenditure.amount)
        elif self.table_state.sort_argument == 'Amount down':
            self.data_array.sort(
                key=lambda expenditure: expenditure.amount, reverse=True)

    def get_table_array(self) -> None:
        """Returns the list filtered by the given filters.
        """
        self.sort_data_array()
        self.table_state.table_array = []
        for expenditure in self.data_array:
            expenditure: ExpenditureStrukture
            date_filter: str = f"{self.table_state.year_filter}.{self.table_state.month_filter}"
            if date_filter in expenditure.date:
                self.table_state.table_array.append(expenditure)

        if len(self.table_state.table_array) < 10 or \
                not self.table_state.table_array:

            for _ in range(10 - (len(self.table_state.table_array) % 10)):
                self.table_state.table_array.append(
                    ExpenditureStrukture('', 0, '', ''))

    def append_expenditure(self, person_name: str, amount: float,
                           comment: str, date: str, state=True) -> None:
        """Adds an input to the data_array.
        """
        expenditure = ExpenditureStrukture(person_name, amount, comment, date)
        self.data_array.append(expenditure)
        if state:
            self.get_table_array()

    def remove_expenditure(self, person_name: str, amount: float,
                           comment: str, date: str, state=True
                           ) -> None:
        """Deletes an input from Data_array.
        """
        expenditure = ExpenditureStrukture(person_name, amount, comment, date)
        self.data_array.remove(expenditure)
        if state:
            self.get_table_array()

    def get_personal_expenses(self) -> None:
        """sets the dictionary with the sums of the
            individual persons
        """
        self.get_table_array()
        self.debts_state.personal_expenses = {}
        for expenditure in self.table_state.table_array:
            expenditure: ExpenditureStrukture
            if expenditure.person_name != '':
                if expenditure.person_name in self.debts_state.personal_expenses:
                    self.debts_state.personal_expenses[expenditure.person_name]\
                        += expenditure.amount
                else:
                    self.debts_state.personal_expenses[expenditure.person_name]\
                        = expenditure.amount
        self.debts_state.personal_expenses = dict(
            sorted(self.debts_state.personal_expenses.items(),
                   key=lambda item: item[1]))
        self.debts_state.average_expenses = average(
            self.debts_state.personal_expenses)

    def get_debts_array(self) -> None:
        """sets the array with the transfer data of
            the individual persons
        """
        self.get_personal_expenses()
        self.debts_state.debts_array = []
        persons = list(self.debts_state.personal_expenses.keys())
        amounts = list(self.debts_state.personal_expenses.values())
        list_len = len(persons)
        for i in range(list_len-1):
            if i == 0:
                amount = round(
                    self.debts_state.average_expenses - amounts[i], 2)
                if amount != 0:
                    self.debts_state.debts_array.append(DebtsStrukture(
                        persons[i], persons[i+1], amount))
            else:
                amount = round(self.debts_state.average_expenses - amounts[i]
                               + self.debts_state.debts_array[i-1].amount, 2)
                if amount != 0:
                    self.debts_state.debts_array.append(DebtsStrukture(
                        persons[i], persons[i+1], amount))

    def check_names(self) -> bool:
        """Checks if names appear in the list
            that have not been registered

        Returns:
            bool: _description_
        """
        names = []
        for expenses in self.data_array:
            expenses: ExpenditureStrukture
            if expenses.person_name not in names:
                names.append(expenses.person_name)

        for name in names:
            if name not in self.settings['app_settings']['persons_mames']:
                return False
        return True
