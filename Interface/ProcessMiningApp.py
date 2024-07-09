from tkinter import *
import tkinter as tk
import customtkinter as s

from Janela.Janela import *

raiz = s.CTk(className='Proces Mining GUI')
raiz.title('CABETUDA MINNING ltda.')
s.set_appearance_mode("system")
s.set_default_color_theme("dark-blue")
raiz.geometry('960x540')
Janela(raiz)
raiz.mainloop()


###### janela de variantes 

# import pandas as pd
# import pm4py


# dataframe = pd.read_excel("C:\\Users\\meduarda\\Documents\\grupo-2\\Notebooks\\Case Navios Tanque\\BaseNTFinalDeles.xlsx")
# dataframe = pm4py.format_dataframe(dataframe, case_id='ID', activity_key= 'Ocorrência', timestamp_key='Início')
# for variant, subdf in pm4py.split_by_process_variant(dataframe):
#     print(variant)
#     print(subdf)