import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from BrainMapper import * 
    else:
        from ..BrainMapper import * 

class Help(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Help')
        self.setWindowIcon(QtGui.QIcon('ressources/help.png'))
        self.setGeometry(QRect(100, 100, 400, 200))
        label = QLabel(self)
        pixmap = QPixmap(os.getcwd() + '/ressources/logo.png')
        label.setPixmap(pixmap)
        label.resize(pixmap.width(),pixmap.height())
        label.move(10,10)
        names = QLabel("Raphael Agathon & Maxime Cluchague",self)
        names2 = QLabel("  Graziella Husson & Valentina Zelaya", self)
        title= QLabel("BrainMapper", self)
        names.setGeometry(QtCore.QRect(70, 110, 400, 100))
        names2.setGeometry(QtCore.QRect(73, 130, 400, 100))
        title.setGeometry(QtCore.QRect(210, 20, 400, 100))
        self.show()


class UI(QtGui.QMainWindow):
    
    def __init__(self):
        super(UI, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        self.statusBar() # lower bar for tips
        menubar = self.menuBar() #menu bar
        
        # WINDOW PARAMETERS
        self.setGeometry(300, 200, 800, 500)
        self.setWindowTitle('BrainMapper')
        self.setWindowIcon(QtGui.QIcon('ressources/logo.png'))
        
        # ACTIONS AVAILABLE FOR MENUS
        exitAction = QtGui.QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        saveAction = QtGui.QAction('&Help', self)        
        saveAction.setShortcut('Ctrl+H')
        saveAction.setStatusTip('Help')
        saveAction.triggered.connect(self.showHelp)

        setAction = QtGui.QAction('&Create new set', self)     
        setAction.setStatusTip('Create new set')
        setAction.triggered.connect(self.buttonClicked)

        excelAction = QtGui.QAction('&Import from Excel file', self)     
        excelAction.setStatusTip('Import from Excel file')
        excelAction.triggered.connect(self.buttonClicked)

        niftiAction = QtGui.QAction('&Import from NIfTI file', self)    
        niftiAction.setStatusTip('Import from NIfTI file')
        niftiAction.triggered.connect(self.fromNiFile)
        
        
        # ADDING ACTIONS TO MENUS
        fileMenu = menubar.addMenu('&Program')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)
        SetMenu = menubar.addMenu('&New Set')
        SetMenu.addAction(setAction)
        SetMenu.addAction(excelAction)
        SetMenu.addAction(niftiAction)

        # BUTTONS 
        btnNS = QtGui.QPushButton('Set 1 : Speech', self)
        btnNS.setStatusTip('Set 1 : Speech')
        btnNS.setFixedWidth(150)
        btnNS.move(1, 27)
        btnNS.clicked.connect(self.buttonClicked) # Action for button          
        
        self.show()

    def buttonClicked(self):
        print "Test passed. SUCCESS!"

    def fromNiFile(self):
        file = str(QFileDialog.getOpenFileName())
        open_nifti(file)
        
    def showHelp(self):
        self.w = Help()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


