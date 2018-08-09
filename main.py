from as400 import ConnectionManager
import main_gui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *
import time

conn = ConnectionManager()
global hd_from
global hd_to

"""Initial settings and Refresh reaction."""


def add_connections():
    ui.choose_session_combo.clear()
    connections = conn.get_available_connections()
    ui.choose_session_combo.addItems(connections)
    # ui.from_line_edit.setText('000000060004548614')
    # ui.to_line_edit.setText('990000000000000001')
    #
    # ui.choose_session_combo.setCurrentText("D")


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

    """ Go to 4-2 and paste HD"""

    # conn.esc()
    # conn.send_keys("GO HLMU00"),
    if not conn.check("HLMU00", timeout=1):
        error_msg("Please go to main menu and train again. Main menu is after Reflex logo.")
        return
    conn.send_keys("4")
    if not conn.enter("HLMU04", 1):
        err()
        return
    conn.send_keys("2")
    if not conn.enter("HLGE40", 2):
        err()
        return
    conn.send_keys(hd_from, 20, 28)

    """ Ckeck if HD is for pick or prepared"""

    if not conn.fkey(11, program="HLGE45", back=3):
        err()
        return

    conn.send_keys("Y", 13, 31)
    conn.send_keys(" ", 14, 31)
    if not conn.enter("HLGE41", 3):
        err()
        return
    if conn.get_text(11, 8, 10) != "          ":
        error_msg("HD have items to pick")
        conn.fkey(12, 5)
        return

    if not conn.enter("HLGE40", 4):
        err()
        return
    if not conn.fkey(11, program="HLGE45", back=3):
        err()
        return
    conn.send_keys(" ", 13, 31)
    conn.send_keys("Y", 14, 31)
    if not conn.enter("HLGE41", 3):
        err()
        return
    if conn.get_text(11, 8, 10) != "          ":
        error_msg("HD have prepared")
        conn.fkey(12, 5)
        return

    if not conn.enter("HLGE40", 2):
        err()
        return
    if not conn.fkey(11, program="HLGE45", back=3):
        err()
        return
    conn.send_keys(" ", 13, 31)
    conn.send_keys(" ", 14, 31)
    if not conn.enter("HLGE41", 3):
        err()
        return

    """ Start moving """

    first_done = False  # Flag for checking if HD was created by program. After that next IPG's are moved without
    # "New HD" set to "Y"

    while conn.get_text(11, 8, 1) != " ":  # Loop for every IPG line

        conn.send_keys("20")
        conn.enter()
        # time.sleep(5)
        if conn.get_text(24, 28, 16) == "must be in place":  # Changing status of HD to IPL
            conn.send_keys("14")
            if not conn.enter("HLST63", 4):
                err()
                return
            conn.send_keys("23")
            conn.enter()
            if not conn.fkey(12, program="HLGE41", back=3):
                err()
                return
            conn.send_keys("20")
            if not conn.enter("HLGE50", 3):
                err()
                return
        elif not conn.enter("HLGE50", 3):
            err()
            return

        pcs = conn.get_text(12, 28, 7)
        conn.send_keys(pcs, 16, 28)
        conn.send_keys(hd_to, 17, 34)

        # Creation of new HD. If checkbox is ticked then for the first IPG line we need to create.
        # for next lines flag "first_done" is set to true so it is ommited.
        if ui.new_hd_check.isChecked() and first_done == False:
            conn.send_keys("Y", 18, 34)
            conn.erase(18, 34, 5)  # clearing location
            conn.send_keys(ui.location_line_edit.text(), 19, 34)  # location from line_edit
            first_done = True
        else:
            conn.send_keys("N", 18, 34)  # with this set to "N" location will be updated by reflex.

        conn.send_keys("N", 20, 34)  # label no
        conn.send_keys("STD", 18, 75)  # carton type
        conn.enter()
        conn.fkey(20)
        if not conn.check("HLGE41", timeout=15):
            err()
            conn.fkey(12, 5)
            return
        # print("break")

    conn.fkey(12, 3)

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


def err():
    error_msg("Something went wrong! Try again.")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = main_gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.location_line_edit.setDisabled(ui.new_hd_check.checkState() == Qt.Unchecked)
    ui.new_hd_check.stateChanged.connect(lambda state: ui.location_line_edit.setDisabled(state == Qt.Unchecked))
    ui.location_line_edit.setText("RECV-SC")
    ui.refresh_session_button.clicked.connect(add_connections)
    ui.start_button.clicked.connect(start_moving)
    add_connections()
    MainWindow.show()
    sys.exit(app.exec_())
