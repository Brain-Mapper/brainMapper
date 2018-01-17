import os
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *

from functools import partial

import resources

from mainView import MainView
from clusteringView import ClusteringView
from editCollectionsView import EditCollectionsView
from exportView import ExportView
from calculationView import CalculationView


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
        self.calculation = CalculationView()
        self.edit_colls = EditCollectionsView()
        self.export = ExportView()
        # -- Add them to stack widget
        self.stack.addWidget(self.mainview)
        self.stack.addWidget(self.clustering)
        self.stack.addWidget(self.calculation)
        self.stack.addWidget(self.edit_colls)
        self.stack.addWidget(self.export)

        # Define behaviour when widget emit certain signals (see class MainView and Clustering View for more details
        #  on signals and events)

        # -- when mainView widget emits signal showClust, change current Widget in stack to clustering widget
        self.mainview.showClust.connect(self.updateClusteringView)
        # -- when clustering widget emits signal showMain, change current Widget in stack to main view widget
        self.clustering.showMain.connect(partial(self.stack.setCurrentWidget, self.mainview))

        self.mainview.showEdit.connect(self.updateEditView)
        # -- when mainView widget emits signal showEdit, change current Widget in stack to clustering widget
        self.mainview.showEdit.connect(partial(self.stack.setCurrentWidget, self.edit_colls))
        # -- when collection edition widget emits signal showMain, change current Widget in stack to main view widget
        self.edit_colls.showMain.connect(partial(self.stack.setCurrentWidget, self.mainview))
        self.edit_colls.showMain.connect(self.updateMain)

        self.mainview.showExport.connect(self.updateExportView)
        self.export.showMain.connect(partial(self.stack.setCurrentWidget, self.mainview))

    # -- when mainView widget emits signal showCalcul, change current Widget in stack to calculation widget
        self.mainview.showCalcul.connect(partial(self.stack.setCurrentWidget, self.calculation))
        # -- when calculation widget emits signal showMain, change current Widget in stack to main view widget
        self.calculation.showMain.connect(partial(self.stack.setCurrentWidget, self.mainview))

        # Set current widget to main view by default
        self.stack.setCurrentWidget(self.mainview)

    def updateClusteringView(self):
        self.clustering.fill_table(get_current_usableDataset())
        self.stack.setCurrentWidget(self.clustering)

    def updateEditView(self):
        self.edit_colls.fill_coll()
        self.stack.setCurrentWidget(self.edit_colls)
    
    def updateMain(self):
        self.mainview.update()

    def updateExportView(self):
        self.export.set_usable_data_set(get_current_usableDataset())
        self.stack.setCurrentWidget(self.export)


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
        
        global homepage
        homepage = HomePage()
        self.setCentralWidget(homepage)
        
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
        setAction.setShortcut('Ctrl+S')
        setAction.triggered.connect(self.createSet)

        excelAction = QtGui.QAction('&Import from Excel file', self)
        excelAction.setStatusTip('Import from Excel file')
        excelAction.triggered.connect(self.buttonClicked)

        niftiAction = QtGui.QAction('&Import from NIfTI file(s)', self)
        niftiAction.setStatusTip('Create a collection with one or several NIfTI images (added in the current set)')
        niftiAction.setShortcut('Ctrl+N')
        niftiAction.triggered.connect(self.fromNiFile)

        # ADDING ACTIONS TO MENUS
        fileMenu = menubar.addMenu('&Program')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)
        SetMenu = menubar.addMenu('&New Set')
        SetMenu.addAction(setAction)
        CollecMenu = menubar.addMenu('&New Collection')
        CollecMenu.addAction(excelAction) 
        CollecMenu.addAction(niftiAction) 

        self.show()


    def buttonClicked(self):
        print "Test passed. SUCCESS!"

    def fromNiFile(self):
# -- We create a collection with the list of images the user selected and give it to the main view and the edit view
        file = QFileDialog.getOpenFileNames()
        if (file != ""):
            try:
                collec = do_image_collection(file)
                homepage.mainview.show_coll(collec)
                homepage.edit_colls.fill_coll()
            except:
                err = QtGui.QMessageBox.critical(self, "Error", "An error has occured. Maybe you tried to open a non-NIfTI file")
                #print (sys.exc_info()[0])
        
    def showHelp(self):
        self.w = Help()

    def createSet(self):
# -- We create a set with the name given by the user (if its free) and give it to the mainpage
        text, ok = QInputDialog.getText(self, 'Create a Set', "Enter a name for your set :")
        if str(text)!= "":
##            try:
##                new_ok = True
##                not_ok = ['^','[','<','>',':',';',',','?','"','*','|','/',']','+','$']
##                for i in not_ok:
##                    if i in str(text):
##                        new_ok = False
##                if new_ok and not exists_set(str(text)):
##                    new_set = newSet(str(text))
##                    homepage.mainview.show_set(new_set)
##                else :
##                    err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid (empty, invalid caracter or already exists)")
##            except :
##                err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid ("+str(sys.exc_info()[0])+")")
            if not exists_set(str(text)):
                new_set = newSet(str(text))
                homepage.mainview.show_set(new_set)
            else :
                err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid (empty, invalid caracter or already exists)")
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


