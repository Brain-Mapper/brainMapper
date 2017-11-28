import sys, os
from PyQt4 import QtGui, QtCore

from PyQt4.Qt import *

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
        self.statusBar() # Fait apparaitre la bar en bas, ou l'on peut mettre des tips
        menubar = self.menuBar() #Creation de la bar de menu
        
        # PARAMETRES FENETRE
        self.setGeometry(300, 200, 800, 500)
        self.setWindowTitle('BrainMapper')
        self.setWindowIcon(QtGui.QIcon('ressources/logo.png'))
        
        # DEFINITION DES ACTIONS DES MENUS
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
        niftiAction.triggered.connect(self.buttonClicked)
        
        
        # AJOUT DES ACTIONS AU MENU CORRESPONDANT
        fileMenu = menubar.addMenu('&Program')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)
        SetMenu = menubar.addMenu('&New Set')
        SetMenu.addAction(setAction)
        SetMenu.addAction(excelAction)
        SetMenu.addAction(niftiAction)

        # DEFINITION DES BOUTONS 
        btnNS = QtGui.QPushButton('Set 1 : Speech', self)
        btnNS.setStatusTip('Set 1 : Speech')
        btnNS.setFixedWidth(150)
        btnNS.move(1, 27)
        btnNS.clicked.connect(self.buttonClicked) # Action du bouton           
        
        self.show()

    def buttonClicked(self):
        print "Test passed. SUCCESS!"

    def showHelp(self):
        self.w = Help()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


