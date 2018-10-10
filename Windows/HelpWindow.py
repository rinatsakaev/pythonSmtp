from PyQt5 import QtWidgets

from UI.Help_UI import Ui_HelpWindow


class HelpWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_HelpWindow()
        self.ui.setupUi(self)
