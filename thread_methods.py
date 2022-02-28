from PyQt5 import QtCore


class MyThreadProgressBar(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        self.mysignal.emit(10)
