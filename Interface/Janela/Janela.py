from datetime import timedelta
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
from typing import OrderedDict
import customtkinter as s
import CTkMessagebox
import os
from PIL import Image, ImageTk
import pm4py
from pm4py.objects.petri_net.importer import importer as pmnl_importer
import pandas as pd

from datetime import  datetime, timedelta
from collections import OrderedDict

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
        self.frameConform.pack(side='bottom', fill='both')

        # Imagens dos botões:
        self.arq = s.CTkImage(light_image=Image.open('Interface\\Janela\\iconArq.png'), dark_image=Image.open('Interface\\Janela\\iconArq.png'), size=(80,80))
        self.arqPerform = s.CTkImage(light_image=Image.open('Interface\\Janela\\iconPerformance.png'), dark_image=Image.open('Interface\\Janela\\iconPerformanceDark.png'), size=(80,80))
        self.arqFreq = s.CTkImage(light_image=Image.open('Interface\\Janela\\iconFreq.png'), dark_image=Image.open('Interface\\Janela\\iconFreqDark.png'), size=(80,80))
        self.arqPetri = s.CTkImage(light_image=Image.open('Interface\\Janela\\iconPetri.png'), dark_image=Image.open('Interface\\Janela\\iconPetriDark.png'), size=(80,80))
        self.arqNot = s.CTkImage(light_image=Image.open('Interface\\Janela\\mode.png'), dark_image=Image.open('Interface\\Janela\\modeDark.png'), size=(20,20))

        # Labels:
        self.label_aux_agg_duracao = s.CTkLabel(self.frame_lateral, text="ESCOLHA UM DE AGREGAÇÃO PARA DURAÇÃO")
        self.label_aux_agg_duracao.pack()

        self.label_arquivo = s.CTkLabel(self.frameTOP, text="Nenhum arquivo selecionado")
        self.label_arquivo.pack(side='bottom')

        self.label_escalaA = s.CTkLabel(self.frame_escala, text="Activities")
        self.label_escalaA.place(relx=0.3, rely=0.1, anchor= CENTER)

        self.label_escalaP = s.CTkLabel(self.frame_escala, text="Paths")
        self.label_escalaP.place(relx=0.7, rely=0.1, anchor= CENTER)

        self.lableConform = s.CTkLabel(self.frameConform, text=None, font=('Arial', 20))
        self.lableConform.pack()

        self.image_label = s.CTkLabel(self.frame_grafico, text=None)
        self.image_label.pack()

        self.label_agg_measure = s.CTkLabel(self.frame_grafico, text=None, font=('Arial', 12))
        self.label_agg_measure.pack(side='bottom')


        # Sliders:
        self.slider_Activities = s.CTkSlider(self.frame_escala, from_=1, to=0, orientation='vertical')
        self.slider_Activities.set(0)
        self.slider_Activities.place(relx=0.3, rely=0.5, anchor= CENTER)

        self.slider_Paths = s.CTkSlider(self.frame_escala,from_=0.9, to=0, orientation='vertical')
        self.slider_Paths.set(0)
        self.slider_Paths.place(relx=0.7, rely=0.5, anchor=CENTER)

        # Botões: 
        self.botaoArquivo = s.CTkButton(self.frameTOP, text= "Seleção de arquivos" , image=self.arq, hover_color=None, fg_color="black", command= lambda: self.escolhe_arquivo())
        self.botaoArquivo.pack(side='left')

        self.botaoConform = s.CTkButton(self.frame_lateral, text='Análise de Conformidade', command=lambda: self.analize_conformidade())
        self.botaoConform.pack(before = self.label_aux_agg_duracao)

        self.botaoFrequencia = s.CTkButton(self.frameTOP, text="Gráfico de Frequência", image=self.arqFreq, hover_color=None, fg_color="transparent", command=lambda: self.cria_grafo_dfg())
        self.botaoFrequencia.pack(side='left', pady=10)

        self.botaoPerformance = s.CTkButton(self.frameTOP, text="Gráfico de Performace", image=self.arqPerform, hover_color=None, fg_color="transparent", command=lambda: self.cria_grafo_duracao()) 
        self.botaoPerformance.pack(side='left', pady=10)

        self.botaoPetriNet = s.CTkButton(self.frameTOP, text="Gráfico PetriNet", image=self.arqPetri, hover_color=None, fg_color="transparent", command=lambda: self.cria_grafo_petri_net())
        self.botaoPetriNet.pack(side='left', pady=10)

        #Switch:
        # self.switch_var = s.StringVar(value="on")
        # self.switch = s.CTkSwitch(self.frameTOP, text=None, variable=self.switch_var, onvalue="on", offvalue="off", command=lambda: self.modo_escuro())
        # self.switch.pack(side='right')

        #Combo:
        self.agg_measure = s.CTkComboBox(self.frame_lateral, values=['mean', 'median', 'min', 'max', 'sum'], command=lambda _: self.agg_duracao_atividades(self.agg_measure.get()))
        self.agg_measure.pack(side='bottom')


        return

# Não usado porque o nome dos gráficos ficam invisíveis no modo claro
    def modo_escuro(self):
    #     if self.switch.get() == "on":
    #         s.set_appearance_mode("Dark")
    #     else:
    #         s.set_appearance_mode("Light")
        return
    
    def escolhe_arquivo(self):
        self.caminho_do_arquivo = askopenfilename(filetypes=[ ("Arquivo Excel", "*.xlsx"),("Arquivo CSV", "*.csv"), ("Arquivo XES", '*.xes')])
        if self.caminho_do_arquivo:
            self.label_arquivo.configure(text=f"Arquivo selecionado: {self.caminho_do_arquivo}")
    
        tipoArq = self.caminho_do_arquivo.split('.')
        try:
            if tipoArq[-1] in 'csv':
                self.dataframe = pd.read_csv(self.caminho_do_arquivo, sep= ';')
            elif tipoArq[-1] in 'xlsx':
                self.dataframe = pd.read_excel(self.caminho_do_arquivo)

            elif tipoArq[-1] in 'xes':
                self.dataframe = pm4py.read_xes(self.caminho_do_arquivo)

            try:
                self.dataframe.drop('Unnamed: 0', axis = 1, inplace=True)
            except:
                pass
            return self.janela_define_chaves()
        except Exception as e:
            self.avisos(f"Selecione um arquivo!\nerro: {e}")
            
        return
    
    def janela_define_chaves(self):
        self.raizCaio= s.CTkToplevel(self.raiz)
        self.raizCaio.transient(self.raiz)
        self.raizCaio.grab_set()

        self.listID = s.CTkComboBox(self.raizCaio, values=self.dataframe.columns)
        self.listID.set("Case ID")
        self.listID.pack()
        
        self.listTimestampInicio = s.CTkComboBox(self.raizCaio, values=self.dataframe.columns)
        self.listTimestampInicio.set("Timestamp: Início")
        self.listTimestampInicio.pack()

        self.listTimestampFinal = s.CTkComboBox(self.raizCaio, values=self.dataframe.columns)
        self.listTimestampFinal.set("Timestamp: Final")
        self.listTimestampFinal.pack()


        self.listActivity = s.CTkComboBox(self.raizCaio, values=self.dataframe.columns)
        self.listActivity.set("Activity")
        self.listActivity.pack()

        botaoAplicar = s.CTkButton(self.raizCaio, text='Aplicar', command=lambda: self.define_chaves())
        botaoAplicar.pack()
        
        return

    
    def define_chaves(self):
        ##REDEFININDO AS VARIÁVEIS PORQUE PELO VISTO O TKINTER NÃO RECONHECE COMO VARIÁVEL DA JANELA PRINCIPAL OS WIDGETS CRIADOS EM JANELAS TIPO Toplevel()
        self.ID = self.listID.get()
        self.Timestamp = self.listTimestampInicio.get()
        self.Activity = self.listActivity.get()
        ########################################################################################################################################
        try:
            self.log = pm4py.format_dataframe(self.dataframe, case_id= self.listID.get(), activity_key= self.listActivity.get(), timestamp_key=self.listTimestampFinal.get())

        except Exception as e:
            self.avisos(f'Selecione uma coluna que exista no arquivo\n {e}')

        return self.raizCaio.destroy()


    def exibe_grafico(self, caminho):
        caminho = './'+caminho
        if caminho:
            tamanho_grafico_largura = 1340 
            tamanho_grafico_altura = 300
            # Carrega a nova imagem
            pil_image = Image.open(caminho)
            ctk_image = s.CTkImage(light_image=pil_image, dark_image=pil_image, size= (tamanho_grafico_largura, tamanho_grafico_altura))

            # Atualiza o rótulo com a nova imagem
            self.image_label.configure(image=ctk_image)
            self.image_label.image = ctk_image
        return
    
    def filtra_grafo_por_variantes(self):
        try:
            self.log.fillna({self.Timestamp: 0},inplace=True)
            self.log[self.Timestamp] = pd.to_datetime(self.log[self.Timestamp])
            self.log[self.ID] = self.log[self.ID].astype(str)
            self.log[self.Activity] = self.log[self.Activity].astype(str)
        except AttributeError:
            self.avisos('Nenhum arquivo selecionado:')

        except Exception as e:
            self.avisos(type(e).__name__)

        self.filtradoPath = pm4py.filtering.filter_variants_by_coverage_percentage(self.log, self.slider_Paths.get(), case_id_key=self.ID, activity_key=self.Activity, timestamp_key=self.Timestamp)
        return

    
       
    def filtra_grafo_por_atividades(self):
        # Obter valor do slider
        bet = self.slider_Activities.get()
        # Obter a contagem das atividades
        activity_counts = pm4py.stats.get_event_attribute_values(self.filtradoPath, attribute=self.Activity,case_id_key=self.ID)
        # Porcentagem de acordo com o maximo de atividades
        maximo = max(activity_counts.values()) * bet

        # Imprimir as contagens das atividades
        for activity, count in activity_counts.items():
            if count < maximo:
                self.filtrado = self.filtradoPath[self.filtradoPath[self.Activity]!=activity]
            else:
                self.filtrado = self.filtradoPath
        return 

    def cria_grafo_duracao(self):
    ############################################### FILTRA OS PATHS ###############################################
        self.filtra_grafo_por_variantes()
        self.filtra_grafo_por_atividades()
    ###############################################################################################################
        performance_dfg, start_activities, end_activities = pm4py.discover_performance_dfg(self.filtrado, case_id_key=self.ID, activity_key=self.Activity, timestamp_key=self.Timestamp)
    ################################ ESSE PARAMETRO COLOCA NO GRÁFICO O TEMPO QUE CADA ATIVIDADE DUROU ###################################
        pm4py.vis.save_vis_performance_dfg(performance_dfg, start_activities, end_activities, "grafico_Duracao.png") #serv_time – (optional) provides the activities’ service times, used to decorate the graph
        ##----------------------------------------------------------------------------------------------------------------------------------------
        self.exibe_grafico("grafico_Duracao.png")
        return
    
    def cria_grafo_dfg(self):
    ############################################### FILTRA OS PATHS ###############################################
        self.filtra_grafo_por_variantes()
        self.filtra_grafo_por_atividades()
    ###############################################################################################################
        dfg, start_activities, end_activities = pm4py.discover_dfg(self.filtrado, case_id_key=self.ID, activity_key=self.Activity, timestamp_key=self.Timestamp)
        pm4py.vis.save_vis_dfg(dfg, start_activities, end_activities, "grafico.png")#, rankdir='TB'

        self.exibe_grafico("grafico.png")
        
        return
    
    def cria_grafo_petri_net(self):
    ############################################### FILTRA OS PATHS ###############################################
        self.filtra_grafo_por_variantes()
        self.filtra_grafo_por_atividades()
    ###############################################################################################################
        pn, ini, fim = pm4py.discover_petri_net_inductive(self.filtrado)
        pm4py.vis.save_vis_petri_net(pn, ini, fim, "grafico_PetriNet.png")

        self.exibe_grafico("grafico_PetriNet.png")
        
        return
    
    def analize_conformidade(self):
        # log['ID'] = log['ID'].astype(str)
        self.caminho_do_modelo = askopenfilename(filetypes=[("Arquivo Pnml", "*.pnml")])
        rede, inicial, final = pmnl_importer.apply(self.caminho_do_modelo)
        try:
            duda_result = pm4py.fitness_token_based_replay(self.log, rede, inicial, final, case_id_key=self.ID, activity_key=self.Activity, timestamp_key=self.Timestamp)
            self.lableConform.configure(text=f'média fittness: %.3f \n fittness: %.2f %%'%(duda_result["average_trace_fitness"], duda_result["percentage_of_fitting_traces"]))
        except Exception as e:
             self.avisos(f'selecione um gráfico primeiro!\n{type(e).__name__}')

        return
    

    def agg_duracao_atividades(self, measure):
        try:
            media_atividades= pm4py.get_service_time(self.log, start_timestamp_key=self.Timestamp, aggregation_measure=measure)
            # media_atividades = OrderedDict(media_atividades)
            mensagem = ''
            for atividade,segundos in media_atividades.items():
                segundos_arredondados = round(segundos)
                media_horas = timedelta(seconds=segundos_arredondados)
                mensagem += f"| {atividade} - {media_horas} horas |\n"
            self.label_agg_measure.configure(text = mensagem)

        except Exception as e:
            self.avisos(type(e).__name__)
        return
    
    
    # pensando se não faço isso ser uma classe
    def avisos(self, nome_do_erro):
        return CTkMessagebox.CTkMessagebox(self.raiz, title = 'AVISO!', message = f"Ocorreu um erro do tipo: \n{nome_do_erro}")