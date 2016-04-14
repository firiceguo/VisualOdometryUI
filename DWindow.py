# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from ui import Ui_VisualOdometryUI


class DWindow(QtGui.QDialog, Ui_VisualOdometryUI):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    widget = DWindow()
    widget.show()
    sys.exit(app.exec_())
