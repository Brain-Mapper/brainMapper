import os
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *

from functools import partial

import resources

from mainView import MainView
from clusteringView import ClusteringView

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
        self.setWindowIcon(QtGui.QIcon(':ressources/help.png'))
        self.setGeometry(QRect(100, 100, 400, 200))
        label = QLabel(self)
        pixmap = QPixmap(':ressources/logo.png')
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        label.move(10,10)
        names = QLabel("Raphael Agathon & Maxime Cluchague",self)
        names2 = QLabel("  Graziella Husson & Valentina Zelaya", self)
        title= QLabel("BrainMapper", self)
        icons_credits=QLabel("BrainMapper icon made by Graziella Husson \nApp icons made by Icomoon from www.flaticon."
                             "com ", self)
        names.setGeometry(QtCore.QRect(70, 110, 400, 100))
        names2.setGeometry(QtCore.QRect(73, 130, 400, 100))
        title.setGeometry(QtCore.QRect(210, 20, 400, 100))
        icons_credits.setGeometry(QtCore.QRect(10, 80, 400, 100))
        self.show()


class Error(QMainWindow):
    def __init__(self, message):
        QMainWindow.__init__(self)
        self.setWindowTitle('Error')
        self.setWindowIcon(QtGui.QIcon(':ressources/error.png'))
        self.setGeometry(QRect(100, 100, 400, 200))
        self.show()
        print message


# In PyQt we cannot open two windows at a time easily, so we will have to change the central widget of our app
# according to what the user clicks on... To do so, we will use an instance of the following class

# The class Home Page implements a custom QWidget that can stack several QWidgets
# We will use an instance of it as the central widget of our application, thus facilitating the switch
# between the different views of our application
class HomePage(QWidget):

    def __init__(self, parent=None):

        super(HomePage, self).__init__(parent)

        # Initialize a stack (pile) widget
        self.stack = QStackedWidget()
        layout = QVBoxLayout(self) # vertical layout
        layout.addWidget(self.stack) # stack in the vertical layout

        # Here are the custom widgets we will put on the stack
        self.mainview = MainView()
        self.clustering = ClusteringView()
        # -- Add them to stack widget
        self.stack.addWidget(self.mainview)
        self.stack.addWidget(self.clustering)

        # Define behaviour when widget emit certain signals (see class MainView and Clustering View for more details
        #  on signals and events)

        # -- when mainView widget emits signal showClust, change current Widget in stack to clustering widget
        self.mainview.showClust.connect(partial(self.stack.setCurrentWidget, self.clustering))
        # -- when clustering widget emits signal showMain, change current Widget in stack to main view widget
        self.clustering.showMain.connect(partial(self.stack.setCurrentWidget, self.mainview))

        # Set current widget to main view by default
        self.stack.setCurrentWidget(self.mainview)


class UI(QtGui.QMainWindow):

    # ---------- Box Layout Set up with Widgets ---------
    # Since we cannot change the layout of a QtMainWindow, we will use a CENTRAL WIDGET (var homepage)
    # This central widget is an instance of HomePage class here above, and represents a stack of widgets
    # This stack contains several custom widgets from and to we will change as the users clicks on buttons
    
    def __init__(self):
        super(UI, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        self.statusBar() # lower bar for tips

        
        # WINDOW PARAMETERS
        rec = QApplication.desktop().availableGeometry()
        screenHeight = rec.height()
        screenWidth = rec.width()
        self.setGeometry(300, 200, screenWidth/1.5, screenHeight/1.4)
        self.setWindowTitle('BrainMapper')
        self.setWindowIcon(QtGui.QIcon(':ressources/logo.png'))

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

        homepage = HomePage()
        self.setCentralWidget(homepage)
        self.show()


    def buttonClicked(self):
        print "Test passed. SUCCESS!"

    def show_coll(self, coll):
        print coll

    def fromNiFile(self):
        file = QFileDialog.getOpenFileNames()
        if len(file) == 1:
            try:
                open_nifti(str(file[0]))
            except:
                self.w = Error(sys.exc_info()[0])
        else:
            try:
                collec = do_image_collection(file)
                self.show_coll(collec)
            except:
                self.w = Error(sys.exc_info()[0])

    def showHelp(self):
        self.w = Help()


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


