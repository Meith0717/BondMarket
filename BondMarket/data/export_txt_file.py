from tkinter.filedialog import askdirectory
from tkinter import messagebox
from fpdf import FPDF
from app.app_lib import app_state
from debts.debts_lib import calc, get_transfere_str

def get_dir_path () -> str or bool:
    path : str = askdirectory()
    if path == '':
        return False
    return path

def get_data_as_list(app : app_state) -> list:
    l : list = ['', '__Data__', '', f"{'Name:'}   {'Amount:'}   {'Comment:'}   {'Date:'}"]
    c : list = calc(app)
    debts : list = get_transfere_str(app)
    for d in app.data_array:
        if app.settings.month == 'all':
            l += [f"{d.person_name}     {d.amount}     {d.comment}     {d.date}"] 
        else:
            if f"{app.settings.jear}.{app.settings.month}" in d.date:
                l += [f"{d.person_name}     {d.amount}     {d.comment}     {d.date}"] 
    l += ['', '__Totlas__', '']
    l += [f"{'Name:'}     {'Amount:'}"]
    for d in c:
        l += [f'{ d.name}     {str(d.amount)}']
    l += ['', '__Debts__', '']
    for i in debts:
        l += [f'{i}']
    return l

def export (app : app_state) -> None:
    lines   : list = get_data_as_list(app)
    path    : str = get_dir_path()
    if path is not False:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font(family='Arial', size=20)
        pdf.cell(200, 3, txt=f'BondMarked Invoice {app.settings.month}/{app.settings.jear}', ln=5, align='C')
        pdf.set_font('Arial', size=8)
        for line in lines:
            pdf.cell(200, 3, txt=line, ln=1, align='L')
        pdf.output(f'{path}/BondMarket Data.pdf')
        messagebox.showinfo('Info',  f'Pdf has been created in {path}/BondMarket Data.pdf')
    
