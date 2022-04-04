import tkinter as tk
import tkinter.font as font
from PIL import ImageTk, Image

def center_window(root : tk.Tk, w, h):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = int((ws/2) - (w/2))    
    y = int((hs/2) - (h/2))
    root.geometry(f'{w}x{h}+{x}+{y}')

def welcome_window() -> None:
    welcome_window = tk.Tk()
    welcome_window.geometry('450x170')
    welcome_window.overrideredirect(1)
    center_window(welcome_window, 450, 170)
    tk.Label(welcome_window, text='Welcome to BondMarket', font=font.Font(family="Segoe UI", size=25)).pack(side='top', pady=5, padx=30)
    try:
        logo = Image.open("BondMarket\Icons\BondMarket_Logo_dark.png")
    except:
        logo = Image.open("Icons\BondMarket_Logo_dark.png")
    logo = logo.resize((256, 50))
    logo = ImageTk.PhotoImage(logo)
    tk.Label(welcome_window, image=logo).pack(side='top', pady=5)
    tk.Button(welcome_window, text='Start', font=font.Font(family="Segoe UI"), relief='flat', command=welcome_window.destroy).pack(side='top', anchor='se', pady=5, padx=10)
    welcome_window.title('')
    welcome_window.mainloop()