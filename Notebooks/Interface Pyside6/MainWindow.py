from SeletorDeArquivo import SeletorDeArquivo

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
import pm4py

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Janela em Branco")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        button = QPushButton("Clique aqui para selecionar um arquivo")
        button.clicked.connect(self.createQDialog)

        layout.addWidget(button)

        self.setCentralWidget(central_widget)
    
    def createQDialog(self):
        self.seletor = SeletorDeArquivo(self)

    def initUI(self, geracao, filepath):
        print(geracao, filepath)
  