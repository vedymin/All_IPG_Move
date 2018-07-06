from as400 import ConnectionManager
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
    ui.from_line_edit.setText('222000000000000010')
    ui.to_line_edit.setText('000009203008170004')

    # ui.choose_session_combo.setCurrentIndex(3)

"""Main functions."""


def start_moving():
    global hd_from
    global hd_to
    global session

    delete_object()

    session = ui.choose_session_combo.currentText()
    conn.open_session(session)
    conn.set_active_session(session)

    hd_from = ui.from_line_edit.text()
    hd_to = ui.to_line_edit.text()

    if check_loggged() is False or check_hd() is False:
        return

    conn.esc()
    conn.send_keys("go hlmu00"),
    conn.enter()
    conn.send_keys("4")
    conn.enter()
    conn.send_keys("2")
    conn.enter()
    conn.send_keys(hd_from, 20, 28)

    """ Ckeck if HD is for pick or prepared"""
    conn.fkey(11)
    conn.send_keys("Y",13,31)
    conn.send_keys(" ", 14, 31)
    conn.enter()
    if conn.get_text(11, 8, 10) != "          ":
        error_msg("HD have items to pick")
        conn.fkey(12, 5)
        return

    conn.enter()
    conn.fkey(11)
    conn.send_keys(" ", 13, 31)
    conn.send_keys("Y", 14, 31)
    conn.enter()
    if conn.get_text(11, 8, 10) != "          ":
        error_msg("HD have prepared")
        conn.fkey(12, 5)
        return
    conn.enter()
    conn.fkey(11)
    conn.send_keys(" ", 13, 31)
    conn.send_keys(" ", 14, 31)
    conn.enter()

    """ Start moving """

    while conn.get_text(11, 8, 1) != " ":
        conn.send_keys("20")
        conn.enter()
        if conn.get_text(24, 28, 16) == "must be in place":
            conn.send_keys("14")
            conn.enter()
            conn.send_keys("23")
            conn.enter()
            conn.fkey(12)
            conn.send_keys("20")
            conn.enter()

        pcs = conn.get_text(12, 28, 7)
        conn.send_keys(pcs,16,28)
        conn.send_keys(hd_to, 17, 34)
        # conn.set_cursor(18,34),,
        # conn.tab()
        conn.send_keys("N", 18, 34)
        # conn.tab(7)
        # conn.set_cursor(20,34)
        conn.send_keys("N", 20, 34)
        conn.enter()
        conn.fkey(20)
        print("break")

    conn.fkey(12, 5)



    return

def delete_object():
    conn.sessions = None


"""Checking and errors messages."""


def check_loggged():
    if conn.check_logged_in(session):
        print("logged in")
        return True
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
