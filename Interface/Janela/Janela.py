from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import customtkinter as s
import os
from PIL import Image, ImageTk
import pm4py
from pm4py.objects.petri_net.importer import importer as pmnl_importer
import pandas as pd

class Janela:
    def __init__(self, raiz):
        #Frame da seleção de arquivos e gráficos:
        self.raiz = raiz
        self.frameTOP = s.CTkFrame(raiz)
        self.frameTOP.pack(side='top',fill=tk.BOTH)

        #Frame dos paths lateral:
        self.frame_lateral = s.CTkFrame(raiz)
        self.frame_lateral.pack(side = 'right',  fill='y')

        self.frame_escala = s.CTkFrame(self.frame_lateral)
        self.frame_escala.pack(fill="both", expand=True)

        #Frame do gráfico:
        self.frame_grafico = s.CTkFrame(raiz)
        self.frame_grafico.pack(expand=True, fill='both')

        #Frame inferior da análise de conformidade:
        self.frameConform = s.CTkFrame(raiz)
        self.frameConform.pack(side='right', fill='both')

        #Imagens dos botões:
        self.arq = s.CTkImage(light_image=Image.open('Interface\\Janela\\iconArq.png'), dark_image=Image.open('Interface\\Janela\\iconArq.png'), size=(80,80))
        self.arqPerform = s.CTkImage(light_image=Image.open('Interface\\Janela\\iconPerformance.png'), dark_image=Image.open('Interface\\Janela\\iconPerformanceDark.png'), size=(80,80))
        self.arqFreq = s.CTkImage(light_image=Image.open('Interface\\Janela\\iconFreq.png'), dark_image=Image.open('Interface\\Janela\\iconFreqDark.png'), size=(80,80))
        self.arqPetri = s.CTkImage(light_image=Image.open('Interface\\Janela\\iconPetri.png'), dark_image=Image.open('Interface\\Janela\\iconPetriDark.png'), size=(80,80))
        self.arqNot = s.CTkImage(light_image=Image.open('Interface\\Janela\\mode.png'), dark_image=Image.open('Interface\\Janela\\modeDark.png'), size=(20,20))

        #Labels:
        self.label_arquivo = s.CTkLabel(self.frameTOP, text="Nenhum arquivo selecionado")
        self.label_arquivo.pack(side='bottom')

        self.lable_auxImagem= s.CTkLabel(self.frameTOP, text="Nenhma Imagem Gerada")
        self.lable_auxImagem.pack(side='bottom')

        self.label_escalaA = s.CTkLabel(self.frame_escala, text="Activities")
        self.label_escalaA.place(relx=0.3, rely=0.1, anchor= CENTER)

        self.label_escalaP = s.CTkLabel(self.frame_escala, text="Paths")
        self.label_escalaP.place(relx=0.7, rely=0.1, anchor= CENTER)

        self.lableConform = s.CTkLabel(self.frameConform, text=None, font=('Arial', 20))
        self.lableConform.pack()

        self.image_label = s.CTkLabel(self.frame_grafico, text=None)
        self.image_label.pack()

        #Sliders:
        self.slider_Activities = s.CTkSlider(self.frame_escala, from_=0, to=1, orientation='vertical')
        self.slider_Activities.set(100)
        self.slider_Activities.place(relx=0.3, rely=0.5, anchor= CENTER)

        self.slider_Paths = s.CTkSlider(self.frame_escala,from_=0.9, to=0, orientation='vertical')
        self.slider_Paths.set(0)
        self.slider_Paths.place(relx=0.7, rely=0.5, anchor=CENTER)

        #Botões: 
        self.botaoArquivo = s.CTkButton(self.frameTOP, text= "Seleção de arquivos" , image=self.arq, hover_color=None, fg_color="black", command= lambda: self.escolhe_arquivo()) #
        self.botaoArquivo.pack(side='left')

        self.botaoConform = s.CTkButton(self.frame_lateral, text='Análise de Conformidade') #, command=lambda: analize_conformidade()
        self.botaoConform.pack()

        self.botaoFrequencia = s.CTkButton(self.frameTOP, text="Gráfico de Frequência", image=self.arqFreq, hover_color=None, fg_color="transparent") #, command=lambda: cria_grafo_dfg(log)
        self.botaoFrequencia.pack(side='left', pady=10)

        self.botaoPerformance = s.CTkButton(self.frameTOP, text="Gráfico de Performace", image=self.arqPerform, hover_color=None, fg_color="transparent", command=lambda: self.cria_grafo_duracao()) #
        self.botaoPerformance.pack(side='left', pady=10)

        self.botaoPetriNet = s.CTkButton(self.frameTOP, text="Gráfico PetriNet", image=self.arqPetri, hover_color=None, fg_color="transparent") #, command=lambda: cria_grafo_petri_net(log)
        self.botaoPetriNet.pack(side='left', pady=10)

        #Switch:
        self.switch_var = s.StringVar(value="off")
        self.switch = s.CTkSwitch(self.frameTOP, text=None, variable=self.switch_var, onvalue="on", offvalue="off", command=lambda: self.modo_escuro())
        self.switch.pack(side='right')

        return


    def modo_escuro(self):
        if self.switch.get() == "on":
            s.set_appearance_mode("Dark")
        else:
            s.set_appearance_mode("Light")

    
    def escolhe_arquivo(self):
        self.caminho_do_arquivo = askopenfilename(filetypes=[ ("Arquivo Excel", "*.xlsx"),("Arquivo CSV", "*.csv"), ("Arquivo XES", '*.xes')])
        if self.caminho_do_arquivo:
            self.label_arquivo.configure(text=f"Arquivo selecionado: {self.caminho_do_arquivo}") # Calma é pra não estar definido msm
    
        tipoArq = self.caminho_do_arquivo.split('.')
        try:
            if tipoArq[-1] in 'csv':
                self.dataframe = pd.read_csv(self.caminho_do_arquivo, sep= ';')
            elif tipoArq[-1] in 'xlsx':
                self.dataframe = pd.read_excel(self.caminho_do_arquivo)

            elif tipoArq[-1] in 'xes':
                self.dataframe = pm4py.read_xes(self.caminho_do_arquivo)
            
            self.dataframe.drop('Unnamed: 0', axis = 1, inplace=True)

            return self.janela_define_chaves()
        except Exception as error:
            self.lable_auxImagem.configure(text=f"NÃO CONSEGUI TRANSFORMAR EM GRÁFICO. UMA COLUNA NÃO FOI ENCONTRADA NESSE ARQUIVO.\n erro: {error}")
            
        return
    
    def janela_define_chaves(self):
        raizColunas= s.CTkToplevel(self.raiz)
        raizColunas.transient(self.raiz)
        raizColunas.grab_set()

        self.listID = s.CTkComboBox(raizColunas, values=self.dataframe.columns)
        self.listID.pack()
        
        self.listTimestamp = s.CTkComboBox(raizColunas, values=self.dataframe.columns)
        self.listTimestamp.pack()

        self.listActivity = s.CTkComboBox(raizColunas, values=self.dataframe.columns)
        self.listActivity.pack()

        botaoAplicar = s.CTkButton(raizColunas, text='Aplicar', command=lambda: self.define_chaves())
        botaoAplicar.pack()
        
        return

    
    def define_chaves(self):
        ##REDEFININDO AS VARIÁVEIS PORQUE PELO VISTO O TKINTER NÃO RECONHECE COMO VARIÁVEL DA JANELA PRINCIPAL OS WIDGETS CRIADOS EM JANELAS TIPO Toplevel()
        self.ID = self.listID.get()
        self.Timestamp = self.listTimestamp.get()
        self.Activity = self.listActivity.get()
        ###################################################################################################################################################
        
        self.log = pm4py.format_dataframe(self.dataframe, case_id= self.listID.get(), activity_key= self.listActivity.get(), timestamp_key=self.listTimestamp.get())
        return


    def exibe_grafico(self, caminho):
        caminho = './'+caminho
        if caminho:
            tamanho_grafico_largura = 1340 
            tamanho_grafico_altura = 110
            # Carrega a nova imagem
            pil_image = Image.open(caminho)
            ctk_image = s.CTkImage(light_image=pil_image, dark_image=pil_image, size= (tamanho_grafico_largura, tamanho_grafico_altura))

            # Atualiza o rótulo com a nova imagem
            self.image_label.configure(image=ctk_image)
            self.image_label.image = ctk_image
        return
    
    def filtra_grafo_por_variantes(self):
        self.log.fillna({self.Timestamp: 0},inplace=True)
        self.log[self.Timestamp] = pd.to_datetime(self.log[self.Timestamp])
        self.log[self.ID] = self.log[self.ID].astype(str)
        self.log[self.Activity] = self.log[self.Activity].astype(str)

        self.filtrado = pm4py.filtering.filter_variants_by_coverage_percentage(self.log, self.slider_Paths.get(), case_id_key=self.ID, activity_key=self.Activity, timestamp_key=self.Timestamp)
        # self.filtrado = self.filtrado.drop('Unnamed: 0', axis=1, inplace=True)
        
    
    def cria_grafo_duracao(self):
    ############################################### FILTRA OS PATHS ###############################################
        self.filtra_grafo_por_variantes()

        performance_dfg, start_activities, end_activities = pm4py.discover_performance_dfg(self.filtrado, case_id_key=self.ID, activity_key=self.Activity, timestamp_key=self.Timestamp)
    ################################ ESSE PARAMETRO COLOCA NO GRÁFICO O TEMPO QUE CADA ATIVIDADE DUROU ###################################
        
        pm4py.vis.save_vis_performance_dfg(performance_dfg, start_activities, end_activities, "grafico_Duracao.png") #serv_time – (optional) provides the activities’ service times, used to decorate the graph
        ##----------------------------------------------------------------------------------------------------------------------------------------
        self.lable_auxImagem.configure(text="Imagem do DFG salva como 'grafico_Duracao.png'")

        self.exibe_grafico("grafico_Duracao.png")
        return