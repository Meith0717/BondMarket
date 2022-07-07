from tkinter.filedialog import askdirectory
from app.app_state import AppState
import messagebox.messagebox as messagebox
from fpdf import FPDF

def get_dir_path () -> str or bool:
    path : str = askdirectory()
    if path == '':
        return False
    return path

def export (app_state : AppState) -> bool:
    data = [['Person', 'Amount', 'Comment', 'Date']]
    debts = [f'{x.sender} -> {x.receiver} : {x.amount}' for x in app_state.debts_state.debts_array]
    for x in app_state.table_state.table_array:
        data.append([x.person_name, x.amount, x.comment, x.date])
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
        pdf.cell(epw, 0.0, f'Date: {app_state.table_state.month_filter}/{app_state.table_state.year_filter}', align='R')
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
        for transfer in debts:
            pdf.ln(0.5)
            pdf.set_font('Arial','',10.0) 
            pdf.cell(epw, 0.0, transfer, align='L')
        pdf.output(f'{path}/BondMarket Data.pdf')
        messagebox.pdf_saved(path)