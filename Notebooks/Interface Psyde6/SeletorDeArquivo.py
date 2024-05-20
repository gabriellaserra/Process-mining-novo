from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog


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
        filename = QFileDialog.getOpenFileName(self, "Open File", "/home", "csv (*.csv)", "excel (*xlsx)")
        self.line.setText(filename[0])

    def confirmGrafico(self):
        geracao = self.comboBox.currentText()
        filepath = self.line.text()
        self.mainwindow.initUI(geracao, filepath)


        

