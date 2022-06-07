"""System module."""
from dataclasses import dataclass
from datetime import date as datetime
import os
import json
import pickle

doc_path = os.path.expanduser('~\\Documents')

SETTINGS = {
    "app_settings":
    {
        "appearance": "dark",
        "file_path": f"{doc_path}\\BondMarket 5.0\\data.pkl",
        "currency": "\u20ac",
        "persons_mames": {
            "meith0717@gmail.com": "Meiers Thierry"
            } 
    },
}


@dataclass
class ExpenditureStrukture:
    """Structure of expenses."""
    person_name: str
    amount: float
    comment: str
    date: str


@dataclass
class TableState:
    """Structure of the table state."""
    table_array = []
    sort_argument = "Amount up"
    index = 0
    month_filter = datetime.today().strftime('%m')
    year_filter = datetime.today().strftime('%Y')


@dataclass
class AppState:
    """Structure of the app state"""
    data_array = []
    settings = {}
    table_state = TableState()
    save_state = True

    def load_settings(self) -> None:
        """Loads the data from the file settings.json."""
        try:
            with open(r"Settings\settings.json", "r", encoding="UTF-8") as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = SETTINGS

    def save_settings(self) -> None:
        """Saves the data to the file settings.json."""
        with open(r"Settings\settings.json", "w", encoding="UTF-8") as file:
            json.dump(self.settings, file)

    def load_array(self) -> None:
        """Loads the data from the file data.pkl."""
        try:
            with open(self.settings['app_settings']['file_path'], "rb", encoding=None) as file:
                self.data_array = pickle.load(file)
        except FileNotFoundError:
            pass

    def save_array(self) -> None:
        """Saves the data to the file data.pkl."""
        try:
            with open(self.settings['app_settings']['file_path'], "wb", encoding=None) as file:
                pickle.dump(self.data_array, file)
        except FileNotFoundError:
            os.mkdir(f"{doc_path}\\BondMarket 5.0")
            with open(self.settings['app_settings']['file_path'], "wb", encoding=None) as file:
                pickle.dump(self.data_array, file)

    def sort_data_array(self) -> None:
        """Sorts the data_array according to the argument."""
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
        """Returns the list filtered by the given filters."""
        self.sort_data_array()
        self.table_state.table_array = []
        for expenditure in self.data_array:
            expenditure: ExpenditureStrukture
            date_filter: str = f"{self.table_state.year_filter}.{self.table_state.month_filter}"
            if date_filter in expenditure.date:
                self.table_state.table_array.append(expenditure)
        if (len(self.table_state.table_array) % 10) != 0 or not self.table_state.table_array:
            for i in range(10 - (len(self.table_state.table_array) % 10)):
                self.table_state.table_array.append(
                    ExpenditureStrukture('', 0, '', ''))

    def append_expenditure(self, person_name: str, amount: float,
                           comment: str, date: str, state=True) -> None:
        """Adds an input to the data_array."""
        expenditure = ExpenditureStrukture(person_name, amount, comment, date)
        self.data_array.append(expenditure)
        if state:
            self.get_table_array()

    def remove_expenditure(self, person_name: str, amount: float,
                           comment: str, date: str, state=True
                           ) -> None:
        """Deletes an input from Data_array."""
        expenditure = ExpenditureStrukture(person_name, amount, comment, date)
        self.data_array.remove(expenditure)
        if state:
            self.get_table_array()
