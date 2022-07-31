"""System module."""
from typing import Any
from app.app_state import AppState, ExpenditureStrukture
import messagebox.messagebox as msg
from datetime import date as datetime
from customtkinter.theme_manager import ThemeManager
import customtkinter as ctk

PADX = PADY = IPADX = IPADY = 10
LABLE_TITLE_FONT = ('San Francisco', 20)
FRAME_BG = ThemeManager.theme['color']['frame_low']
YEARS = [str(2000+x) for x in range(22, 30)]
MONTHS = ['01', '02', '03', '04', '05', '06',
          '07', '08', '09', '10', '11', '12']


def table_filter(main_root: ctk.CTk, app_state: AppState) -> None:
    """The funkrion grinds the frame with the settings for the table.

    Args:
        main_root (ctk.CTk)
        app_state (AppState)
    """

    def set_month(value: Any, app_state: AppState) -> None:
        """The function filters the table by month

        Args:
            value (Any)
            app_state (AppState)
        """
        app_state.table_state.month_filter = value
        update_table(app_state)

    def set_year(value: Any, app_state: AppState) -> None:
        """The function filters the table by year

        Args:
            value (Any)
            app_state (AppState)
        """
        app_state.table_state.year_filter = value
        update_table(app_state)

    def sort(argument: str, app_state: AppState) -> None:
        """The function sorts the table according to the
            sort argument

        Args:
            argument (str)
            app_state (AppState)
        """
        app_state.settings["app_settings"]["sort_argument"] = argument
        update_table(app_state)

    root = ctk.CTkFrame(main_root)
    root.pack(side='top', anchor='nw', fill='y',
              padx=PADX, pady=PADY, ipadx=IPADX,
              ipady=IPADY, expand=False)
    ctk.CTkLabel(root, text='Filter      ', text_font=LABLE_TITLE_FONT
                 ).grid(row=0, column=0, pady=5, padx=20, sticky='w')

    ctk.CTkLabel(root, text='Month:'
                 ).grid(row=1, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='Year:'
                 ).grid(row=2, column=0, pady=5, padx=20, sticky='e')

    e1 = ctk.CTkComboBox(root, width=200, values=MONTHS,
                         command=lambda value: set_month(value, app_state))
    e1.set(app_state.table_state.month_filter)
    e1.grid(row=1, column=1, pady=5, sticky='w', padx=20)

    e2 = ctk.CTkComboBox(root, width=200, values=YEARS,
                         command=lambda value: set_year(value, app_state))
    e2.set(app_state.table_state.year_filter)
    e2.grid(row=2, column=1, pady=5, sticky='w', padx=20)

    ctk.CTkLabel(root, text='Sort', text_font=('Segoe UI', 15),
                 width=100).grid(row=5, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='Date up',
                  command=lambda: sort('Date up', app_state)
                  ).grid(row=6, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='Date down',
                  command=lambda: sort('Date down', app_state)
                  ).grid(row=6, column=1, padx=20, pady=5)
    ctk.CTkButton(root, text='Amount up',
                  command=lambda: sort('Amount up', app_state)
                  ).grid(row=7, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='Amount down',
                  command=lambda: sort('Amount down', app_state)
                  ).grid(row=7, column=1, padx=20, pady=5)


def update_entrys_combox(app_state: AppState) -> None:
    """Updates the Combox in the Entry Frame

    Args:
        app_state (AppState)
    """
    e1.configure(values=list(
        app_state.settings["app_settings"]["persons_mames"].keys()))
    e1.set('')


def entrys(main_root, app_state: AppState) -> None:
    """The funkrion grinds the frame with the entrys for the table.

    Args:
        main_root (_type_)
        app_state (AppState)
    """
    global e1, e2, e3, e4

    def add_to_table_array(app_state: AppState, person_name: str,
                           amount: float, comment: str, date: str) -> None:
        """Adds an ExpenditureStrukture to the table

        Args:
            app_state (AppState)
            person_name (str)
            amount (float)
            comment (str)
            date (str)
        """
        if person_name != '' and amount != '' and comment != '':
            app_state.append_expenditure(
                person_name, float(amount), comment, date)
            update_table(app_state)
            e1.set('')
            e2.delete(0, 'end')
            e3.delete(0, 'end')
            e4.delete(0, 'end')
            e4.insert(0, datetime.today().strftime('%Y.%m.%d'))
            app_state.save_state = False
        else:
            msg.enter_all()
    
        if app_state.check_names() is False:
            msg.user_detected()
        

    def remove_from_table_array(app_state: AppState, person_name: str,
                                amount: float, comment: str, date: str) -> None:
        """Remove the given ExpenditureStrukture from the table

        Args:
            app_state (AppState)
            person_name (str)
            amount (float)
            comment (str)
            date (str)
        """
        if person_name != '' and amount != '' and comment != '':
            app_state.remove_expenditure(person_name, float(amount), comment, date)
            app_state.table_state.index = 0
            update_table(app_state)
            e1.set('')
            e2.delete(0, 'end')
            e3.delete(0, 'end')
            e4.delete(0, 'end')
            e4.insert(0, datetime.today().strftime('%Y.%m.%d'))
            app_state.save_state = False
        else:
            msg.enter_all()


    def change_entry_table_array():
        pass

    root = ctk.CTkFrame(main_root)
    root.pack(side='top', anchor='nw', fill='y', padx=PADX,
              pady=PADY, ipadx=IPADX, ipady=IPADY, expand=False)
    ctk.CTkLabel(root, text='Entrys         ', text_font=LABLE_TITLE_FONT
                 ).grid(row=0, column=0, pady=5, padx=20, sticky='w')

    ctk.CTkLabel(root, text='   Person Name:'
                 ).grid(row=1, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='        Amount:'
                 ).grid(row=2, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='       Comment:'
                 ).grid(row=3, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='          Date:'
                 ).grid(row=4, column=0, pady=5, padx=20, sticky='e')

    e1 = ctk.CTkComboBox(root, width=200, hover=False,
                         values=list(app_state.settings["app_settings"]["persons_mames"].keys()))
    e2 = ctk.CTkEntry(root, width=200)
    e3 = ctk.CTkEntry(root, width=200)
    e4 = ctk.CTkEntry(root, width=200)

    e1.set('')
    e1.grid(row=1, column=1, pady=5, padx=20)
    e2.grid(row=2, column=1, pady=5, padx=20)
    e3.grid(row=3, column=1, pady=5, padx=20)
    e4.grid(row=4, column=1, pady=5, padx=20)
    e4.insert(0, datetime.today().strftime('%Y.%m.%d'))

    ctk.CTkButton(root, text='Add',
                  command=lambda: add_to_table_array(
                      app_state, e1.get(), e2.get(), e3.get(), e4.get())
                  ).grid(row=5, column=0, pady=5, padx=20, sticky='w')

    ctk.CTkButton(root, text='Delete',
                  command=lambda: remove_from_table_array(
                      app_state, e1.get(), e2.get(), e3.get(), e4.get())
                  ).grid(row=7, column=0, pady=5, padx=20, sticky='w')


def changet_table_index(app_state: AppState, value: Any) -> None:
    """Changes the index for scrolling

    Args:
        app_state (AppState)
        value (int): value from the slider
    """
    app_state.table_state.index = int(value)
    update_table(app_state)


def update_table(app_state: AppState) -> None:
    """Updates the content of the table

    Args:
        app_state (AppState)
    """
    app_state.get_table_array()
    for i in range(10):
        try:
            expenditure: ExpenditureStrukture = app_state.table_state.table_array[
                i+app_state.table_state.index]
            text_lables[i].configure(text=f"{expenditure.person_name} {expenditure.comment}")
            date_lables[i].configure(text=f"{expenditure.date}")
            if expenditure.amount == 0:
                amount_lables[i].configure(text="")
            else:
                amount_lables[i].configure(
                    text=f"{-expenditure.amount} {app_state.settings['app_settings']['currency']}")
        except IndexError:
            app_state.table_state.index -= 10
            update_table(app_state)


def table(main_root, app_state: AppState) -> None:
    """The funkrion grinds the table.

    Args:
        main_root (_type_)
        app_state (AppState)
    """
    global text_lables, amount_lables, date_lables, slider

    def mouse_wheel(event, app_state: AppState) -> None:
        len_ = len(app_state.table_state.table_array)
        if event.num == 5 or event.delta == -120:
            if app_state.table_state.index < len_ - 10:
                app_state.table_state.index += 1
        if event.num == 4 or event.delta == 120:
            if app_state.table_state.index > 0:
                app_state.table_state.index -= 1
        update_table(app_state)

    def get_row(index: int, app_state: AppState) -> None:
        """Returns the clipped row in the input fields

        Args:
            index (int): _description_
            app_state (AppState): _description_
        """
        expenditure: ExpenditureStrukture = app_state.table_state.table_array[
            app_state.table_state.index+index]
        if expenditure.date != '':
            e2.delete(0, 'end')
            e3.delete(0, 'end')
            e4.delete(0, 'end')
            e1.set(expenditure.person_name)
            e2.insert(0, expenditure.amount)
            e3.insert(0, expenditure.comment)
            e4.insert(0, expenditure.date)

    root = ctk.CTkFrame(main_root, width=300)
    root.pack(side='left', anchor='nw', padx=PADX,
              pady=PADY, ipadx=IPADX, ipady=IPADY, expand=False)
    ctk.CTkLabel(root, text='', width=550, height=5
                 ).pack(side='top')
    root.canvas.bind("<MouseWheel>", lambda e: mouse_wheel(e, app_state))
    row_frames = [ctk.CTkFrame(root, border_width=2,
                               fg_color=ThemeManager.theme['color']['frame_low']) for i in range(10)]
    text_lables = [ctk.CTkLabel(row_frames[i]) for i in range(10)]
    amount_lables = [ctk.CTkLabel(row_frames[i], text_color='red', width=50,
                                  text_font=('San Francisco', 14)) for i in range(10)]
    date_lables = [ctk.CTkLabel(row_frames[i], width=60) for i in range(10)]
    app_state.get_table_array()
    
    for i in range(10):
        row_frames[i].pack(side='top', padx=25, pady=7, fill='x')
        row_frames[i].canvas.bind("<MouseWheel>", lambda e: mouse_wheel(e, app_state))
        expenditure: ExpenditureStrukture = app_state.table_state.table_array[i]
        
        amount_lables[i].pack(side='top', anchor='nw', padx=12, pady=5)
        amount_lables[i].configure(text=f"{-expenditure.amount} {app_state.settings['app_settings']['currency']}")
        
        date_lables[i].pack(side='right', anchor='ne', padx=12, pady=5)
        date_lables[i].configure(text=f"{expenditure.date}")
        
        text_lables[i].pack(side='left', anchor='sw', padx=12, pady=5)
        text_lables[i].configure(text=f"{expenditure.person_name} {expenditure.comment}")


    row_frames[0].canvas.bind('<Button-1>', lambda e: get_row(0, app_state))
    row_frames[1].canvas.bind('<Button-1>', lambda e: get_row(1, app_state))
    row_frames[2].canvas.bind('<Button-1>', lambda e: get_row(2, app_state))
    row_frames[3].canvas.bind('<Button-1>', lambda e: get_row(3, app_state))
    row_frames[4].canvas.bind('<Button-1>', lambda e: get_row(4, app_state))
    row_frames[5].canvas.bind('<Button-1>', lambda e: get_row(5, app_state))
    row_frames[6].canvas.bind('<Button-1>', lambda e: get_row(6, app_state))
    row_frames[7].canvas.bind('<Button-1>', lambda e: get_row(7, app_state))
    row_frames[8].canvas.bind('<Button-1>', lambda e: get_row(8, app_state))
    row_frames[9].canvas.bind('<Button-1>', lambda e: get_row(9, app_state))
    row_frames[0].canvas.bind("<MouseWheel>", lambda e: mouse_wheel(e, app_state))


def draw_info_frame(main_root, app_state: AppState) -> None:
    """_summary_

    Args:
        main_root (_type_)
        app_state (AppState)
    """
    root = ctk.CTkFrame(main_root, width=600, height=600)
    root.pack(side='top', anchor='nw', fill='y', padx=PADX,
              pady=PADY, ipadx=IPADX, ipady=IPADY, expand=False)

    ctk.CTkLabel(root, text='Info           ', text_font=('Segoe UI', 20)
                 ).grid(row=0, column=0, pady=5, padx=20, sticky='w')


def draw_menue_1(main_root: ctk.CTk, app_state: AppState) -> None:
    """_summary_

    Args:
        main_root (ctk.CTk)
        app_state (AppState)
    """
    global root

    root = ctk.CTkFrame(
        main_root,
        fg_color=ThemeManager.theme['color']['window_bg_color'])
    table(root, app_state)
    entrys(root, app_state)
    table_filter(root, app_state)
    root.pack(padx=20, pady=20, fill='both', expand=True)


def destroy_menue_1() -> None:
    """_summary_
    """
    try:
        root.destroy()
    except:
        pass
