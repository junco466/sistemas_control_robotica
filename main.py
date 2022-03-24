from View.Interface import Ui_MainWindow
from Model.Datos import Datos
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    #ui = Ui_MainWindow()
    ui = Datos()
    #ui.setupUi(MainWindow)
    #datos = Datos()
    #MainWindow.show()
    #print(MainWindow.close())
    ui.show()
    sys.exit(app.exec_())