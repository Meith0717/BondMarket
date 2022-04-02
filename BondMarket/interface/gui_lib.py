code_autor = "Thierry Meiers"
code_copyright = "Copyright © 2022 Thierry Meiers" 
code_version = "4.0"

import tkinter as tk
import clipboard 
import webbrowser
import Lib.app_lib as app_lib
import Lib.save_backup_lib as save_backup_lib
import Lib.save_pdf_lib as save_pdf_lib 
import Calculations.debts_lib as debts_lib
from Lib.save_data_lib import save_data_in_file, save_settings_in_file, read_data_from_file, read_settings_from_file, read_from_pkl
from Theme.theme_lib import LIGHT, DARK
from datetime import date
from tkinter.font import Font
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

    p1.config(text=f"{app.settings.data_path}")

    if app.safe_state_data is True:
        change.config(state='enabled')
        backup.config(state='enabled')
    else:
        change.config(state='disabled')
        backup.config(state='disabled')
    
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

def safe_to_dataarray (app : app_lib.app_state):
    if combo1.get() == ''  or e3.get() == '':
        return
    if len(app_lib.find_names(app))+1 > 10 and combo1.get() not in app_lib.find_names(app):
        messagebox.showwarning('Warning', 'Name Error: Only 10 persons are allowed')
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
            messagebox.showerror('Error', message='Amount Error: Please enter a Number')

def delet_from_dataarray (app : app_lib.app_state):
    app_lib.pop_from_data_array(app, combo1.get(), e2.get(), e3.get(), e4.get())
    clear(app)
    update_screen(app)

def ask_to_save(app : app_lib):
    if app.safe_state_data: 
        pass
    else:
        if messagebox.askyesno('Warning!', 'Do you want to save?'):
            save_data_in_file(app)
    save_settings_in_file(app)

def exit (root : tk.Tk, app : app_lib.app_state):
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

def get_data_path (main_root : tk.Tk, app : app_lib.app_state):
    if app.safe_state_data is False:
        return
    prew_path = app.settings.data_path
    app.settings.data_path = filedialog.askopenfilename(filetypes=[('PKL', '.pkl')])
    if app.settings.data_path == '' or prew_path == app.settings.data_path:
        app.settings.data_path = prew_path
    else:
        save_settings_in_file(app)
        read_data_from_file(app)
        update_screen(app)
        
def center_window(root : tk.Tk, w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)    
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def table_ (root, app : app_lib.app_state):
    global tree
    tree = tk.ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings', selectmode='browse', height=200)
    vsb = tk.ttk.Scrollbar(root, orient='vertical', command=tree.yview)
    headline : list = ['Person', 'Amount', 'Coment', 'Date']
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

def settings_ (main_root : tk.Tk, root : tk.Tk, app : app_lib.app_state) :
    global p1, change, backup

    def restore_backup(app : app_lib.app_state):
        if messagebox.askyesno('Warning', 'Are you sure you want to recover the data? Data can be lost'):
            path = filedialog.askopenfilename(filetypes=[('PKL', '.pkl')])
            if path != '':
                app.data_array = read_from_pkl(path)
                update_screen(app)

    def save_appearance (app : app_lib.app_state):
        print(str(app.settings.appearance))
        if sel_apperance.get() in str(app.settings.appearance):
            return
        if sel_apperance.get() == 'LIGHT':
            app.settings.appearance = LIGHT
        if sel_apperance.get() == 'DARK':
            app.settings.appearance = DARK
        save_settings_in_file(app)
        if messagebox.askyesno('Warning!', 'Do you want to restart the application for the changes to take effect!'):
            exit(main_root, app)

    def save_filter (app : app_lib.app_state):
        if jear.get() == '' or month.get() == '':
            pass
        else:
            app.settings.jear = jear.get()
            app.settings.month = month.get()
            update_screen(app)

    def clear (app : app_lib.app_state):
        if messagebox.askyesno(title='Warning:', message='Are you sure you want to delete everything?'):
            app.data_array = []
            update_screen(app)

    tk.Label(root, text='Appearance:', font=Font(family="Segoe UI", size=12, weight='bold'), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).grid(row=1, sticky='w', pady=5, padx=1)
    
    sel_apperance = tk.StringVar()
    sel_apperance.set(app.settings.appearance.name)
    tk.ttk.Radiobutton(root, text='white', value='LIGHT', variable=sel_apperance).grid(row=2, sticky='w', pady=5, padx=1)
    tk.ttk.Radiobutton(root, text='Dark', value='DARK', variable=sel_apperance).grid(row=3, sticky='w', pady=5, padx=1)

    tk.Label(root, text='Data Table:', font=Font(family="Segoe UI", size=12, weight='bold'), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).grid(row=4, sticky='w', pady=5, padx=1)
    tk.Label(root, text='Month:', fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).grid(row=5, sticky='w', pady=5, padx=1)
    month = tk.ttk.Combobox(root, values=tuple(x for x in ['all', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11' ,'12']))
    month.grid(row=5,column=2,sticky='w', pady=5, padx=1)
    month.insert(0, date.today().strftime("%m"))
    tk.Label(root, text='Jear:', fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).grid(row=6, sticky='w', pady=5, padx=1)
    jear = tk.ttk.Combobox(root, values=tuple(x for x in range(2000, 2100)))
    jear.grid(row=6,column=2,sticky='w', pady=5, padx=1)
    jear.insert(0, app.settings.jear)

    tk.Label(root, text='Data Path:', font=Font(family="Segoe UI", size=12, weight='bold'), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).grid(row=7, sticky='w', pady=5, padx=1)
    tk.Label(root, text='Save to enable Button', font=Font(family="Segoe UI", size=8), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).grid(row=8,column=2, sticky='w', pady=5, padx=1)

    p1 = tk.Label(root, text=app.settings.data_path.replace('/', "\\"), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color)
    tk.Label(root, text=f"Default: ~\Documents", fg=app.settings.appearance.fg_color, bg=app.settings.appearance.lb_color).place(x=1, y=300)
    p1.place(x=1, y=275)

    tk.ttk.Button(root, text='Apply', command=(lambda : save_appearance(app))).grid(row=1, column=10, padx=5, pady=5)
    tk.ttk.Button(root, text='Clear Data', command=(lambda : clear(app))).grid(row=4, column=10, padx=5, pady=5)
    tk.ttk.Button(root, text='Apply', command=(lambda : save_filter(app))).grid(row=5, column=10, padx=5, pady=5)
    tk.ttk.Button(root, text='Restore', command=(lambda : restore_backup(app))).grid(row=8, column=10, padx=5, pady=5)
    backup = tk.ttk.Button(root, text='Create Backup', command=(lambda : save_backup_lib.create_backup(app)))
    backup.grid(row=8, column=0, padx=5, pady=5)
    change = tk.ttk.Button(root, text='Open File', command=(lambda : get_data_path(main_root, app)))
    change.grid(row=7, column=10, padx=5, pady=5)
    change.config(state='disabled')
    backup.config(state='disabled')

def info_ (root, app : app_lib) :
   
    def open_link (link : str):
        if messagebox.askokcancel(title='Info',message=f"You will be redirected to {link}, do you want to continue?"):
            webbrowser.open(link, new=0, autoraise=True)

    tk.Label(root, text='Shortcuts:', font=Font(family="Segoe UI", size=12, weight='bold'), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=0, column=0, sticky='w')

    tk.Label(root, text='Save Entry:', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=1, column=0, sticky='w')
    tk.Label(root, text='ENTER', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=1, column=1, sticky='w')

    tk.Label(root, text='Deleete Entry:', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=2, column=0, sticky='w')
    tk.Label(root, text='DELETE', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=2, column=1, sticky='w')

    tk.Label(root, text='Exit:', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=3, column=0, sticky='w')
    tk.Label(root, text='ESCAPE', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=3, column=1, sticky='w')

    tk.Label(root, text='Save File:', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=4, column=0, sticky='w')
    tk.Label(root, text='Control-s', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=4, column=1, sticky='w')

    tk.Label(root, text='Open File:', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=5, column=0, sticky='w')
    tk.Label(root, text='Control-o', background=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=5, column=1, sticky='w')

    tk.Label(root, text='Info:', font=Font(family="Segoe UI", size=12, weight='bold'), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=6, column=0, sticky='w')
    text = tk.Text(root, bg=app.settings.appearance.lb_color, fg=app.settings.appearance.fg_color, width=30, height=8, font=Font(family="Segoe UI", size=9), relief='flat')
    text.grid(row=7)
    text.insert('insert', 'If you have any problems or\nsuggestions for improvement,\nyou are welcome to send me an\nemail. Suggestions for.\nimprovements to the code are\nalso welcome, you can find it on\nGithub.')
    text.config(state='disabled')
    tk.Button(root, text='Donate', relief='flat', font=Font(underline=True, size=8),fg='#0082FF', bg=app.settings.appearance.lb_color, activebackground=app.settings.appearance.lb_color, command=(lambda : open_link('https://www.paypal.com/donate/?hosted_button_id=47BGH5AWNSV88'))).grid(row=13, column=0, sticky='w')
    tk.Button(root, text='Github', relief='flat', font=Font(underline=True, size=8),fg='#0082FF', bg=app.settings.appearance.lb_color, activebackground=app.settings.appearance.lb_color, command=(lambda : open_link('https://github.com/Meith0717/BondMarket.git'))).grid(row=14, column=0, sticky='w')
    tk.Button(root, text='Discord', relief='flat', font=Font(underline=True, size=8),fg='#0082FF', bg=app.settings.appearance.lb_color, activebackground=app.settings.appearance.lb_color, command=(lambda : open_link('https://discordapp.com/users/773830054726860811/'))).grid(row=15, column=0, sticky='w')
    #tk.Button(root, text='meith0717@gmail.com', relief='flat',font=Font(underline=True, size=8), fg='#0082FF', bg=app.settings.appearance.lb_color, activebackground=app.settings.appearance.lb_color, command=(lambda : messagebox.showinfo(title='Info',message='Mail-Adress copy to clipboard', options=clipboard.copy('meith0717@gmail.com')))).grid(row=15, column=0, sticky='w')

def tools_ (root : tk.Tk, app : app_lib.app_state):
    global s0, s1, s2, s3, s4, s5, s6, s7, s8, s9
    global d0, d1, d2, d3, d4, d5, d6, d7, d8, d9
    l : list = debts_lib.calc_expand(app)
    s : list = debts_lib.get_transfere_str(app)
    s0 = tk.Label(root, text= f"{l[0].name}{l[0].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    s0.grid(row=1, column=0, sticky='w', pady=0, padx=30)
    s1 = tk.Label(root, text= f"{l[1].name}{l[1].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    s1.grid(row=2, column=0, sticky='w', pady=0, padx=30)
    s2 = tk.Label(root, text= f"{l[2].name}{l[2].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    s2.grid(row=3, column=0, sticky='w', pady=0, padx=30)
    s3 = tk.Label(root, text= f"{l[3].name}{l[3].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    s3.grid(row=4, column=0, sticky='w', pady=0, padx=30)
    s4 = tk.Label(root, text= f"{l[4].name}{l[4].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    s4.grid(row=5, column=0, sticky='w', pady=0, padx=30)
    s5 = tk.Label(root, text= f"{l[5].name}{l[5].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    s5.grid(row=6, column=0, sticky='w', pady=0, padx=30)
    s6 = tk.Label(root, text= f"{l[6].name}{l[6].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    s6.grid(row=7, column=0, sticky='w', pady=0, padx=30)
    s7 = tk.Label(root, text= f"{l[7].name}{l[7].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    s7.grid(row=8, column=0, sticky='w', pady=0, padx=30)
    s8 = tk.Label(root, text= f"{l[8].name}{l[8].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    s8.grid(row=9, column=0, sticky='w', pady=0, padx=30)
    s9 = tk.Label(root, text= f"{l[9].name}{l[9].amount}" , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    s9.grid(row=10, column=0, sticky='w', pady=0, padx=30)
    d0 = tk.Label(root, text=s[0], bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    d0.grid(row=12, column=0, sticky='w', pady=0, padx=30)
    d1 = tk.Label(root, text=s[1], bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    d1.grid(row=13, column=0, sticky='w', pady=0, padx=30)
    d2 = tk.Label(root, text=s[2] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    d2.grid(row=14, column=0, sticky='w', pady=0, padx=30)
    d3 = tk.Label(root, text=s[3] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    d3.grid(row=15, column=0, sticky='w', pady=0, padx=30)
    d4 = tk.Label(root, text=s[4], bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    d4.grid(row=16, column=0, sticky='w', pady=0, padx=30)
    d5 = tk.Label(root, text=s[5] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    d5.grid(row=17, column=0, sticky='w', pady=0, padx=30)
    d6 = tk.Label(root, text=s[6] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    d6.grid(row=18, column=0, sticky='w', pady=0, padx=30)
    d7 = tk.Label(root, text=s[7] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    d7.grid(row=19, column=0, sticky='w', pady=0, padx=30)
    d8 = tk.Label(root, text=s[8] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    d8.grid(row=20, column=0, sticky='w', pady=0, padx=30)
    d9 = tk.Label(root, text=s[9] , bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color)
    d9.grid(row=11, column=0, sticky='w', pady=0, padx=30)
    tk.Label(root, text='Total expenses:', font=Font(family="Segoe UI", size=12, weight='bold'), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=0, column=0, sticky='w', pady=1, padx=2)
    tk.Label(root, text='Total debt:', font=Font(family="Segoe UI", size=12, weight='bold'), bg=app.settings.appearance.bg_color, fg=app.settings.appearance.fg_color).grid(row=11, column=0, sticky='w', pady=1, padx=2)

def entry_ (root : tk.Tk, app : app_lib.app_state):
    # cavas ##############################################################################################
    fields : list = ['Person:', 'Amount:', 'Coment:', 'Date:']
    for i, field in enumerate(fields):
        tk.Label(root, width=8, text=field, anchor='w', font=Font(family="Segoe UI", size=10), fg=app.settings.appearance.fg_color, bg=app.settings.appearance.bg_color).grid(row=i, padx=2, pady=2,  sticky='e')
    global combo1, e2, e3, e4
    app_lib.find_names(app)
    combo1 = tk.ttk.Combobox(root, values=tuple(app_lib.find_names(app)), height=17, width=32)
    combo1.grid(row=0, column=1, padx=2, pady=2, sticky='e')
    e2 = tk.ttk.Entry(root, font=Font(family="Segoe UI", size=10), width=30)
    e2.grid(row=1, column=1, padx=2, pady=2, sticky='e')
    e3 = tk.ttk.Entry(root, font=Font(family="Segoe UI", size=10), width=30)
    e3.grid(row=2, column=1, padx=2, pady=2, sticky='e')
    e4 = tk.ttk.Entry(root, font=Font(family="Segoe UI", size=10), width=30)
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
