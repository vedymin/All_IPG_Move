import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


app = QApplication(sys.argv)
w=QWidget()
w.setLayout(QVBoxLayout())

QLE_On = QCheckBox("Non-editable?")
generic = QLineEdit()

generic.setDisabled(QLE_On.checkState()==Qt.Unchecked)
QLE_On.stateChanged.connect(lambda state: generic.setDisabled(state==Qt.Unchecked))

w.layout().addWidget(QLE_On)
w.layout().addWidget(generic)
w.show()
sys.exit(app.exec_())