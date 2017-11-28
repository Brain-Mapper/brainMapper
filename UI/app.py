import sys
from PyQt4 import QtGui

class UI(QtGui.QMainWindow):
    
    def __init__(self):
        super(UI, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        exitAction = QtGui.QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 200, 800, 500)
        self.setWindowTitle('BrainMapper')
        self.setWindowIcon(QtGui.QIcon('ressources/logo.png'))

        btnNS = QtGui.QPushButton('Create new Set', self)
        btnNS.setToolTip('This is a <b>QPushButton</b> widget')
        btnNS.setFixedWidth(150)
        btnNS.move(1, 27)
        btnNS.clicked.connect(self.buttonClicked)            

        btnEx = QtGui.QPushButton('Import from Excel', self)
        btnEx.setToolTip('This is a <b>QPushButton</b> widget')
        btnEx.setFixedWidth(150)
        btnEx.move(151, 27)


        btnNf = QtGui.QPushButton('Import from Excel', self)
        btnNf.setToolTip('This is a <b>QPushButton</b> widget')
        btnNf.setFixedWidth(150)
        btnNf.move(301, 27)
        
        self.show()

    def buttonClicked(self):
        print "ahah"
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


