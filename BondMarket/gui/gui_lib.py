__author__ = code_autor = "Thierry Meiers"
__copyright__ = code_copyright = "Copyright © 2022 Thierry Meiers"
__license__ = "Apache License 2.0"
__version__ = code_version = "3.8.1"

import tkinter as tk
import os
import clipboard 
import webbrowser
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
from tkinter.font import Font
from tkinter import messagebox
from app import app_lib
from data import save_data_lib, create_backup_file, export_txt_file
from datetime import date
from debts import debts_lib

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

    p1.config(text=f"{app.settings.data_dir_path}")

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
    if len(app_lib.find_names(app))+1 > 10:
        messagebox.showwarning('Warning', 'Name Error: Only 10 persons are allowed')
    else:
        if combo1.get() == ''  or e3.get() == '':
            pass
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

def exit (root : tk.Tk, app : app_lib.app_state):
    save_data_lib.save_data_in_file(app)
    save_data_lib.save_settings_in_file(app)
    root.destroy()

def OnDoubleClick(app: app_lib.app_state, event):
    global e5
    clear(app)
    curItem = tree.item(tree.focus())
    combo1.insert(0, curItem['values'][0])
    e2.insert(0, curItem['values'][1])
    e3.insert(0, curItem['values'][2])
    e4.delete(0, 100)
    e4.insert(0, curItem['values'][3])

def save (app : app_lib.app_state):
    app.safe_state_data = True
    save_data_lib.save_data_in_file(app)
    save_data_lib.save_settings_in_file(app)
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

def draw_tree (root, app : app_lib.app_state):
    global tree
    tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings', selectmode='browse', height=200)
    vsb = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
    headline : list = ['Person', 'Amount', 'Coment', 'Date']
    tree.tag_configure('odd', background='#F4F6F7')
    tree.tag_configure('even', background='#F0F3F4')

    tree.column("# 1", width=12, anchor='w')
    tree.heading("# 1", text=headline[0], anchor='w')
    tree.column("# 2", width=12, anchor='w')
    tree.heading("# 2", text=headline[1], anchor='w')
    tree.column("# 3", width=86, anchor='w')
    tree.heading("# 3", text=headline[2], anchor='w')
    tree.column("# 4", width=10, anchor='w')
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

def settings (root : tk.Tk, app : app_lib.app_state) :
    global p1, change, backup

    def get_data_dir (app : app_lib.app_state):
        prew_dir = app.settings.data_dir_path
        app.settings.data_dir_path = filedialog.askdirectory()
        if app.settings.data_dir_path == '':
            app.settings.data_dir_path = prew_dir
        elif prew_dir == 'na':
            pass
        else:
            save_data_lib.check_if_dir_exist(app.settings.data_dir_path)
            try:
                os.rename(f'{prew_dir}\BondMarket\data.pkl' ,f'{app.settings.data_dir_path}\BondMarket\data.pkl')
                save(app)
            except FileExistsError:
                save_data_lib.save_settings_in_file(app)
                win.destroy()
                os.remove(f'{prew_dir}\BondMarket\data.pkl')
                window(750, 550, True)


    def save_appearance (app : app_lib.app_state):
        if app.settings.appearance != sel_apperance.get():
            app.settings.appearance = sel_apperance.get()
            save_data_lib.save_settings_in_file(app)
            save_data_lib.save_data_in_file(app)
            winx = win.winfo_width()
            winy = win.winfo_height()
            win.destroy()
            window(winx, winy, True)

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

    tk.Label(root, text='Appearance:', font=Font(family="Segoe UI", size=12, weight='bold'), fg=text_color, bg=lab_color).grid(row=1, sticky='w', pady=5)
    
    sel_apperance = tk.StringVar()
    sel_apperance.set(app.settings.appearance)
    ttk.Radiobutton(root, text='white', value='white', variable=sel_apperance).grid(row=2, sticky='w', pady=5)
    ttk.Radiobutton(root, text='Dark', value='Dark', variable=sel_apperance).grid(row=3, sticky='w', pady=5)

    tk.Label(root, text='Data Table:', font=Font(family="Segoe UI", size=12, weight='bold'), fg=text_color, bg=lab_color).grid(row=4, sticky='w', pady=5)
    tk.Label(root, text='Month:', fg=text_color, bg=lab_color).grid(row=5, sticky='w', pady=5)
    month = ttk.Combobox(root, values=tuple(x for x in ['all', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11' ,'12']))
    month.grid(row=5,column=2,sticky='w', pady=5)
    month.insert(0, date.today().strftime("%m"))
    tk.Label(root, text='Jear:', fg=text_color, bg=lab_color).grid(row=6, sticky='w', pady=5)
    jear = ttk.Combobox(root, values=tuple(x for x in range(2000, 2100)))
    jear.grid(row=6,column=2,sticky='w', pady=5)
    jear.insert(0, app.settings.jear)

    tk.Label(root, text='Data Path:', font=Font(family="Segoe UI", size=12, weight='bold'), fg=text_color, bg=lab_color).grid(row=7, sticky='w', pady=5)
    p1 = tk.Label(root, text=f"{app.settings.data_dir_path}", fg=text_color, bg=lab_color)
    tk.Label(root, text=f"Default: ~/Documents", fg=text_color, bg=lab_color).place(x=1, y=290)
    p1.place(x=1, y=270)

    ttk.Button(root, text='Apply', command=(lambda : save_appearance(app))).grid(row=1, column=10, padx=5, pady=5)
    ttk.Button(root, text='Clear Data', command=(lambda : clear(app))).grid(row=4, column=10, padx=5, pady=5)
    ttk.Button(root, text='Apply', command=(lambda : save_filter(app))).grid(row=5, column=10, padx=5, pady=5)
    backup = ttk.Button(root, text='Create Backup', command=(lambda : create_backup_file.create_backup(app)))
    backup.grid(row=8, column=0, padx=5, pady=5)
    change = ttk.Button(root, text='Change', command=(lambda : get_data_dir(app)))
    change.grid(row=9, column=10, padx=5, pady=5)
    change.config(state='disabled')
    backup.config(state='disabled')

def info (root) :
    def redirected_paypal ():
        if messagebox.askokcancel(title='Info',message='You will be redirected to paypal.com, do you want to continue?'):
            webbrowser.open('https://www.paypal.com/donate/?hosted_button_id=47BGH5AWNSV88', new=0, autoraise=True)
 
    tk.Label(root, text='Not yet implemented', fg='red', bg=lab_color).place(x=2, y=25)
    tk.Button(root, text='Donate', relief='flat', fg=text_color, bg=lab_color, activebackground=lab_color, command=redirected_paypal).pack(side='right', anchor='se', padx=3, pady=3)
    tk.Button(root, text='meith0717@gmail.com', relief='flat', fg=text_color, bg=lab_color, activebackground=lab_color, command=(lambda : messagebox.showinfo(title='Info',message='Mail-Adress copy to clipboard', options=clipboard.copy('meith0717@gmail.com')))).pack(side='left', anchor='sw', padx=3, pady=3)

def tools (root : tk.Tk, app : app_lib.app_state):
    global s0, s1, s2, s3, s4, s5, s6, s7, s8, s9
    global d0, d1, d2, d3, d4, d5, d6, d7, d8, d9
    l : list = debts_lib.calc_expand(app)
    s : list = debts_lib.get_transfere_str(app)
    s0 = tk.Label(root, text= f"{l[0].name}{l[0].amount}" , bg=bg_color, fg=text_color)
    s0.grid(row=1, column=0, sticky='w', pady=0, padx=2)
    s1 = tk.Label(root, text= f"{l[1].name}{l[1].amount}" , bg=bg_color, fg=text_color)
    s1.grid(row=2, column=0, sticky='w', pady=0, padx=2)
    s2 = tk.Label(root, text= f"{l[2].name}{l[2].amount}" , bg=bg_color, fg=text_color)
    s2.grid(row=3, column=0, sticky='w', pady=0, padx=2)
    s3 = tk.Label(root, text= f"{l[3].name}{l[3].amount}" , bg=bg_color, fg=text_color)
    s3.grid(row=4, column=0, sticky='w', pady=0, padx=2)
    s4 = tk.Label(root, text= f"{l[4].name}{l[4].amount}" , bg=bg_color, fg=text_color)
    s4.grid(row=5, column=0, sticky='w', pady=0, padx=2)
    s5 = tk.Label(root, text= f"{l[5].name}{l[5].amount}" , bg=bg_color, fg=text_color)
    s5.grid(row=6, column=0, sticky='w', pady=0, padx=2)
    s6 = tk.Label(root, text= f"{l[6].name}{l[6].amount}" , bg=bg_color, fg=text_color)
    s6.grid(row=7, column=0, sticky='w', pady=0, padx=2)
    s7 = tk.Label(root, text= f"{l[7].name}{l[7].amount}" , bg=bg_color, fg=text_color)
    s7.grid(row=8, column=0, sticky='w', pady=0, padx=2)
    s8 = tk.Label(root, text= f"{l[8].name}{l[8].amount}" , bg=bg_color, fg=text_color)
    s8.grid(row=9, column=0, sticky='w', pady=0, padx=2)
    s9 = tk.Label(root, text= f"{l[9].name}{l[9].amount}" , bg=bg_color, fg=text_color)
    s9.grid(row=10, column=0, sticky='w', pady=0, padx=2)
    d0 = tk.Label(root, text=s[0], bg=bg_color, fg=text_color)
    d0.grid(row=12, column=0, sticky='w', pady=0, padx=2)
    d1 = tk.Label(root, text=s[1], bg=bg_color, fg=text_color)
    d1.grid(row=13, column=0, sticky='w', pady=0, padx=2)
    d2 = tk.Label(root, text=s[2] , bg=bg_color, fg=text_color)
    d2.grid(row=14, column=0, sticky='w', pady=0, padx=2)
    d3 = tk.Label(root, text=s[3] , bg=bg_color, fg=text_color)
    d3.grid(row=15, column=0, sticky='w', pady=0, padx=2)
    d4 = tk.Label(root, text=s[4], bg=bg_color, fg=text_color)
    d4.grid(row=16, column=0, sticky='w', pady=0, padx=2)
    d5 = tk.Label(root, text=s[5] , bg=bg_color, fg=text_color)
    d5.grid(row=17, column=0, sticky='w', pady=0, padx=2)
    d6 = tk.Label(root, text=s[6] , bg=bg_color, fg=text_color)
    d6.grid(row=18, column=0, sticky='w', pady=0, padx=2)
    d7 = tk.Label(root, text=s[7] , bg=bg_color, fg=text_color)
    d7.grid(row=19, column=0, sticky='w', pady=0, padx=2)
    d8 = tk.Label(root, text=s[8] , bg=bg_color, fg=text_color)
    d8.grid(row=20, column=0, sticky='w', pady=0, padx=2)
    d9 = tk.Label(root, text=s[9] , bg=bg_color, fg=text_color)
    d9.grid(row=11, column=0, sticky='w', pady=0, padx=2)
    tk.Label(root, text='Total expenses:', font=Font(family="Segoe UI", size=12, weight='bold'), bg=bg_color, fg=text_color).grid(row=0, column=0, sticky='w', pady=0, padx=2)
    tk.Label(root, text='Total debt:', font=Font(family="Segoe UI", size=12, weight='bold'), bg=bg_color, fg=text_color).grid(row=11, column=0, sticky='w', pady=0, padx=2)
    ttk.Button(root, text='Export Text File', command=(lambda : export_txt_file.export(app))).grid(row=0, column=10, sticky='e')

def set_fullscreen(app : app_lib.app_state): 
    if app.settings.fullscreen:
        app.settings.fullscreen = False
    else:
        app.settings.fullscreen = True
    win.attributes('-fullscreen', app.settings.fullscreen)

def center_window(root : tk.Tk, w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)    
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def window (winx : int, winy : int, restart : bool):

    global bg_color, text_color, lab_color, win
    app = app_lib.app_state([], {}, True)
    save_data_lib.read_settings_from_file(app)
    save_data_lib.read_data_from_file(app)
    win = ThemedTk()
    center_window(win, winx, winy)
    if app.settings.appearance == 'white':
        bg_color = None
        text_color = 'black'
        lab_color = '#f0f0f0'
    elif app.settings.appearance == 'Dark':
        win.config(theme='black')
        bg_color = '#424242'
        text_color = 'white'
        lab_color = '#424242'
    
    # Window settings ##############################################################################################
    win.title('BondMarket')
    win.wm_attributes('-toolwindow', 'True')
    win.config(bg=bg_color)
    win.attributes('-fullscreen', app.settings.fullscreen)
    win.geometry(f'{winx}x{winy}')
    win.minsize(750, 550)
    # Frames ##############################################################################################
    global data_frame
    data_frame = tk.LabelFrame(win, text="Data Table", fg=text_color, bg=bg_color)
    entry_frame = tk.LabelFrame(win, text="Enty Data", fg=text_color, bg=bg_color)
    more_frame = tk.LabelFrame(win, text="Menue", fg=text_color, bg=bg_color)
    # Descriptions ##############################################################################################
    tk.Label(win, text='Python 3.10.1     %s    Version %s' %(code_copyright,code_version), font=Font(family="Segoe UI", size=8), fg=text_color, bg=bg_color, width=5000).pack(side='bottom', fill='x')
    # Table ##############################################################################################
    draw_tree(data_frame, app)
    # Tabs ###############################################################################################
    tab = ttk.Notebook(more_frame)
    tab1 = ttk.Frame(tab)
    tab2 = ttk.Frame(tab) 
    tab3 = ttk.Frame(tab) 
    tab.add(tab1, text ='     Tools     ')
    tools(tab1, app)
    tab.add(tab2, text ='    Settings   ')
    settings(tab2, app)
    tab.add(tab3, text ='   Help/Info   ')
    info(tab3)
    tab.pack(side='left', fill='both', padx=5, pady=5)
    # cavas ##############################################################################################
    fields : list = ['Person:', 'Amount:', 'Coment:', 'Date:']
    for i, field in enumerate(fields):
        tk.Label(entry_frame, width=8, text=field, anchor='w', font=Font(family="Segoe UI", size=10), fg=text_color, bg=bg_color).grid(row=i, padx=2, pady=2,  sticky='e')
    global combo1, e2, e3, e4
    app_lib.find_names(app)
    combo1 = ttk.Combobox(entry_frame, values=tuple(app_lib.find_names(app)), width=25)
    combo1.grid(row=0, column=1, padx=2, pady=2, sticky='e')
    e2 = ttk.Entry(entry_frame, font=Font(family="Segoe UI", size=10), width=25)
    e2.grid(row=1, column=1, padx=2, pady=2, sticky='e')
    e3 = ttk.Entry(entry_frame, font=Font(family="Segoe UI", size=10), width=25)
    e3.grid(row=2, column=1, padx=2, pady=2, sticky='e')
    e4 = ttk.Entry(entry_frame, font=Font(family="Segoe UI", size=10), width=25)
    e4.grid(row=3, column=1, padx=2, pady=2, sticky='e')
    if app.settings.month == 'all' or app.settings.month == date.today().strftime("%m"):
        e4.insert(0, date.today().strftime("%Y.%m.%d"))
    else:
        e4.insert(0, f"{app.settings.jear}.{app.settings.month}.01")
    # Buttons ##############################################################################################
    ttk.Button(entry_frame, text='Add',width=5,command=(lambda : safe_to_dataarray(app))).grid(row=1, column=5, padx=10, pady=2)
    ttk.Button(entry_frame, text='Delet',width=5, command=(lambda : delet_from_dataarray(app))).grid(row=2, column=5, padx=10, pady=2)
    ttk.Button(entry_frame, text='Clear',width=5, command=(lambda : clear(app))).grid(row=3, column=5, padx=10, pady=2)
    ttk.Button(entry_frame, text='Save', width=5, command=(lambda : save(app))).grid(row=2, column=6, padx=10, pady=2)
    ttk.Button(entry_frame, text='Exit', width=5, command=(lambda : exit(win, app))).grid(row=3, column=6, padx=10, pady=2)
    # Keyboard ###############################################################################################
    win.bind('<Control-s>', lambda event: save(app))
    win.bind('<F11>', lambda event: set_fullscreen(app))
    win.bind('<Escape>', lambda event: exit(win, app))
    win.bind('<Return>', lambda event: safe_to_dataarray(app))
    win.bind('<t>', lambda event: debts_lib.get_transfere_str(app))
    # Place some Frames ######################################################################################
    more_frame.pack(side='right', anchor='e', padx=1, pady=1, fill='both')
    entry_frame.pack(side='bottom', anchor='sw', padx=1, pady=1, fill='both')
    data_frame.pack(side='top', anchor='nw', padx=1, pady=1, fill='both')
    win.mainloop()
