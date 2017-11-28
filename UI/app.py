import sys
from PyQt4 import QtGui, QtCore

class UI(QtGui.QWidget):
    
    def __init__(self):
        super(UI, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setGeometry(300, 200, 800, 500)
        self.setWindowTitle('BrainMapper')
        self.setWindowIcon(QtGui.QIcon('ressources/web.png'))

        btnNS = QtGui.QPushButton('New Set', self)
        btnNS.setToolTip('This is a <b>QPushButton</b> widget')
        btnNS.setFixedWidth(150)
        btnNS.move(1, 1)
        btnNS.clicked.connect(self.buttonClicked)            

        btnNC = QtGui.QPushButton('New Collection', self)
        btnNC.setToolTip('This is a <b>QPushButton</b> widget')
        btnNC.setFixedWidth(150)
        btnNC.move(151, 1)
        
        self.show()

    def buttonClicked(self):
        print "ahah"
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


