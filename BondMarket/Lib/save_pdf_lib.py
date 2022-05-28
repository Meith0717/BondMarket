from tkinter.filedialog import askdirectory
from tkinter import messagebox
from fpdf import FPDF
from app.app_lib import app_state
import calculations.debts_lib as debts_lib

def get_dir_path () -> str or bool:
    path : str = askdirectory()
    if path == '':
        return False
    return path

def get_data_as_list(app : app_state) -> list:
    l : list = [['Person', 'Amount', 'Comment', 'Date']]
    for d in app.data_array:
        if app.settings.month == 'all':
            l += [[d.person_name,d.amount,d.comment,d.date]] 
        else:
            if f"{app.settings.jear}.{app.settings.month}" in d.date:
                l += [[d.person_name,d.amount,d.comment,d.date]]
    l += [[]]
    for d in debts_lib.calc(app):
        l += [[d.name,'Total: '+str(d.amount)]]
    l += [['Total:', debts_lib.get_total(app)]]
    return l

def export (app : app_state) -> None:
    data    : list = get_data_as_list(app)
    path    : str = get_dir_path()
    if path is not False:
        pdf=FPDF(format='letter', unit='in')
        pdf.add_page()
        pdf.set_font('Arial','',10.0) 
        epw = pdf.w - 2*pdf.l_margin
        col_width = epw/4
        th = pdf.font_size
        pdf.ln(4*th)
        pdf.set_font('Arial','B',17.0) 
        pdf.cell(epw, 0.0, 'BondMarket - Invoice', align='C')
        pdf.ln(0.5)
        pdf.set_font('Arial','',10.0) 
        pdf.cell(epw, 0.0, f'Date: {app.settings.month}/{app.settings.jear}', align='R')
        pdf.ln(0.5)
        pdf.set_font('Arial','',14.0) 
        pdf.cell(epw, 0.0, 'Expenses', align='L')
        pdf.ln(0.5)
        pdf.set_font('Arial','',10.0) 
        for row in data:
            for datum in row:
                pdf.cell(col_width, 1.3*th, str(datum), border=1)
            pdf.ln(1.3*th)
        pdf.ln(0.5)
        pdf.set_font('Arial','',14.0) 
        pdf.cell(epw, 0.0, 'Transfers', align='L')
        for transfer in debts_lib.get_transfere_str(app):
            pdf.ln(0.5)
            pdf.set_font('Arial','',10.0) 
            pdf.cell(epw, 0.0, transfer, align='L')
        pdf.output(f'{path}/BondMarket Data.pdf')
        messagebox.showinfo('BondMarket',f'Pdf has been created in {path}/BondMarket Data.pdf')
    
