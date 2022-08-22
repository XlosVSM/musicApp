from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sys import argv, exit

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Python")
        
        self.setGeometry(100, 100, 600, 400)
        
        self.UiComponents()
        
        self.show()
        
    def UiComponents(self):
        label = QLabel("Label", self)
        
        label.setGeometry(100, 100, 120, 40)
        
        label.setStyleSheet("border: 2px solid black")
        
        self.showMaximized()
    
App = QApplication(argv)

window = Window()

exit(App.exec())