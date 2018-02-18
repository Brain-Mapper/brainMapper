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

        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from BrainMapper import *
    else:
        from ..BrainMapper import *


class Help(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('Help')
        self.setWindowIcon(QtGui.QIcon(':ressources/help.png'))
        self.setFixedSize(465, 235)
        centralwidget = QWidget(self)
        horizontalLayoutWidget = QWidget(centralwidget)
        horizontalLayoutWidget.setGeometry(QRect(0, 0, 461, 231));
        horizontalLayout = QHBoxLayout(horizontalLayoutWidget);

        label = QLabel(horizontalLayoutWidget)
        pixmap = QPixmap(':ressources/logo.png')
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        label.move(10, 10)

        horizontalLayout.addWidget(label)

        verticalLayout = QVBoxLayout()
        label1 = QLabel(horizontalLayoutWidget)
        label1.setText("BrainMapper icon made by Graziella Husson")
        verticalLayout.addWidget(label1)

        label_2 = QLabel(horizontalLayoutWidget)
        label_2.setText("App icons made by Icomoon from flaticon.com")
        verticalLayout.addWidget(label_2)

        label_3 = QLabel(horizontalLayoutWidget)
        label_3.setText("Developped by :")
        verticalLayout.addWidget(label_3)

        label_5 = QLabel(horizontalLayoutWidget)
        label_5.setText("Raphael Agathon, Maxime Cluchague,")
        verticalLayout.addWidget(label_5)

        label_4 = QLabel(horizontalLayoutWidget)
        label_4.setText("Graziella Husson & Valentina Zelaya")
        verticalLayout.addWidget(label_4)

        pushButton = QPushButton(horizontalLayoutWidget)
        pushButton.setText("Show help")
        pushButton.clicked.connect(lambda: self.openUrl(""))
        verticalLayout.addWidget(pushButton)

        horizontalLayout.addLayout(verticalLayout)

        self.setCentralWidget(centralwidget);
        self.show()

    def openUrl(self, url):
        url = QtCore.QUrl('https://brain-mapper.github.io/BrainMapper-help/')
        if not QtGui.QDesktopServices.openUrl(url):
            QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')


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
        layout = QVBoxLayout(self)  # vertical layout
        layout.addWidget(self.stack)  # stack in the vertical layout

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
        self.clustering.showMain.connect(self.updateMainCluster)

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
        self.calculation.showMain.connect(self.updateMainCalcul)

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

    def updateMainCluster(self):
        self.mainview.updateClusterRes()

    def updateMainCalcul(self):
        self.mainview.updateCalculRes()

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

        self.statusBar()  # lower bar for tips

        global homepage
        homepage = HomePage()
        self.setCentralWidget(homepage)

        # WINDOW PARAMETERS
        rec = QApplication.desktop().availableGeometry()
        screenHeight = rec.height()
        screenWidth = rec.width()
        self.setGeometry(300, 200, screenWidth / 1.5, screenHeight / 1.4)
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
        excelAction.setShortcut('Ctrl+E')
        excelAction.triggered.connect(self.fromExcel)

        niftiAction = QtGui.QAction('&Import from NIfTI file(s)', self)
        niftiAction.setStatusTip('Create a collection with one or several NIfTI images (added in the current set)')
        niftiAction.setShortcut('Ctrl+N')
        niftiAction.triggered.connect(self.fromNiFile)

        workspaceImportAction = QtGui.QAction('&Import workspace', self)
        workspaceImportAction.setStatusTip(
            'Import Set and ImageCollection from a workspace and add its to the current set')
        workspaceImportAction.triggered.connect(self.fromWorkspace)

        workspaceSaveAction = QtGui.QAction('&Save workspace', self)
        workspaceSaveAction.setStatusTip('Save the current worksapce')
        workspaceSaveAction.triggered.connect(self.workspaceSave)

        # ADDING ACTIONS TO MENUS
        fileMenu = menubar.addMenu('&Program')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)
        workspaceMenu = menubar.addMenu('&Workspace')
        workspaceMenu.addAction(workspaceImportAction)
        workspaceMenu.addAction(workspaceSaveAction)
        SetMenu = menubar.addMenu('&New Set')
        SetMenu.addAction(setAction)
        CollecMenu = menubar.addMenu('&New Collection')
        CollecMenu.addAction(excelAction)
        CollecMenu.addAction(niftiAction)

        self.show()

    def fromNiFile(self):
        # -- We create a collection with the list of images the user selected and give it to the main view and the edit view
        file = QFileDialog.getOpenFileNames()
        if (file != ""):
            # try:
            collec = do_image_collection(file)
            homepage.mainview.show_coll(collec)
            homepage.edit_colls.fill_coll()
            # except:
            #    err = QtGui.QMessageBox.critical(self, "Error", "An error has occured. Maybe you tried to open a non-NIfTI file")

        # -- We create a collection with the list of images the user selected and give it to the main view and the edit view

    def fromExcel(self):
        file = QFileDialog.getOpenFileName()
        if (file != ""):
            # try:
            collec = simple_import(file, os.path.join(os.path.dirname(__file__),
                                                      'ressources/template_mni/mni_icbm152_t1_tal_nlin_asym_09a.nii'))
            homepage.mainview.show_coll(collec)
            homepage.edit_colls.fill_coll()
            # except:
            #     err = QtGui.QMessageBox.critical(self, "Error",
            #                                      "An error has occured. Maybe you tried to open a non-CSV file")

    def fromWorkspace(self):
        folder_path = str(QFileDialog.getExistingDirectory())
        if (file != ""):
            test = general_workspace_import_control(folder_path)
            print test
            if test is None:
                general_workspace_import(folder_path)
                for key in get_workspace_set():
                    homepage.mainview.show_set(key)
                    rm_workspace_set(key)
                    # Problem to fix : the list is not properly clean, if we don't do rm all, smthg is left in the list...
                ##                    print "list before rm all"
                ##                    for i in get_workspace_set():
                ##                        print i
                rm_all_workspace_set()
            ##                    print "list"
            ##                    for i in get_workspace_set():
            ##                        print i

            else:
                err = QtGui.QMessageBox.critical(self, "Error", "An error has occured. " + test)

    def workspaceSave(self):
        folder_path = str(QFileDialog.getExistingDirectory())
        general_workspace_save(folder_path)

    def showHelp(self):
        self.w = Help()

    def createSet(self):
        # -- We create a set with the name given by the user (if its free) and give it to the mainpage
        text, ok = QInputDialog.getText(self, 'Create a Set', "Enter a name for your set :")
        if str(text) != "":
            try:
                new_ok = True
                not_ok = ['^', '[', '<', '>', ':', ';', ',', '?', '"', '*', '|', '/', ']', '+', '$']
                for i in not_ok:
                    if i in str(text):
                        new_ok = False
                if new_ok and not exists_set(str(text)):
                    new_set = newSet(str(text))
                    homepage.mainview.show_set(new_set)
                else:
                    err = QtGui.QMessageBox.critical(self, "Error",
                                                     "The name you entered is not valid (empty, invalid caracter or already exists)")
            except:
                err = QtGui.QMessageBox.critical(self, "Error",
                                                 "The name you entered is not valid (" + str(sys.exc_info()[0]) + ")")


def main():
    app = QtGui.QApplication(sys.argv)

    # INIT APP STYLE ACCORDING TO OS

    if sys.platform.startswith('linux'):
        app.setStyle(QStyleFactory.create("GTK+"))
    elif sys.platform.startswith('darwin'):
        app.setStyle(QStyleFactory.create("GTK+"))
    elif sys.platform.startswith('win32'):
        app.setStyle(QStyleFactory.create("Cleanlooks"))
    elif sys.platform.startswith('cygwin'):
        app.setStyle(QStyleFactory.create("Windows"))
    else:
        app.setStyle(QStyleFactory.create("GTK+"))

    ex = UI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
