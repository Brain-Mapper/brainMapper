# NAME
#
#        editCollectionsView
#
# DESCRIPTION
#
#       'editCollectionsView' contains the custom QWidget for the edition of image collections view
#
# HISTORY
#
# 3 january 2018- Initial design and coding. (@vz-chameleon, Valentina Z.)

from PyQt4 import QtGui
from PyQt4.Qt import *
from PyQt4.QtCore import pyqtSignal,QCoreApplication

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from BrainMapper import * 

import resources
import random

class InfosBar(QtGui.QWidget):
    
    styler = "border:1px solid rgb(255,255,225);"
    def __init__(self):
        super(InfosBar, self).__init__()
        self.vbox = QtGui.QVBoxLayout()
        self.group = QtGui.QGroupBox()
        self.group.setStyleSheet(self.styler)
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()
        mainwind_w = rec.width()
        self.setMaximumSize(QSize(mainwind_w, mainwind_h))
        
        self.hbox=QtGui.QHBoxLayout()
        self.hbox.addWidget(self.group)

    def redo(self,coll):
        self.hbox.removeWidget(self.group)
        self.group.setParent(None)
        self.group = QtGui.QGroupBox()
        self.group.setStyleSheet(self.styler)
        label_name = QtGui.QLabel("Collection's name : "+ str(coll.name) + str(random.randint(0,50)))
        label2_name = QtGui.QLabel("Collection's name : "+ str(coll.name) + str(random.randint(0,50)))
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(label_name)
        self.vbox.addWidget(label2_name)
        self.vbox.addStretch(1)
        self.group.setLayout(self.vbox)
        self.hbox.addWidget(self.group)
        self.setLayout(self.hbox)


class CollectionAccessButton(QtGui.QPushButton):

    styler = "CollectionAccessButton {background-color: white; border-bottom: 1px solid black;} " \
             "CollectionAccessButton:hover {background-color : #ccff99;}"

    def __init__(self, label, parent=None):
        super(CollectionAccessButton, self).__init__(label, parent=parent)
        self.setStyleSheet(self.styler)
        self.clicked.connect(lambda : self.parent().parent().parent().parent().parent().showInfos(label))


class CollectionsAccessBar(QtGui.QWidget):
    def __init__(self, labels_array, parent):
        super(CollectionsAccessBar, self).__init__(parent=parent)

        group = QtGui.QGroupBox()
        vbox = QtGui.QVBoxLayout()
        access_bar_title = QtGui.QLabel("Selected Image Collections")
        vbox.addWidget(access_bar_title)

        for lab in labels_array :
            vbox.addWidget(CollectionAccessButton(lab, self))

        vbox.addStretch(1)
        group.setLayout(vbox)

        hbox=QtGui.QHBoxLayout()
        hbox.addWidget(group)

        self.setLayout(hbox)
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()/1.4
        mainwind_w = rec.width()/1.5
        self.setMaximumSize(QSize(mainwind_w/4.5, mainwind_h))

class EditCollectionsView(QtGui.QWidget):
    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to know when to change the central view (central widget) of our app
    # In our custom widgets (like this one), buttons will emit a given signal, and the change of views will be handled
    # by the HomePage widgets' instances (see UI.py, class HomePage)

    showMain = pyqtSignal()

    def __init__(self):
        super(EditCollectionsView, self).__init__()
        self.initEditCollectionsView()

    def initEditCollectionsView(self):
        global splitter1, containerVbox
        # - Horizontal box for go back home button
        buttonsBox = QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        runClusteringButton = QtGui.QPushButton('OK')
        runClusteringButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/checking.png'))
        runClusteringButton.setToolTip("Save changes")

        goHomeButton = QtGui.QPushButton('Go back')
        goHomeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/home-2.png'))
        goHomeButton.setToolTip("Return to main page")
        goHomeButton.clicked.connect(self.go_back)  # When go back home button is clicked, change central views

        buttonsBox.addWidget(runClusteringButton)
        buttonsBox.addWidget(goHomeButton)

        hbox = QtGui.QHBoxLayout()
        bottom = QtGui.QFrame()
        bottom.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter1 = QtGui.QSplitter(Qt.Horizontal)
        topleft=CollectionsAccessBar(['1','2'],self)
        splitter1.setSizes([100, 200])
        
        self.infos = InfosBar()
        splitter1.addWidget(self.infos)
        splitter1.addWidget(topleft)
        splitter2 = QtGui.QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)

        containerVbox = QtGui.QVBoxLayout()
        containerVbox.addLayout(buttonsBox)
        containerVbox.addLayout(hbox)

        self.setLayout(containerVbox)

    def fill_coll(self):
        old = splitter1.widget(1)
        containerVbox.removeWidget(old)
        old.setParent(None)
        colls = get_selected()
        labels = []
        for x in colls:
            labels.append(x.name)
        topleft=CollectionsAccessBar(labels, self)
        splitter1.addWidget(topleft)

    def showInfos(self, name):
        col = get_selected_from_name(name)
        self.infos.redo(col)

    def go_back(self):
        self.infos = InfosBar()
        topleft=CollectionsAccessBar(['1','2'],self)
        old_info = splitter1.widget(0)
        old_left = splitter1.widget(1)
        containerVbox.removeWidget(old_info)
        containerVbox.removeWidget(old_left)
        old_info.setParent(None)
        old_left.setParent(None)
        splitter1.addWidget(self.infos)
        splitter1.addWidget(topleft)
        self.showMain.emit()
