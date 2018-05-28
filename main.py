from pyas400 import ConnectionManager
import main_gui
from PyQt5 import QtCore, QtGui, QtWidgets

conn = ConnectionManager()


def add_connections():

    connections = conn.get_available_connections()
    ui.choose_session_combo.addItems(connections)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = main_gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    add_connections()
    MainWindow.show()
    sys.exit(app.exec_())