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

class ImageBar(QtGui.QWidget):
    #styler = "border:1px solid rgb(255,255,225);"
    def __init__(self, im):
        super(ImageBar, self).__init__()
        filname = im.filename.split("/")
        filna = filname[len(filname)-1]
        self.label = QtGui.QLabel("   "+filna)
        self.label.setToolTip(im.filename)
        self.label.setFixedWidth(420)

        self.removeButton = QtGui.QPushButton("Remove")
        self.removeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/trash.png'))
        self.removeButton.setStatusTip("Remove image from collection")
        self.removeButton.clicked.connect(self.remove)
        self.removeButton.setFixedWidth(110)

        showButton = QtGui.QPushButton("Show")
        showButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/eye.png'))
        showButton.setStatusTip("Show image")
        showButton.clicked.connect(self.show)
        showButton.setFixedWidth(110)

        hbox=QtGui.QHBoxLayout()
        hbox.addWidget(self.label)
        hbox.addWidget(self.removeButton)
        hbox.addWidget(showButton)
        self.setLayout(hbox)
        #self.setStyleSheet(self.styler)

    def remove(self):
        self.label.setStyleSheet('color : red')
        self.removeButton.setText("Re Add")
        self.removeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/curve-arrow.png'))
        self.removeButton.setStatusTip("Re add image into collection")
        self.removeButton.clicked.connect(self.readd)

    def readd(self):
        self.label.setStyleSheet('')
        self.removeButton.setText("Remove")
        self.removeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/trash.png'))
        self.removeButton.setStatusTip("Remove image from collection")
        self.removeButton.clicked.connect(self.remove)
        
        
class InfosBar(QtGui.QWidget):
    def __init__(self):
        super(InfosBar, self).__init__()
        self.vbox = QtGui.QVBoxLayout()
        self.group = QtGui.QGroupBox()
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()
        mainwind_w = rec.width()
        self.setMaximumSize(QSize(mainwind_w, mainwind_h))
        
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidget(self.group)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(220)
        
        self.hbox=QtGui.QHBoxLayout()
        self.hbox.addWidget(self.scroll)
        

    def redo(self,coll):
        self.hbox.removeWidget(self.scroll)
        self.scroll.setParent(None)
        self.scroll = QtGui.QScrollArea()
        self.group = QtGui.QGroupBox()
        self.vbox = QtGui.QVBoxLayout()
        label_name = QtGui.QLabel("Collection's name : "+ str(coll.name))
        list_images = "List of images :"
        label2_name = QtGui.QLabel(list_images)
        self.vbox.addWidget(label_name)
        self.vbox.addWidget(label2_name)
        for i in coll.get_img_list().values():
            im = ImageBar(i)
            self.vbox.addWidget(im)
        self.vbox.addStretch(1)
        self.group.setLayout(self.vbox)
        
        self.scroll.setWidget(self.group)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(220)
        self.hbox.addWidget(self.scroll)
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
