from tkinter import messagebox

TITLE = 'BondMarket '

def ms_is_running() -> str:
    return messagebox.showwarning(TITLE,
                               '''Please stop the mail service 
before using BondMarket,
otherwise this can 
lead to errors.''')

def want_to_save(path: str) -> bool:
    return messagebox.askyesno(TITLE,
                                  f'''Do you want to save thh changes to the file?
{path}''')

def enter_name() -> str:
    return messagebox.showerror(TITLE,
                                'Please enter Name')

def was_added(s: str) -> str:
    return messagebox.showinfo(TITLE,
                               f'{s} was added.')

def was_removed(s: str) -> str:
    return messagebox.showinfo(TITLE,
                               f'{s} has been removed!')

def name_exist():
    return messagebox.showerror(TITLE,
                                'Name already registered!')

def name_does_not_exist():
    return messagebox.showerror(TITLE,
                                'User doesent exist!')

def send_mail(adress: str):
    return messagebox.showinfo(TITLE,
                               f'Mail has been send to {adress}')

def invalide_mail():
    return messagebox.showinfo(TITLE,
                               'Invalid email address, error!')

def mail_exist():
    return messagebox.showerror(TITLE,
                                'Email address already bound to one person!')

def unknown_error():
    return messagebox.showinfo(TITLE,
                               'Unnown Error!')
    
def enter_all():
    return messagebox.showerror(TITLE,
                                'Please enter all the entries!')
    
def user_detected():
    return messagebox.showwarning(TITLE,
                                  'A user was detected in the table which was not registered ')
