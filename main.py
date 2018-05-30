from pyas400 import ConnectionManager
import main_gui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

conn = ConnectionManager()
global hd_from
global hd_to

"""Initial settings and Refresh reaction."""


def add_connections():
    ui.choose_session_combo.clear()
    connections = conn.get_available_connections()
    ui.choose_session_combo.addItems(connections)


"""Main functions."""


def start_moving():
    global hd_from
    global hd_to
    global session

    session = ui.choose_session_combo.currentText()
    conn.open_session(session)
    conn.set_active_session(session)

    hd_from = ui.from_line_edit.text()
    hd_to = ui.to_line_edit.text()

    if check_loggged() or check_hd() is False:
        return

    conn.send_keys("1")
    conn.enter()


"""Checking and errors messages."""


def check_loggged():
    if conn.check_logged_in(session):
        print("logged in")
    else:
        error_msg("You are not logged in here. Log in or choose another session")
        print("not logged in")
        return False


def check_hd():
    global hd_from
    global hd_to

    # if hd_from.isdigit() or hd_to.isdigit():
    #     error_msg("One of HD have letters inside.")
    #     return False

    if len(hd_from) < 18 or len(hd_to) < 18:
        error_msg("One of the HD is too short.")
        return False
    elif len(hd_from) > 18:
        hd_from = hd_from[-18:len(hd_from)]
        ui.from_line_edit.setText(hd_from)
    elif len(hd_to) > 18:
        hd_to = hd_to[-18:len(hd_to)]
        ui.to_line_edit.setText(hd_to)


def error_msg(info):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(info)
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
    ui.start_button.clicked.connect(start_moving)
    add_connections()
    MainWindow.show()
    sys.exit(app.exec_())
