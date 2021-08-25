import sys

from PyQt5 import QtWidgets

from gui.gui import MainMenu

app = QtWidgets.QApplication(sys.argv)
w = MainMenu()
w.show()
sys.exit(app.exec_())
