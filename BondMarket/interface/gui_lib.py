code_autor = "Thierry Meiers"
code_copyright = "Copyright © 2022 Thierry Meiers" 
code_version = "4.1"

import tkinter as tk
import webbrowser
import tkinter.font
import app.app_lib as app_lib
import lib.save_backup_lib as save_backup_lib
import lib.save_pdf_lib as save_pdf_lib 
import calculations.debts_lib as debts_lib
from lib.save_data_lib import save_data_in_file, save_settings_in_file, read_data_from_file, read_settings_from_file, read_from_pkl
from app.theme_lib import LIGHT, DARK
from datetime import date
from tkinter import messagebox, filedialog

def update_screen(app : app_lib.app_state):
    combo1.config(values=tuple(app_lib.find_names(app)))
    tree.delete(*tree.get_children())
    for d in app.data_array:
        if app.settings.month == 'all':
            tree.insert('', 'end', values=(d.person_name, d.amount, d.comment, d.date)) 
        else:
            if f"{app.settings.jear}.{app.settings.month}" in d.date:
                tree.insert('', 'end', values=(d.person_name, d.amount, d.comment, d.date)) 
     
    e4.delete(0, 'end')
    if app.settings.month == 'all' or app.settings.month == date.today().strftime("%m"):
        e4.insert(0, date.today().strftime("%Y.%m.%d"))
    else:
        e4.insert(0, f"{app.settings.jear}.{app.settings.month}.01")

    data_path.config(text='Path:  ' + app.settings.data_path)
    average_expenses.config(text=debts_lib.get_average(app))
    total_expenses.config(text=debts_lib.get_total(app))
    
    l : list = debts_lib.calc_expand(app)
    s : list = debts_lib.get_transfere_str(app)
    s0.config(text= f"{l[0].name}{l[0].amount}")
    s1.config(text= f"{l[1].name}{l[1].amount}")
    s2.config(text= f"{l[2].name}{l[2].amount}")
    s3.config(text= f"{l[3].name}{l[3].amount}")
    s4.config(text= f"{l[4].name}{l[4].amount}")
    s5.config(text= f"{l[5].name}{l[5].amount}")
    s6.config(text= f"{l[6].name}{l[6].amount}")
    s7.config(text= f"{l[7].name}{l[7].amount}")
    s8.config(text= f"{l[8].name}{l[8].amount}")
    s9.config(text= f"{l[9].name}{l[9].amount}")
    d0.config(text=s[0])
    d1.config(text=s[1])
    d2.config(text=s[2])
    d3.config(text=s[3])
    d4.config(text=s[4])
    d5.config(text=s[5])
    d6.config(text=s[6])
    d7.config(text=s[7])
    d8.config(text=s[8])
    d9.config(text=s[9])
    df0.config(text=f"{l[0].name}{l[0].difference}")
    df1.config(text=f"{l[1].name}{l[1].difference}")
    df2.config(text=f"{l[2].name}{l[2].difference}")
    df3.config(text=f"{l[3].name}{l[3].difference}")
    df4.config(text=f"{l[4].name}{l[4].difference}")
    df5.config(text=f"{l[5].name}{l[5].difference}")
    df6.config(text=f"{l[6].name}{l[6].difference}")
    df7.config(text=f"{l[7].name}{l[7].difference}")
    df8.config(text=f"{l[8].name}{l[8].difference}")
    df9.config(text=f"{l[9].name}{l[9].difference}")

def safe_to_dataarray (app : app_lib.app_state):
    if combo1.get() == ''  or e3.get() == '':
        return
    if len(app_lib.find_names(app))+1 > 10 and combo1.get() not in app_lib.find_names(app):
        messagebox.showwarning('BondMarket', 'Name Error: Only 10 persons are allowed')
    else:
        try:
            name : str = combo1.get()
            amount : float = str(float(e2.get()))
            comment : str = e3.get()
            date : str = e4.get()
            app_lib.push_to_data_array(app, name, amount, comment, date)
            tree.insert('', 0, values=(combo1.get(), e2.get(), e3.get(), e4.get()))
            clear(app)
            update_screen(app)
        except ValueError:
            messagebox.showerror('BondMarket', message='Amount Error: Please enter a Number')

def delet_from_dataarray (app : app_lib.app_state):
    app_lib.pop_from_data_array(app, combo1.get(), e2.get(), e3.get(), e4.get())
    clear(app)
    update_screen(app)

def ask_to_save(app : app_lib.app_state):
    if app.safe_state_data: 
        pass
    else:
        if messagebox.askyesno('BondMarket', f'Do you want to save the changes to\n{app.settings.data_path}?'):
            save_data_in_file(app)
    save_settings_in_file(app)

def exit (root : tk.Tk, app : app_lib.app_state):
    app.settings.first_start = False
    ask_to_save(app)
    root.destroy()

def OnDoubleClick(app: app_lib.app_state, event):
    global e5
    clear(app)
    curItem = tree.item(tree.focus())
    try:
        combo1.insert(0, curItem['values'][0])
        e2.insert(0, curItem['values'][1])
        e3.insert(0, curItem['values'][2])
        e4.delete(0, 100)
        e4.insert(0, curItem['values'][3])
    except IndexError:
        pass

def save (app : app_lib.app_state):
    app.safe_state_data = True
    save_data_in_file(app)
    save_settings_in_file(app)
    update_screen(app)
    
def clear (app : app_lib.app_state):
    combo1.delete(0, 100)
    e2.delete(0, 100)
    e3.delete(0, 100)
    e4.delete(0, 100)
    if app.settings.month == 'all' or app.settings.month == date.today().strftime("%m"):
        e4.insert(0, date.today().strftime("%Y.%m.%d"))
    else:
        e4.insert(0, f"{app.settings.jear}.{app.settings.month}.01")

def open_file (app : app_lib.app_state):
    ask_to_save(app)
    prew_path = app.settings.data_path
    app.settings.data_path = filedialog.askopenfilename(filetypes=[('PKL', '.pkl')]).replace('/', '\\')
    if app.settings.data_path == '' or prew_path == app.settings.data_path:
        app.settings.data_path = prew_path
    else:
        if read_data_from_file(app) == 'Error':
            messagebox.showerror('BondMarket', 'An error occurred while reading the file.\n\nProbably the file is not compatible!')
            app.settings.data_path = prew_path
        else:
            save_settings_in_file(app)
        app.safe_state_data = True
    update_screen(app)

def open_new_file (app : app_lib.app_state):
    ask_to_save(app)
    ask_to_save(app)
    prew_path = app.settings.data_path
    app.settings.data_path = filedialog.asksaveasfilename(filetypes=[('PKL', '.pkl')]).replace('/', '\\')
    if app.settings.data_path == '' or prew_path == app.settings.data_path:
        app.settings.data_path = prew_path
    else:
        app.safe_state_data = True
        app.data_array = []
        save_settings_in_file(app)
        save_data_in_file(app)
        update_screen(app)
      
def restore_backup(app : app_lib.app_state):
    if app.safe_state_data is False:
        return
    if messagebox.askyesno('BondMarket', 'Are you sure you want to recover the data? Data can be lost'):
        path = filedialog.askopenfilename(filetypes=[('PKL', '.pkl')])
        if path != '':
            app.data_array = read_from_pkl(path)
            update_screen(app)

def table_ (root, app : app_lib.app_state):
    global tree
    tree = tk.ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings', selectmode='browse', height=200)
    vsb = tk.ttk.Scrollbar(root, orient='vertical', command=tree.yview)
    headline : list = ['Person', 'Amount', 'Comment', 'Date']
    tree.tag_configure('odd', background='#F4F6F7')
    tree.tag_configure('even', background='#F0F3F4')

    tree.column("# 1", width=8, anchor='w')
    tree.heading("# 1", text=headline[0], anchor='w')
    tree.column("# 2", width=8, anchor='w')
    tree.heading("# 2", text=headline[1], anchor='w')
    tree.column("# 3", width=89, anchor='w')
    tree.heading("# 3", text=headline[2], anchor='w')
    tree.column("# 4", width=15, anchor='w')
    tree.heading("# 4", text=headline[3], anchor='w')

    for d in app.data_array:
        if app.settings.month == 'all':
            tree.insert('', 'end', values=(d.person_name, d.amount, d.comment, d.date)) 
        else:
            if f"{app.settings.jear}.{app.settings.month}" in d.date:
                tree.insert('', 'end', values=(d.person_name, d.amount, d.comment, d.date)) 

    vsb.pack(side='right', anchor='se', fill='y', pady=1, padx=0)
    tree.pack(fill='both', padx=2, pady=2)
    tree.config(yscrollcommand=vsb.set)
    tree.bind("<Double-1>", lambda event: OnDoubleClick(app, event))

def settings_ (main_root : tk.Tk, root : tk.Tk, app : app_lib.app_state, resrart_funktion) :
    global data_path, open, backup

    def save_appearance (app : app_lib.app_state):
        if sel_apperance.get() in str(app.settings.appearance):
            return
        if sel_apperance.get() == 'LIGHT':
            app.settings.appearance = LIGHT
        if sel_apperance.get() == 'DARK':
            app.settings.appearance = DARK
        save_settings_in_file(app)
        if messagebox.askyesno('BondMarket', 'Do you want to restart the application for the changes to take effect!'):
            exit(main_root, app)
            resrart_funktion()

    def save_filter (app : app_lib.app_state):
        if jear.get() == '' or month.get() == '':
            pass
        else:
            app.settings.jear = jear.get()
            app.settings.month = month.get()
            update_screen(app)

    def clear (app : app_lib.app_state):
        if messagebox.askyesno(title='BondMarket', message='Are you sure you want to delete everything?'):
            app.data_array = []
            app.safe_state_data = False
            update_screen(app)

    # Appearance Settings ##########
    tk.Label(root, text='Appearance:', font=tkinter.font.Font(family="Segoe UI", size=12, weight='bold'), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).grid(row=1, sticky='w', pady=5, padx=1)
    sel_apperance = tk.StringVar()
    sel_apperance.set(app.settings.appearance.name)
    tk.ttk.Radiobutton(root, text='White', value='LIGHT', variable=sel_apperance).grid(row=2, column=0, sticky='w', pady=5, padx=1)
    tk.ttk.Radiobutton(root, text='Dark', value='DARK', variable=sel_apperance).grid(row=3, column=0, sticky='w', pady=5, padx=1)
    tk.ttk.Button(root, text='Apply', command=(lambda : save_appearance(app))).grid(row=4, column=0, padx=5, pady=5)
    # Table Settings ##########
    tk.Label(root, text='Table:', font=tkinter.font.Font(family="Segoe UI", size=12, weight='bold'), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).grid(row=5, sticky='w', pady=5, padx=1)
    tk.Label(root, text='Month:', fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).grid(row=6, sticky='w', pady=5, padx=1)
    month = tk.ttk.Combobox(root, values=tuple(x for x in ['all', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11' ,'12']))
    month.grid(row=6,column=1,sticky='w', pady=5, padx=1)
    month.insert(0, app.settings.month)
    tk.Label(root, text='Jear:', fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).grid(row=7, sticky='w', pady=5, padx=1)
    jear = tk.ttk.Combobox(root, values=tuple(x for x in range(2000, 2100)))
    jear.grid(row=7,column=1,sticky='w', pady=5, padx=1)
    jear.insert(0, app.settings.jear)
    tk.ttk.Button(root, text='Apply', command=(lambda : save_filter(app))).grid(row=8, column=0, padx=5, pady=5)
    tk.ttk.Button(root, text='Clear Table', command=(lambda : clear(app))).grid(row=8, column=1, padx=5, pady=5)
    # Path Settings ##########
    tk.Label(root, text='Data File Path:', font=tkinter.font.Font(family="Segoe UI", size=12, weight='bold'), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).grid(row=9, sticky='w', pady=5, padx=1)
    data_path = tk.Label(root, text=app.settings.data_path.replace('/', '\\'), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color, width=45, anchor='w')
    data_path.grid(row=12, columnspan=2, sticky='w')
    tk.Label(root, text=f"Default: ~\Documents\BondMarket", fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color, width=45, anchor='w').grid(row=13, columnspan=2, sticky='w')

def info_ (root, app : app_lib) :
   
    def open_link (link : str):
        if messagebox.askokcancel('BondMarket',f"You will be redirected to:\n{link}\n\nDo you want to continue?"):
            webbrowser.open(link, new=0, autoraise=True)

    tk.Label(root, text='Shortcuts:', font=tkinter.font.Font(family="Segoe UI", size=12, weight='bold'), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=0, column=0, sticky='w')
    tk.Label(root, text='Save Entry:', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=1, column=0, sticky='w')
    tk.Label(root, text='ENTER', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=1, column=1, sticky='w', padx=10)
    tk.Label(root, text='Deleete Entry:', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=2, column=0, sticky='w')
    tk.Label(root, text='DELETE', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=2, column=1, sticky='w', padx=10)
    tk.Label(root, text='Exit:', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=3, column=0, sticky='w')
    tk.Label(root, text='ESCAPE', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=3, column=1, sticky='w', padx=10)
    tk.Label(root, text='Save File:', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=4, column=0, sticky='w')
    tk.Label(root, text='Control-s', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=4, column=1, sticky='w', padx=10)
    tk.Label(root, text='Open File:', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=5, column=0, sticky='w')
    tk.Label(root, text='Control-o', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=5, column=1, sticky='w', padx=10)
    tk.Label(root, text='New File', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=6, column=0, sticky='w')
    tk.Label(root, text='Control-n', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=6, column=1, sticky='w', padx=10)

    tk.Label(root, text='Info:', font=tkinter.font.Font(family="Segoe UI", size=12, weight='bold'), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=10, column=0, sticky='w')
    tk.Button(root, text='Github', relief='flat', font=tkinter.font.Font(underline=True, size=8),fg='#0082FF', bg=app.settings.appearance.lb_color, activebackground=app.settings.appearance.lb_color, command=(lambda : open_link('https://github.com/Meith0717/BondMarket.git'))).grid(row=11, column=0, sticky='w')
    tk.Button(root, text='Discord', relief='flat', font=tkinter.font.Font(underline=True, size=8),fg='#0082FF', bg=app.settings.appearance.lb_color, activebackground=app.settings.appearance.lb_color, command=(lambda : open_link('https://discordapp.com/users/773830054726860811/'))).grid(row=12, column=0, sticky='w')
    tk.Button(root, text='Donate', relief='flat', font=tkinter.font.Font(underline=True, size=8),fg='#0082FF', bg=app.settings.appearance.lb_color, activebackground=app.settings.appearance.lb_color, command=(lambda : open_link('https://www.paypal.com/donate/?hosted_button_id=47BGH5AWNSV88'))).grid(row=13, column=0, sticky='w')

def expenses_ (root : tk.Tk, app : app_lib.app_state):
    global s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, average_expenses, total_expenses
    tk.Label(root, text='Average Expenses:', font=tkinter.font.Font(family="Segoe UI", size=12, weight='bold'), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=1, column=0, sticky='w', pady=1, padx=2)
    average_expenses = tk.Label(root, text=debts_lib.get_average(app), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    average_expenses.grid(row=2, column=0, sticky='w', padx=30)
    tk.Label(root, text='Total expenses:', font=tkinter.font.Font(family="Segoe UI", size=12, weight='bold'), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=3, column=0, sticky='w', pady=1, padx=2)
    total_expenses = tk.Label(root, text=debts_lib.get_total(app), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    total_expenses.grid(row=4, column=0, sticky='w', padx=30)
    l : list = debts_lib.calc_expand(app)
    tk.Label(root, text='Personal expenses:', font=tkinter.font.Font(family="Segoe UI", size=12, weight='bold'), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=5, column=0, sticky='w', pady=1, padx=2)
    s0 = tk.Label(root, text= f"{l[0].name}{l[0].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    s0.grid(row=6, column=0, sticky='w', pady=2, padx=30)
    s1 = tk.Label(root, text= f"{l[1].name}{l[1].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    s1.grid(row=7, column=0, sticky='w', pady=2, padx=30)
    s2 = tk.Label(root, text= f"{l[2].name}{l[2].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    s2.grid(row=8, column=0, sticky='w', pady=2, padx=30)
    s3 = tk.Label(root, text= f"{l[3].name}{l[3].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    s3.grid(row=9, column=0, sticky='w', pady=2, padx=30)
    s4 = tk.Label(root, text= f"{l[4].name}{l[4].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    s4.grid(row=10, column=0, sticky='w', pady=2, padx=30)
    s5 = tk.Label(root, text= f"{l[5].name}{l[5].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    s5.grid(row=11, column=0, sticky='w', pady=2, padx=30)
    s6 = tk.Label(root, text= f"{l[6].name}{l[6].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    s6.grid(row=12, column=0, sticky='w', pady=2, padx=30)
    s7 = tk.Label(root, text= f"{l[7].name}{l[7].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    s7.grid(row=13, column=0, sticky='w', pady=2, padx=30)
    s8 = tk.Label(root, text= f"{l[8].name}{l[8].amount} " , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    s8.grid(row=14, column=0, sticky='w', pady=2, padx=30)
    s9 = tk.Label(root, text= f"{l[9].name}{l[9].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    s9.grid(row=15, column=0, sticky='w', pady=2, padx=30)

def debts_ (root: tk.Tk, app : app_lib.app_state):
    global d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, df0, df1, df2, df3, df4, df5, df6, df7, df8, df9
    s : list = debts_lib.get_transfere_str(app)
    l : list = debts_lib.calc_expand(app)
    d0 = tk.Label(root, text=s[0], bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    d0.grid(row=1, column=0, sticky='w', pady=2, padx=30)
    d1 = tk.Label(root, text=s[1], bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    d1.grid(row=2, column=0, sticky='w', pady=2, padx=30)
    d2 = tk.Label(root, text=s[2] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    d2.grid(row=3, column=0, sticky='w', pady=2, padx=30)
    d3 = tk.Label(root, text=s[3] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    d3.grid(row=4, column=0, sticky='w', pady=2, padx=30)
    d4 = tk.Label(root, text=s[4], bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    d4.grid(row=5, column=0, sticky='w', pady=2, padx=30)
    d5 = tk.Label(root, text=s[5] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    d5.grid(row=6, column=0, sticky='w', pady=2, padx=30)
    d6 = tk.Label(root, text=s[6] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    d6.grid(row=7, column=0, sticky='w', pady=2, padx=30)
    d7 = tk.Label(root, text=s[7] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    d7.grid(row=8, column=0, sticky='w', pady=2, padx=30)
    d8 = tk.Label(root, text=s[8] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    d8.grid(row=9, column=0, sticky='w', pady=2, padx=30)
    d9 = tk.Label(root, text=s[9] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    d9.grid(row=10, column=0, sticky='w', pady=2, padx=30)
    tk.Label(root, text='Transfers:', font=tkinter.font.Font(family="Segoe UI", size=12, weight='bold'), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=0, column=0, sticky='w', pady=1, padx=2)
    df0 = tk.Label(root, text=f"{l[0].name}{l[0].difference}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    df0.grid(row=12, column=0, sticky='w', pady=2, padx=30)
    df1 = tk.Label(root, text=f"{l[1].name}{l[1].difference}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    df1.grid(row=13, column=0, sticky='w', pady=2, padx=30)
    df2 = tk.Label(root, text=f"{l[2].name}{l[2].difference}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    df2.grid(row=14, column=0, sticky='w', pady=2, padx=30)
    df3 = tk.Label(root, text=f"{l[3].name}{l[3].difference}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    df3.grid(row=15, column=0, sticky='w', pady=2, padx=30)
    df4 = tk.Label(root, text=f"{l[4].name}{l[4].difference}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    df4.grid(row=16, column=0, sticky='w', pady=2, padx=30)
    df5 = tk.Label(root, text=f"{l[5].name}{l[5].difference}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    df5.grid(row=17, column=0, sticky='w', pady=2, padx=30)
    df6 = tk.Label(root, text=f"{l[6].name}{l[6].difference}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    df6.grid(row=18, column=0, sticky='w', pady=2, padx=30)
    df7 = tk.Label(root, text=f"{l[7].name}{l[7].difference}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    df7.grid(row=19, column=0, sticky='w', pady=2, padx=30)
    df8 = tk.Label(root, text=f"{l[8].name}{l[8].difference}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    df8.grid(row=20, column=0, sticky='w', pady=2, padx=30)
    df9 = tk.Label(root, text=f"{l[9].name}{l[9].difference}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color, font=tkinter.font.Font(size=9))
    df9.grid(row=21, column=0, sticky='w', pady=2, padx=30)
    tk.Label(root, text='Personal difference:', font=tkinter.font.Font(family="Segoe UI", size=12, weight='bold'), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=11, column=0, sticky='w', pady=1, padx=2)

def entry_ (root : tk.Tk, app : app_lib.app_state):
    # cavas ##############################################################################################
    fields : list = ['Person:', 'Amount:', 'Comment:', 'Date:']
    for i, field in enumerate(fields):
        tk.Label(root, width=8, text=field, anchor='w', font=tkinter.font.Font(family="Segoe UI", size=10), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.bg_color).grid(row=i, padx=2, pady=2,  sticky='e')
    global combo1, e2, e3, e4
    app_lib.find_names(app)
    combo1 = tk.ttk.Combobox(root, values=tuple(app_lib.find_names(app)), height=17, width=32)
    combo1.grid(row=0, column=1, padx=2, pady=2, sticky='e')
    e2 = tk.ttk.Entry(root, font=tkinter.font.Font(family="Segoe UI", size=10), width=30)
    e2.grid(row=1, column=1, padx=2, pady=2, sticky='e')
    e3 = tk.ttk.Entry(root, font=tkinter.font.Font(family="Segoe UI", size=10), width=30)
    e3.grid(row=2, column=1, padx=2, pady=2, sticky='e')
    e4 = tk.ttk.Entry(root, font=tkinter.font.Font(family="Segoe UI", size=10), width=30)
    e4.grid(row=3, column=1, padx=2, pady=2, sticky='e')
    if app.settings.month == 'all' or app.settings.month == date.today().strftime("%m"):
        e4.insert(0, date.today().strftime("%Y.%m.%d"))
    else:
        e4.insert(0, f"{app.settings.jear}.{app.settings.month}.01")
    # Buttons ##############################################################################################
    tk.ttk.Button(root, text='Add',width=7,command=(lambda : safe_to_dataarray(app))).grid(row=1, column=5, padx=12, pady=2)
    tk.ttk.Button(root, text='Delete',width=7, command=(lambda : delet_from_dataarray(app))).grid(row=2, column=5, padx=12, pady=2)
    tk.ttk.Button(root, text='Clear',width=7, command=(lambda : clear(app))).grid(row=3, column=5, padx=12, pady=2)

def button_ (root : tk.Tk, app : app_lib.app_state):
    tk.ttk.Button(root, text='Save', width=5, command=(lambda : save(app))).pack(side='right', anchor='s', padx=10)
    tk.ttk.Button(root, text='Create PDF', command=(lambda : save_pdf_lib.export(app))).pack(side='right', anchor='s', fill='x')
