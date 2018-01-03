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

class Error(QMainWindow):
    def __init__(self, message):
        QMainWindow.__init__(self)
        self.setWindowTitle('Error')
        self.setWindowIcon(QtGui.QIcon('ressources/error.png'))
        self.setGeometry(QRect(100, 100, 400, 200))
        self.show()
        print message


class UI(QtGui.QMainWindow):
    
    def __init__(self):
        super(UI, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        self.statusBar() # lower bar for tips

        
        # WINDOW PARAMETERS
        self.setGeometry(300, 200, 800, 500)
        self.setWindowTitle('BrainMapper')
        self.setWindowIcon(QtGui.QIcon('ressources/logo.png'))

        menubar = self.menuBar()  # menu bar
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

        # ---------- Box Layout Set up ---------
        # Since we cannot change the layout of a QtMainWindow, we will use a CENTRAL WIDGET (var homepage)
        # to which we will add a box layout containing other boxes with their own widgets

        homepage = QtGui.QWidget()

        # This horizontal Box will contain two vertical boxes, one for the set access bar and another for image collec
        # tions display
        middleBox = QtGui.QHBoxLayout()

        # - Vertical box for sets layout
        setAccessBox = QtGui.QVBoxLayout()
        #setAccessBox.addStretch(2)

        # BUTTONS (SET ACCESS)
        btnNS = QtGui.QPushButton('Set 1 : Speech', self)
        btnNS.setStatusTip('Set 1 : Speech')
        btnNS.setFixedWidth(150)
        btnNS.clicked.connect(self.buttonClicked)  # Action for button

        setAccessBox.addWidget(btnNS, 0, Qt.AlignTop)

        # - Vertical box for image collections display
        collectionsDisplayBox = QtGui.QVBoxLayout()
        edit1 = QtGui.QLineEdit()
        edit2 = QtGui.QLineEdit()
        edit3 = QtGui.QTextEdit()
        collectionsDisplayBox.addWidget(edit1)
        collectionsDisplayBox.addWidget(edit2)
        collectionsDisplayBox.addWidget(edit3)

        # Add the previous vertical boxes to horizontal box
        middleBox.addLayout(setAccessBox)
        middleBox.addLayout(collectionsDisplayBox)

        # This horizontal Box will contain two vertical boxes, one for the set access bar and another for image collec
        # tions display
        buttonsBox = QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        # - Buttons to access other windows
        editButton = QtGui.QPushButton("Edit")
        exportButton = QtGui.QPushButton("Export data")
        clusterButton = QtGui.QPushButton("Apply Clustering")
        buttonsBox.addWidget(editButton)
        buttonsBox.addWidget(exportButton)
        buttonsBox.addWidget(clusterButton)

        # Set the layout of homepage widget and set it as the central widget for QtMainWindow
        containerVbox = QtGui.QVBoxLayout()
        containerVbox.addLayout(middleBox)
        containerVbox.addLayout(buttonsBox)

        homepage.setLayout(containerVbox)

        self.setCentralWidget(homepage)
        self.show()

    def buttonClicked(self):
        print "Test passed. SUCCESS!"

    def fromNiFile(self):
        file = QFileDialog.getOpenFileNames()
        if len(file)==1:
            try :
                open_nifti(str(file[0]))
            except :
                self.w = Error(sys.exc_info()[0])
        else:
            try :
                collec = do_image_collection(file)
                self.show_coll(collec)
            except :
                self.w = Error(sys.exc_info()[0])
                
    def showHelp(self):
        self.w = Help()
        
    def show_coll(self, coll):
        print coll
        
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


