import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import application

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = application.MyApp()
    window.show()
    sys.exit(app.exec_())