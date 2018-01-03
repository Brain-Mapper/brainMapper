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

class MainView(QtGui.QWidget):

    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to know when to change the central view (central widget) of our app
    # In our custom widgets (like this one), buttons will emit a given signal, and the change of views will be handled
    # by the HomePage widgets' instances (see UI.py, class HomePage)
    showClust = pyqtSignal()


    # Icons dir path (ok with all os)
    path = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(path, 'ressources/app_icons_png/')

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
        collectionsDisplayBox = QtGui.QVBoxLayout()
        edit1 = QtGui.QLineEdit()
        edit2 = QtGui.QLineEdit()
        edit3 = QtGui.QTextEdit()
        coll_title = QtGui.QLabel('Set\'s Image collections')
        collectionsDisplayBox.addWidget(edit1)
        collectionsDisplayBox.addWidget(edit2)
        collectionsDisplayBox.addWidget(coll_title)
        collectionsDisplayBox.addWidget(edit3)

        # Add the previous vertical boxes to horizontal box
        middleBox.addLayout(setAccessBox)
        middleBox.addLayout(collectionsDisplayBox)

        # This horizontal Box will contain a button bar to access all other windows and functionalitites once the data
        # in image collection display has been selected
        buttonsBox = QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        # - Buttons to access other windows
        editButton = QtGui.QPushButton("Edit")
        editButton.setIcon(QtGui.QIcon(os.path.join(self.icons_dir, 'writing.png')))
        editButton.setStatusTip("Edit selected image collections")

        exportButton = QtGui.QPushButton("Export data")
        exportButton.setIcon(QtGui.QIcon(os.path.join(self.icons_dir, 'libreoffice.png')))
        exportButton.setStatusTip("Export as xlsx or NIfTI")

        clusterButton = QtGui.QPushButton("Clustering")
        clusterButton.setIcon(QtGui.QIcon(os.path.join(self.icons_dir, 'square.png')))
        clusterButton.setStatusTip("Apply clustering on selected data")
        clusterButton.clicked.connect(self.showClust.emit) # When clusterButton is clicked, change central views


        buttonsBox.addWidget(editButton)
        buttonsBox.addWidget(exportButton)
        buttonsBox.addWidget(clusterButton)

        # Set the layout of homepage widget and set it as the central widget for QtMainWindow
        containerVbox = QtGui.QVBoxLayout()
        containerVbox.addLayout(middleBox)
        containerVbox.addLayout(buttonsBox)

        self.setLayout(containerVbox)

    def buttonClicked(self):
        print "Test passed. SUCCESS!"

    def show_coll(self, coll):
        print coll
