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
import platform
from datetime import *
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from BrainMapper import * 
        
import resources

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
        middleBox = QtGui.QHBoxLayout()

        # - Vertical box for sets layout
        setAccessBox = QtGui.QVBoxLayout()

        # BUTTONS (SET ACCESS)
        btnNS = QtGui.QPushButton('Set 1 : Speech', self)
        btnNS.setStatusTip('Set 1 : Speech')
        btnNS.setFixedWidth(150)
        btnNS.clicked.connect(self.buttonClicked)  # Action for button

        setAccessBox.addWidget(btnNS, 0, Qt.AlignTop)

        # - Vertical box for image collections display
        global collectionsDisplayBox
        collectionsDisplayBox = QtGui.QVBoxLayout()
        edit1 = QtGui.QLineEdit()
        #edit2 = QtGui.QLineEdit()
        #coll_title = QtGui.QLabel('Set\'s Image collections')
        collectionsDisplayBox.addWidget(edit1)
        #collectionsDisplayBox.addWidget(edit2)
        #collectionsDisplayBox.addWidget(coll_title)
        collectionsDisplayBox.addStretch(0)
        collectionsDisplayBox.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        # Add the previous vertical boxes to horizontal box
        middleBox.addLayout(setAccessBox)
        middleBox.addLayout(collectionsDisplayBox)

        # This horizontal Box will contain a button bar to access all other windows and functionalitites once the data
        # in image collection display has been selected
        buttonsBox = QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        # - Buttons to access other windows
        editButton = QtGui.QPushButton("Edit")
        editButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/writing.png'))
        editButton.setStatusTip("Edit selected image collections")
        editButton.clicked.connect(self.showEdit.emit)

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
        clusterButton.clicked.connect(self.showClust.emit) # When clusterButton is clicked, change central views


        buttonsBox.addWidget(editButton)
        buttonsBox.addWidget(exportButton)
        buttonsBox.addWidget(calcButton)
        buttonsBox.addWidget(clusterButton)

        # Set the layout of homepage widget and set it as the central widget for QtMainWindow
        containerVbox = QtGui.QVBoxLayout()
        containerVbox.addLayout(middleBox)
        containerVbox.addLayout(buttonsBox)

        self.setLayout(containerVbox)

    def buttonClicked(self):
        print "Test passed. SUCCESS!"

    def show_coll(self, coll):
        list = coll.get_img_list()
        dates = []
        for l in list :
            dates.append(self.creation_date(str(l.filename)))
        date = max(dates)
        d = datetime.fromtimestamp(int(round(date))).strftime('%Y-%m-%d')
        label = "Patient : \nNIfTI : "+str(len(list))+"\nLast modified : "+str(d)
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
