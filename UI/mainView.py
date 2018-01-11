# NAME
#
#        mainView
#
# DESCRIPTION
#
#       'mainView' contains the Qwidget for the  main page's view
#
# HISTORY
#
# 2 january 201- Initial design and coding. (@vz-chameleon, Valentina Z.)

import os
from PyQt4 import QtGui
from PyQt4.Qt import *
from PyQt4.QtCore import pyqtSignal
from PyQt4 import QtCore

import platform
from datetime import *
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from BrainMapper import * 
        
import resources

class SetButton(QtGui.QWidget):

    styler = "SetButton {background-color: white; border-bottom: 1px solid black;} " \
             "SetButton:hover {background-color : #ccff99;}"

    def __init__(self, my_set, parent=None):
        super(SetButton, self).__init__(parent=parent)
        self.my_set = my_set
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()
        mainwind_w = rec.width()
        setB = QtGui.QPushButton(my_set.name)
        setB.setStatusTip("Select this set and show the collections inside")
        setB.clicked.connect(self.test)
        setB.setStyleSheet(self.styler)

        self.vbox = QtGui.QVBoxLayout()
        self.group = QtGui.QGroupBox()
        self.hbox=QtGui.QHBoxLayout()
        self.hbox.addWidget(self.group)

        self.vbox.addWidget(setB)

        self.group_buttons = QtGui.QGroupBox()
        self.buttons = QtGui.QHBoxLayout()
        SSButton = QtGui.QPushButton('Add')
        SSButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/up-arrow.png'))
        SSButton.setStatusTip("Add sub set")
        self.buttons.addWidget(SSButton)

        NameButton = QtGui.QPushButton('Rename')
        NameButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/writing.png'))
        NameButton.setStatusTip("Change Set Name")
        self.buttons.addWidget(NameButton)
        
        self.group_buttons.setLayout(self.buttons)
        self.vbox.addWidget(self.group_buttons)
        self.group.setLayout(self.vbox)
        
        self.hbox.addWidget(self.group)        
        self.setLayout(self.hbox)

    def test(self):
        set_current_set(self.my_set)

class SetAccessBar(QtGui.QGroupBox):
    def __init__(self, list_sets):
        super(SetAccessBar, self).__init__()
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()
        mainwind_w = rec.width()
        self.vbox = QtGui.QVBoxLayout()
        
        access_bar_title = QtGui.QLabel("List of sets")
        
        self.vbox.addWidget(access_bar_title)
        for lab in list_sets :
            self.vbox.addWidget(SetButton(lab))

        self.setLayout(self.vbox)
    def add(self, my_set):
        self.vbox.addWidget(SetButton(my_set))

class MainView(QtGui.QWidget):

    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to know when to change the central view (central widget) of our app
    # In our custom widgets (like this one), buttons will emit a given signal, and the change of views will be handled
    # by the HomePage widgets' instances (see UI.py, class HomePage)
    showClust = pyqtSignal()
    showEdit = pyqtSignal()

    def __init__(self):
        super(MainView, self).__init__()

        self.initMainView()

    def initMainView(self):
        # This horizontal Box will contain two vertical boxes, one for the set access bar and another for image collec
        # tions display
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()
        mainwind_w = rec.width()
        
        middleBox = QtGui.QHBoxLayout()

        # - Vertical box for sets layout
        self.setAccessBox = SetAccessBar([newSet("default_set")])

        scroll = QtGui.QScrollArea()
        scroll.setWidget(self.setAccessBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(mainwind_h*0.6)
        scroll.setFixedWidth(mainwind_w*0.12)
        #scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # - Vertical box for image collections display
        global collectionsDisplayBox
        collectionsDisplayBox = QtGui.QVBoxLayout()
        edit1 = QtGui.QLineEdit()
        collectionsDisplayBox.addWidget(edit1)
        collectionsDisplayBox.addStretch(0)
        collectionsDisplayBox.setSizeConstraint(QtGui.QLayout.SetMaximumSize)

        # Add the previous vertical boxes to horizontal box
        middleBox.addWidget(scroll)
        middleBox.addLayout(collectionsDisplayBox)

        # This horizontal Box will contain a button bar to access all other windows and functionalitites once the data
        # in image collection display has been selected
        buttonsBox = QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        # - Buttons to access other windows
        editButton = QtGui.QPushButton("Edit")
        editButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/writing.png'))
        editButton.setStatusTip("Edit selected image collections")
        editButton.clicked.connect(self.edit_pannel)

        exportButton = QtGui.QPushButton("Export data")
        exportButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/libreoffice.png'))
        exportButton.setStatusTip("Export as xlsx or NIfTI")
        exportButton.clicked.connect(self.export)

        calcButton = QtGui.QPushButton("Calculations")
        calcButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/calculator.png'))
        calcButton.setStatusTip("Perform calculations on selected data")

        clusterButton = QtGui.QPushButton("Clustering")
        clusterButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/square.png'))
        clusterButton.setStatusTip("Apply clustering on selected data")
        clusterButton.clicked.connect(self.extract_and_cluster) # When clusterButton is clicked, change central views


        buttonsBox.addWidget(editButton)
        buttonsBox.addWidget(exportButton)
        buttonsBox.addWidget(calcButton)
        buttonsBox.addWidget(clusterButton)

        # Set the layout of homepage widget and set it as the central widget for QtMainWindow
        containerVbox = QtGui.QVBoxLayout()
        containerVbox.addLayout(middleBox)
        containerVbox.addLayout(buttonsBox)
        
        
        self.setStyleSheet("border:1px solid rgb(255,255,225);")

        self.setLayout(containerVbox)

    def buttonClicked(self):
        print "Test passed. SUCCESS!"

    def show_coll(self, coll):
        list = coll.get_img_list()
        dates = []
        for l in list :
            dates.append(self.creation_date(str(l)))
        date = max(dates)
        d = datetime.fromtimestamp(int(round(date))).strftime('%Y-%m-%d')
        label = "Patient : "+str(coll.name)+"\nNIfTI : "+str(len(list))+"\nLast modified : "+str(d)
        cb = QtGui.QCheckBox(label, self)
        cb.toggle()
        cb.stateChanged.connect(lambda : self.selectColl(cb, coll))
        collectionsDisplayBox.addWidget(cb)
        collectionsDisplayBox.addStretch(0)
        collectionsDisplayBox.setSizeConstraint(QtGui.QLayout.SetFixedSize)

    def selectColl(self, cb, coll):
        if(cb.isChecked()):
            add_coll(coll)
        else:
            rm_coll(coll)

    def creation_date(self,path_to_file):
        if platform.system() == 'Windows':
            return os.path.getctime(path_to_file)
        else:
            stat = os.stat(path_to_file)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux.
                return stat.st_mtime
            
    def export(self):
        if(get_selected()):
            choice = QtGui.QMessageBox.question(self, 'Export selected files',
                                                "Export into a NIfTI file? (if No : Excel file)",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:
                export_nifti()
            else:
                export_excel()
        else:
            QtGui.QMessageBox.information(self, "Selection empty","There's nothing to export.")

    def extract_and_cluster(self):
        if(get_selected()):
            choice = QtGui.QMessageBox.question(self, 'Extract data for clustering',
                                                "You have selected (" + str(len(get_selected())) +") image collections \n Confirm to extract data",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:
                extract_data_from_selected()
                self.showClust.emit()
        else:
            QtGui.QMessageBox.information(self, "Selection empty", "There's no data to extract and clusterize.")


    def edit_pannel(self):
        if(get_selected()):
            self.showEdit.emit()
        else:
            QtGui.QMessageBox.information(self, "Selection empty", "There's no data to edit.")

    def show_set(self, new_set):
        self.setAccessBox.add(new_set)
