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
from PyQt4 import QtCore

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from BrainMapper import *

import pyqtgraph as pg

import resources
import re

class ImageBar(QtGui.QWidget):
    #styler = "border:1px solid rgb(255,255,225);"
    def __init__(self, im, parent = None):
        super(ImageBar, self).__init__(parent = parent)
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()
        self.im = im
        filname = im.filename.split("/")
        filna = filname[len(filname)-1]
        self.label = QtGui.QLabel("   "+filna)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.label.setToolTip(im.filename)
        self.label.setFixedWidth(420)

        self.removeButton = QtGui.QPushButton("Remove")
        self.removeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/trash.png'))
        self.removeButton.setStatusTip("Remove image from collection")
        self.removeButton.clicked.connect(self.do)
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
        add_toRM(self.im)
        self.label.setStyleSheet('color : red')
        self.removeButton.setText("Re Add")
        self.removeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/curve-arrow.png'))
        self.removeButton.setStatusTip("Re add image into collection")

    def readd(self):
        rm_toRM(self.im)
        self.label.setStyleSheet('')
        self.removeButton.setText("Remove")
        self.removeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/trash.png'))
        self.removeButton.setStatusTip("Remove image from collection")

    def do(self):
        if(self.removeButton.text() == "Remove"):
            self.remove()
        else:
            self.readd()

    def show(self):
        self.parent().parent().parent().parent().parent().parent().parent().parent().parent().updateVizuView()
                
        
class InfosBar(QtGui.QWidget):
    def __init__(self, parent = None):
        super(InfosBar, self).__init__(parent = parent)
        self.vbox = QtGui.QVBoxLayout()
        self.group = QtGui.QGroupBox()
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()
        mainwind_w = rec.width()
        self.setMaximumSize(QSize(mainwind_w, mainwind_h))
        
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidget(self.group)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(mainwind_h*0.5)
        
        self.hbox=QtGui.QHBoxLayout()
        self.hbox.addWidget(self.scroll)
        

    def redo(self,coll):
        if coll != None :
            set_current_coll(coll)
            self.hbox.removeWidget(self.scroll)
            self.scroll.setParent(None)
            self.scroll = QtGui.QScrollArea()
            self.group = QtGui.QGroupBox()
            self.vbox = QtGui.QVBoxLayout()
            label_name = QtGui.QLabel("Collection's name : "+ str(coll.name))
            label_name.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
            label_set = QtGui.QLabel("Set's name \t : "+ str(coll.set_n.name))
            label_set.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
            list_images = "List of images :"
            label2_name = QtGui.QLabel(list_images)
            self.vbox.addWidget(label_name)
            self.vbox.addWidget(label_set)
            self.vbox.addWidget(label2_name)
            for i in coll.get_img_list().values():
                im = ImageBar(i)
                self.vbox.addWidget(im)
            self.vbox.addStretch(1)

            self.group_buttons = QtGui.QGroupBox()
            self.buttons = QtGui.QHBoxLayout()
            OKButton = QtGui.QPushButton('Save Changes')
            OKButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/checking.png'))
            OKButton.setStatusTip("Save changes")
            OKButton.clicked.connect(self.save)
            self.buttons.addWidget(OKButton)

            NameButton = QtGui.QPushButton('Change Collection Name')
            NameButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/writing.png'))
            NameButton.setStatusTip("Change Collection Name")
            NameButton.clicked.connect(self.changeName)
            self.buttons.addWidget(NameButton)

            AddButton = QtGui.QPushButton('Add new Image(s)')
            AddButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/up-arrow.png'))
            AddButton.setStatusTip("Add some new images in the current collection")
            AddButton.clicked.connect(lambda : self.addImage(coll))
            self.buttons.addWidget(AddButton)

            RmButton = QtGui.QPushButton('Delete Collection')
            RmButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/trash.png'))
            RmButton.setStatusTip("Delete the current collection")
            RmButton.clicked.connect(lambda : self.del_col(coll))
            self.buttons.addWidget(RmButton)

            self.group_buttons.setLayout(self.buttons)
            self.vbox.addWidget(self.group_buttons)
            self.group.setLayout(self.vbox)
            
            self.scroll.setWidget(self.group)
            self.scroll.setWidgetResizable(True)
            self.scroll.setFixedHeight(self.parent().frameGeometry().height()*0.9)
            self.hbox.addWidget(self.scroll)
            self.setLayout(self.hbox)
        else:
            self.hbox.removeWidget(self.scroll)
            self.scroll.setParent(None)
            self.scroll = QtGui.QScrollArea()
            self.group = QtGui.QGroupBox()
            self.vbox = QtGui.QVBoxLayout()
            self.scroll.setWidgetResizable(True)
            self.scroll.setFixedHeight(self.parent().frameGeometry().height()*0.9)
            self.hbox.addWidget(self.scroll)
            self.setLayout(self.hbox)

    def addImage(self, coll):
        path = QFileDialog.getOpenFileNames()
        if (path != ""):
            try:
                add_image_coll(coll,path)
                self.redo(get_current_coll())
            except:
                err = QtGui.QMessageBox.critical(self, "Error", "An error has occured. Maybe you tried to open a non-NIfTI file")
                print (sys.exc_info()[0])
        

    def save(self):
        if(len(get_toRM())>0):
            choice = QtGui.QMessageBox.question(self, 'Save changes',
                                                "Are you sure you want to save your modifications? This is irreversible.",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:
                save_modifs()
                self.redo(get_current_coll())
        else:
            info = QtGui.QMessageBox.information(self, "Info", "There's nothing to save!")

    def changeName(self):
        text, ok = QInputDialog.getText(self, 'Change name of the Collection', "Enter a new name for the collection named "+ get_current_coll().name +": ")
        if str(text) != "":
            try:
                new_ok = True
                not_ok = ['^','[','<','>',':',';',',','?','"','*','|','/',']','+','$']
                for i in not_ok:
                    if i in str(text):
                        new_ok = False
                if new_ok and not exists_coll_in_sets(str(text)):
                    setColNameInSet(str(text))
                    cur_col = get_current_coll()
                    self.redo(cur_col)
                    self.parent().parent().parent().parent().parent().fill_coll()
                else :
                    err = QtGui.QMessageBox.critical(self, "Error", "The new name you entered is not valid (empty, invalid caracter or already exists)")
            except :
                err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid ("+str(sys.exc_info()[0])+")")
            
    def del_col(self,coll):
        choice = QtGui.QMessageBox.question(self, 'Delete Collection',
                                                "Are you sure you want to delete this collection?",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            delete_current_coll()
            self.redo(None)
            self.parent().parent().parent().parent().parent().showMain.emit()
            

class CollectionAccessButton(QtGui.QPushButton):

    styler = "CollectionAccessButton {background-color: white; border-bottom: 1px solid black;} " \
             "CollectionAccessButton:hover {background-color : #ccff99;}"

    def __init__(self, label, parent=None):
        super(CollectionAccessButton, self).__init__(label, parent=parent)
        self.setStyleSheet(self.styler)
        self.clicked.connect(lambda : self.parent().parent().parent().parent().parent().parent().parent().showInfos(label,self))


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

        goHomeButton = QtGui.QPushButton('Go back')
        goHomeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/home-2.png'))
        goHomeButton.setStatusTip("Return to main page")
        goHomeButton.clicked.connect(self.go_back)  # When go back home button is clicked, change central views

        buttonsBox.addWidget(goHomeButton)

        hbox = QtGui.QHBoxLayout()
        self.bottom = pg.GraphicsLayoutWidget()

        splitter1 = QtGui.QSplitter(Qt.Horizontal)
        topleft=CollectionsAccessBar(['1','2'],self)

        scroll = QtGui.QScrollArea()
        scroll.setWidget(splitter1)
        scroll.setWidgetResizable(True)
        
        self.infos = InfosBar()
        splitter1.addWidget(self.infos)
        splitter1.addWidget(topleft)
        splitter2 = QtGui.QSplitter(Qt.Vertical)


        splitter2.addWidget(scroll)
        splitter2.addWidget(self.bottom)
        splitter2.setSizes([self.frameGeometry().height()*0.65, self.frameGeometry().height()*0.35])

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

    def showInfos(self, name, button):
        reset_toRM()
        col = get_selected_from_name(name)
        set_current_coll(col)
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
        reset_toRM()
        self.showMain.emit()

    def updateVizuView(self):
        p = self.bottom.addPlot(row=0, col=0)
        p2 = self.bottom.addPlot(row=1, col=0)

        ## variety of arrow shapes
        a1 = pg.ArrowItem(angle=-160, tipAngle=60, headLen=40, tailLen=40, tailWidth=20, pen={'color': 'w', 'width': 3})
        a2 = pg.ArrowItem(angle=-120, tipAngle=30, baseAngle=20, headLen=40, tailLen=40, tailWidth=8, pen=None, brush='y')
        a3 = pg.ArrowItem(angle=-60, tipAngle=30, baseAngle=20, headLen=40, tailLen=None, brush=None)
        a4 = pg.ArrowItem(angle=-20, tipAngle=30, baseAngle=-30, headLen=40, tailLen=None)
        a2.setPos(10,0)
        a3.setPos(20,0)
        a4.setPos(30,0)
        p.addItem(a1)
        p.addItem(a2)
        p.addItem(a3)
        p.addItem(a4)
        p.setRange(QtCore.QRectF(-20, -10, 60, 20))
