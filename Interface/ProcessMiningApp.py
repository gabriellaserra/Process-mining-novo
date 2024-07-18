from tkinter import *
import tkinter as tk
import customtkinter as s

from Janela.Janela import *

raiz = s.CTk(className='Process Mining GUI')
raiz.title('Process Mining GUI')
s.set_appearance_mode("Dark")
s.set_default_color_theme("dark-blue")
raiz.geometry('960x540')
Janela(raiz)
raiz.mainloop()
# teste