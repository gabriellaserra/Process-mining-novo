from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog
import pm4py
import pandas as pd

class SeletorDeArquivo(QDialog):
    def __init__(self, window):
        super().__init__()
        self.mainwindow = window
        self.setGeometry(100, 100, 520, 300) 
        self.uiComponents()
        self.show()

    def uiComponents(self):
        
        filepath = QLabel("Filepath:",self)
        self.setGeometry(100, 100, 520, 300) 
        filepath.setGeometry(10,0,70,40)
        self.line = QLineEdit(self)
        self.line.setGeometry(10,40,500,40)
        
        searchButton = QPushButton('Browse', self)
        searchButton.move(430,90)
        searchButton.clicked.connect(self.browseFiles)

        self.comboBox= QComboBox(self)
        self.comboBox.addItems(["DFG Duração", "DFG Frequência", "Heuristic Miner", "Rede de Petri"])
        self.comboBox.setGeometry(10,160,500,40) 

        showButton = QPushButton("Show",self)
        showButton.move(430,210)
        showButton.clicked.connect(self.confirmGrafico)

        
    def browseFiles(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "/home", "Excel Files (*.xlsx);;CSV Files (*.csv)")
        self.line.setText(filename[0])

    def confirmGrafico(self):
        geracao = self.comboBox.currentText()
        filepath = self.line.text()
        
        if geracao == "DFG Duração":
            self.showDFGDuration(filepath)
        elif geracao == "DFG Frequência":
            self.showDFGFrequency(filepath)
        elif geracao == "Heuristic Miner":
            self.showHeuristicMiner(filepath)
        elif geracao == "Rede de Petri":
            self.showPetriNet(filepath)
    
    def showDFGDuration(self, filepath):
        log = self.load_data(filepath)
        if log is not None:
            log = log.dropna(subset=['Início'])
            log['ID'] = log['ID'].astype(str)
            performance_dfg, start_activities, end_activities = pm4py.discover_performance_dfg(log, case_id_key='ID', activity_key='Ocorrência', timestamp_key='Início')
            pm4py.view_performance_dfg(performance_dfg, start_activities, end_activities)
    
    def showDFGFrequency(self, filepath):
        log = self.load_data(filepath)
        if log is not None:
            log = log.dropna(subset=['Início'])
            log['ID'] = log['ID'].astype(str)
            dfg, start_activities, end_activities = pm4py.discover_dfg(log, case_id_key='ID', activity_key='Ocorrência', timestamp_key='Início')
            pm4py.view_dfg(dfg, start_activities, end_activities)
    
    def showHeuristicMiner(self, filepath):
        log = self.load_data(filepath)
        if log is not None:
            log = log.dropna(subset=['Início'])
            log['ID'] = log['ID'].astype(str)
            heuristics_net = pm4py.discover_heuristics_net(log, case_id_key='ID', activity_key='Ocorrência', timestamp_key='Início')
            pm4py.view_heuristics_net(heuristics_net)
    
    def showPetriNet(self, filepath):
        log = self.load_data(filepath)
        if log is not None:
            log = log.dropna(subset=['Início'])
            log['ID'] = log['ID'].astype(str)
            petri_net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log, case_id_key='ID', activity_key='Ocorrência', timestamp_key='Início')
            pm4py.view_petri_net(petri_net, initial_marking, final_marking)
            
    def load_data(self, filepath):
        try:
            if filepath.endswith('.csv'):
                return pd.read_csv(filepath)
            elif filepath.endswith('.xlsx'):
                return pd.read_excel(filepath)
            else:
                print("Unsupported file format.")
                return None
        except Exception as e:
            print(f"Error loading file: {e}")
            return None