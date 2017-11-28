import sys
from PyQt4 import QtGui


def initUI():
    
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    w.resize(1000, 600)
    w.move(200, 100)
    w.setWindowTitle('BrainMapper')
    w.setWindowIcon(QtGui.QIcon('ressources/web.png'))
    w.show()
    
    sys.exit(app.exec_())


initUI()
