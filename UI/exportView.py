# NAME
#
#        exportView
#
# DESCRIPTION
#
#       'exportView' contains the Qwidget for the export view
#
# HISTORY
#
# 15 january 2018 - Initial design and coding. (@yoshcraft, Raphael A.)
# 16 january 2018 - Basing graphic interface and add export csv method (@yoshcraft, Raphael A.)
# 18 january 2018 - Modification to fit with the new export method (@yoshcraft, Raphael A.)
# 13 february 2018 - Useless, cause of some modification of the csv exporting method, in waiting of the nifti
#  export implementation




from PyQt4 import QtGui
from PyQt4.Qt import *
from PyQt4.QtCore import pyqtSignal,QCoreApplication
from PyQt4 import QtCore

import sys
import os
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import ourLib.ExcelExport.excelExport as ee


class ExportView(QtGui.QWidget):
    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to know when to change the central view (central widget) of our app
    # In our custom widgets (like this one), buttons will emit a given signal, and the change of views will be handled
    # by the HomePage widgets' instances (see UI.py, class HomePage)

    showMain = pyqtSignal()

    def __init__(self):
        self.export_usable_dataset = None
        super(ExportView, self).__init__()

        self.initExportView()

    def initExportView(self):
        # global containerVbox
        # # - Horizontal box for go back home button
        # buttonsBox = QtGui.QHBoxLayout()
        # buttonsBox.addStretch(1)
        #
        # goHomeButton = QtGui.QPushButton('Go back')
        # goHomeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/home-2.png'))
        # goHomeButton.setStatusTip("Return to main page")
        # goHomeButton.clicked.connect(self.showMain.emit)  # When go back home button is clicked, change central views
        #
        #
        #
        # runExportButton = QtGui.QPushButton('Run')
        # runExportButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/play.png'))
        # runExportButton.setToolTip("Run the export")
        # runExportButton.clicked.connect(lambda: self.export('test', 'test'))
        #
        # buttonsBox.addWidget(runExportButton)
        # buttonsBox.addWidget(goHomeButton)
        #
        # hbox = QtGui.QHBoxLayout()
        # bottom = QtGui.QFrame()
        # bottom.setFrameShape(QtGui.QFrame.StyledPanel)
        #
        # containerVbox = QtGui.QVBoxLayout()
        # containerVbox.addLayout(buttonsBox)
        # containerVbox.addLayout(hbox)
        #
        # self.setLayout(containerVbox)

        filename = QtGui.QLabel('File name')
        directory = QtGui.QLabel('Directory')

        self.fileNameEdit = QtGui.QLineEdit('')
        self.directoryEdit = QtGui.QLineEdit('')

        goHomeButton = QtGui.QPushButton('Go back')
        goHomeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/home-2.png'))
        goHomeButton.setStatusTip("Return to main page")
        goHomeButton.clicked.connect(self.showMain.emit)  # When go back home button is clicked, change central views

        runExportButton = QtGui.QPushButton('Run')
        runExportButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/play.png'))
        runExportButton.setStatusTip("Run the export")
        runExportButton.clicked.connect(lambda: ee.simple_export(self.fileNameEdit.text(), self.directoryEdit.text(), self.export_usable_dataset))

        selectButton = QtGui.QPushButton('browse')
        selectButton.clicked.connect(lambda: self.select_directory())

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(goHomeButton, 1, 2)
        grid.addWidget(filename, 2, 0)
        grid.addWidget(self.fileNameEdit, 2, 1)
        grid.addWidget(directory, 3, 0)
        grid.addWidget(self.directoryEdit, 3, 1)
        grid.addWidget(selectButton, 3, 2)
        grid.addWidget(runExportButton, 4, 2)

        self.setLayout(grid)
        self.show()

    def select_directory(self):
        """
        Open a browser to select a directory path and put the result into directoryEdit
        """
        file = str(QFileDialog.getExistingDirectory(self, "Browse Directory"))
        self.directoryEdit.setText(file)

    def set_usable_data_set(self,a_usable_dataset_instance):
        self.export_usable_dataset = a_usable_dataset_instance












