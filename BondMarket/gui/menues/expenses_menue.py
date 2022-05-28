import customtkinter as ctk
from customtkinter.theme_manager import ThemeManager
from datetime import date as datetime
from tkinter import messagebox
from app.app_state import AppState, ExpenditureStrukture

# Filter Frame ###########################################################################


def draw_table_settings(main_root, app_state: AppState, side: str, anchor: str, fill: str, padx: int, pady: int, ipadx: int, ipady: int):

    def filter(app_state: AppState):
        app_state.table_state.month_filter = e1.get()
        app_state.table_state.year_filter = e2.get()
        slider.set(0)
        update_table(app_state)

    def sort(argument: str, app_state: AppState) -> None:
        app_state.table_state.sort_argument = argument
        update_table(app_state)

    root = ctk.CTkFrame(main_root)
    root.pack(side=side, anchor=anchor, padx=padx,
              pady=pady, ipadx=ipadx, ipady=ipady, expand=False)
    ctk.CTkLabel(root, text='Filter           ', text_font=('Segoe UI', 20)
                 ).grid(row=0, column=0, pady=5, padx=20, sticky='w')
    ctk.CTkLabel(root, text='           Month:'
                 ).grid(row=1, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='            Year:'
                 ).grid(row=2, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='     Comment Key:'
                 ).grid(row=3, column=0, pady=5, padx=20, sticky='e')
    e1 = ctk.CTkEntry(root)
    e2 = ctk.CTkEntry(root)
    e3 = ctk.CTkEntry(root)
    e2.insert(0, app_state.table_state.year_filter)
    e1.insert(0, app_state.table_state.month_filter)
    e1.grid(row=1, column=1, pady=5, sticky='w', padx=20)
    e2.grid(row=2, column=1, pady=5, sticky='w', padx=20)
    e3.grid(row=3, column=1, pady=5, sticky='w', padx=20)
    ctk.CTkButton(root, text='Apply',
                  command=lambda: filter(app_state)).grid(row=4, pady=5, padx=20)
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

# Entrys Funktions #####################################################################


def draw_entrys(main_root, app_state: AppState, side: str, anchor: str, fill: str, padx: int, pady: int, ipadx: int, ipady: int):
    global e1, e2, e3, e4

    def add_to_table_array(app_state: AppState, person_name: str, amount: float, comment: str, date: str):
        if person_name == '' and amount == '' and comment == '':
            pass
        elif person_name == '':
            messagebox.showerror('BondMarket', 'Please enter a name')
        elif amount == '':
            messagebox.showerror('BondMarket', 'Please enter an amount')
        elif date == '':
            messagebox.showerror('BondMarket', 'Please enter a date')
        else:
            app_state.append_expenditure(
                person_name, float(amount), comment, date)
            update_table(app_state)
            e1.delete(0, 'end')
            e2.delete(0, 'end')
            e3.delete(0, 'end')
            e4.delete(0, 'end')

    def remove_from_table_array(app_state: AppState, person_name: str, amount: float, comment: str, date: str):
        app_state.remove_expenditure(person_name, float(amount), comment, date)
        update_table(app_state)
        e1.delete(0, 'end')
        e2.delete(0, 'end')
        e3.delete(0, 'end')
        e4.delete(0, 'end')
        e4.insert(0, datetime.today().strftime('%Y.%m.%d'))

    root = ctk.CTkFrame(main_root)
    root.pack(side=side, anchor=anchor, padx=padx, pady=pady,
              ipadx=ipadx, ipady=ipady, expand=False)
    ctk.CTkLabel(root, text='Entrys         ', text_font=('Segoe UI', 20)
                 ).grid(row=0, column=0, pady=5, padx=20, sticky='w')
    ctk.CTkLabel(root, text='   Person Name:'
                 ).grid(row=1, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='        Amount:'
                 ).grid(row=2, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='       Comment:'
                 ).grid(row=3, column=0, pady=5, padx=20, sticky='e')
    ctk.CTkLabel(root, text='          Date:'
                 ).grid(row=4, column=0, pady=5, padx=20, sticky='e')
    e1 = ctk.CTkEntry(root)
    e2 = ctk.CTkEntry(root)
    e3 = ctk.CTkEntry(root)
    e4 = ctk.CTkEntry(root)
    e1.grid(row=1, column=1, pady=5, padx=20)
    e2.grid(row=2, column=1, pady=5, padx=20)
    e3.grid(row=3, column=1, pady=5, padx=20)
    e4.grid(row=4, column=1, pady=5, padx=20)
    e4.insert(0, datetime.today().strftime('%Y.%m.%d'))
    ctk.CTkButton(root, text='Add',
                  command=lambda: add_to_table_array(
                      app_state, e1.get(), e2.get(), e3.get(), e4.get())
                  ).grid(row=5, column=0, pady=5, padx=20)
    ctk.CTkButton(root, text='Change'
                  ).grid(row=6, column=0, pady=5, padx=20)
    ctk.CTkButton(root, text='Delete',
                  command=lambda: remove_from_table_array(
                      app_state, e1.get(), e2.get(), e3.get(), e4.get())
                  ).grid(row=7, column=0, pady=5, padx=20)


# Table Funktions ######################################################################


def changet_table_index(app_state: AppState, value: int):
    app_state.table_state.index = int(value)
    update_table(app_state)


def update_table(app_state: AppState):
    app_state.get_table_array()
    n = len(app_state.table_state.table_array)-10
    if n == 0:
        slider.config(from_=100, command=None)
    else:
        slider.config(from_=n, number_of_steps=n,
                      command=lambda value: changet_table_index(app_state, value))
    for i in range(10):
        try:
            expenditure: ExpenditureStrukture = app_state.table_state.table_array[
                i+app_state.table_state.index]
            name_lables[i].config(text=f"{expenditure.person_name}")
            info_lables[i].config(text=f"{expenditure.comment}")
            date_lables[i].config(text=f"{expenditure.date}")
            if expenditure.amount == 0:
                amount_lables[i].config(text="")
            else:
                amount_lables[i].config(
                    text=f"- {expenditure.amount} {app_state.settings['app_settings']['currency']}")
        except IndexError:
            app_state.table_state.index -= 10
            update_table(app_state)


def draw_table(main_root, app_state: AppState, side: str, anchor: str, fill: str, padx: int, pady: int, ipadx: int, ipady: int) -> None:

    global name_lables, info_lables, amount_lables, date_lables, slider
    frame_bg = ThemeManager.theme['color']['frame_low']

    def get_row(index: int, app_state: AppState):
        '''Returns the clipped row in the input fields'''
        try:
            expenditure: ExpenditureStrukture = app_state.table_state.table_array[
                app_state.table_state.index+index]
            e1.delete(0, 'end')
            e2.delete(0, 'end')
            e3.delete(0, 'end')
            e4.delete(0, 'end')
            e1.insert(0, expenditure.person_name)
            e2.insert(0, expenditure.amount)
            e3.insert(0, expenditure.comment)
            e4.insert(0, expenditure.date)
        except IndexError:
            pass

    root = ctk.CTkFrame(main_root)
    root.pack(side=side, anchor=anchor, padx=padx, pady=pady,
              ipadx=ipadx, ipady=ipady, expand=False)
    row_frames = [ctk.CTkFrame(
        root, height=55, width=350, fg_color=frame_bg) for i in range(10)]
    name_lables = [ctk.CTkLabel(row_frames[i], text_font=(
        'San Francisco', 16), width=200) for i in range(10)]
    info_lables = [ctk.CTkLabel(row_frames[i], width=200) for i in range(10)]
    amount_lables = [ctk.CTkLabel(row_frames[i], text_font=(
        'San Francisco', 18), width=200) for i in range(10)]
    date_lables = [ctk.CTkLabel(row_frames[i]) for i in range(10)]
    ctk.CTkButton(root, text='', width=20, height=20, command=lambda: get_row(
        0, app_state)).grid(row=0, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='', width=20, height=20, command=lambda: get_row(
        1, app_state)).grid(row=1, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='', width=20, height=20, command=lambda: get_row(
        2, app_state)).grid(row=2, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='', width=20, height=20, command=lambda: get_row(
        3, app_state)).grid(row=3, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='', width=20, height=20, command=lambda: get_row(
        4, app_state)).grid(row=4, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='', width=20, height=20, command=lambda: get_row(
        5, app_state)).grid(row=5, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='', width=20, height=20, command=lambda: get_row(
        6, app_state)).grid(row=6, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='', width=20, height=20, command=lambda: get_row(
        7, app_state)).grid(row=7, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='', width=20, height=20, command=lambda: get_row(
        8, app_state)).grid(row=8, column=0, padx=20, pady=5)
    ctk.CTkButton(root, text='', width=20, height=20, command=lambda: get_row(
        9, app_state)).grid(row=9, column=0, padx=20, pady=5)
    app_state.get_table_array()
    for i in range(10):
        row_frames[i].grid(row=i, column=1, padx=5, pady=7)
        expenditure: ExpenditureStrukture = app_state.table_state.table_array[i]
        name_lables[i].config(text=f"{expenditure.person_name}")
        name_lables[i].grid(row=0, column=0, padx=6, pady=6)
        info_lables[i].config(text=f"{expenditure.comment}")
        info_lables[i].grid(row=1, column=0, padx=6, pady=6)
        date_lables[i].config(text=f"{expenditure.date}")
        date_lables[i].grid(row=1, column=1, padx=6, pady=6)
        if expenditure.amount == 0:
            amount_lables[i].config(text="")
        else:
            amount_lables[i].config(
                text=f"- {expenditure.amount} {app_state.settings['app_settings']['currency']}")
        amount_lables[i].grid(row=0, rowspan=3, column=2, padx=6, pady=5)
    n = len(app_state.table_state.table_array)-10
    if n == 0:
        slider = ctk.CTkSlider(root, from_=100, to=0,
                               orient="vertical", height=750)
    else:
        slider = ctk.CTkSlider(root, from_=n, to=0, command=lambda value: changet_table_index(
            app_state, value), orient="vertical", number_of_steps=n, height=750)
    slider.set(0)
    slider.grid(row=0, rowspan=9, column=2)


# Plot Frame ###########################################################################

def draw_plot_frame(main_root, app_state: AppState, side: str, anchor: str, fill: str, padx: int, pady: int, ipadx: int, ipady: int) -> None:
    root = ctk.CTkFrame(main_root, width=600, height=600)
    root.pack(side=side, anchor=anchor, padx=padx, pady=pady,
              ipadx=ipadx, ipady=ipady, expand=False)

    ctk.CTkLabel(root, text='Info           ', text_font=('Segoe UI', 20)
                 ).grid(row=0, column=0, pady=5, padx=20, sticky='w')

# Main Frame Funktions #################################################################


def draw_menue_1(main_root, app_state: AppState):
    global root

    root = ctk.CTkFrame(
        main_root, fg_color=ThemeManager.theme['color']['window_bg_color'])
    title = ctk.CTkLabel(root, text='Expanses', text_font=('Segoe UI', 20))
    title.pack(side='top', anchor='w', padx=5, pady=5)
    draw_table(root, app_state, 'left', 'nw', 'both', 10, 10, 10, 10)
    draw_table_settings(root, app_state, 'top', 'nw', 'both', 10, 10, 10, 10)
    draw_entrys(root, app_state, 'top', 'nw', 'both', 10, 10, 10, 10)
    draw_plot_frame(root, app_state, 'top', 'nw', 'both', 10, 10, 10, 10)
    root.pack(padx=20, pady=10, ipady=500, fill='both', expand=True)
    root.canvas.bind('<Return>', lambda: print('pass'))


def destroy_menue_1():
    try:
        root.destroy()
    except:
        pass
