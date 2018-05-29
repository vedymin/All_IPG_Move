from pyas400 import ConnectionManager
import main_gui
from PyQt5 import QtCore, QtGui, QtWidgets

conn = ConnectionManager()


def add_connections():

    ui.choose_session_combo.clear()
    connections = conn.get_available_connections()
    ui.choose_session_combo.addItems(connections)

def check_loggged():

    session = ui.choose_session_combo.currentText()
    conn.open_session(session)

    if conn.check_logged_in(session):
        print("logged in")
    else:
        error_non_logged()
        print("not logged in")


def error_non_logged():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("You are not logged in here. Log in or choose another session")
    msg.setWindowTitle("Warning")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.show()
    msg.exec_()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = main_gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.refresh_session_button.clicked.connect(add_connections)
    add_connections()
    MainWindow.show()
    sys.exit(app.exec_())