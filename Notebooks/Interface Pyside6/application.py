from MainWindow import MainWindow

from PySide6.QtWidgets import QApplication

import sys

app = QApplication(sys.argv)

main_window = MainWindow()
main_window.show() 

sys.exit(app.exec())