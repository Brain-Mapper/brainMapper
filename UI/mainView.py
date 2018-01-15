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

from datetime import *
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from BrainMapper import * 
        
import resources

class CollButton(QtGui.QCheckBox):

    def __init__(self, coll, parent=None):
        super(CollButton, self).__init__(parent=parent)
        self.coll = coll
        self.toggle()
        self.stateChanged.connect(self.selectColl)

        list = self.coll.get_img_list()
        dates = []
        for l in list :
            dates.append(creation_date(str(l)))
        date = max(dates)
        d = datetime.fromtimestamp(int(round(date))).strftime('%Y-%m-%d')
        label = "Name : "+str(self.coll.name)+"\nNIfTI : "+str(len(list))+"\nLast modified : "+str(d)
        self.setText(label)
        self.setStyleSheet("CollButton {border: 1px solid black;} ")

    def selectColl(self):
        if(self.isChecked()):
            add_coll(self.coll)
        else:
            rm_coll(self.coll)

    def update(self):
        list = self.coll.get_img_list()
        dates = []
        for l in list :
            dates.append(creation_date(str(l)))
        date = max(dates)
        d = datetime.fromtimestamp(int(round(date))).strftime('%Y-%m-%d')
        self.setText("Name : "+str(self.coll.name)+"\nNIfTI : "+str(len(list))+"\nLast modified : "+str(d))
        

class CollectionsView(QtGui.QWidget):
    def __init__(self):
        self.i = 1
        self.j = 1
        super(CollectionsView, self).__init__()
        self.vbox = QtGui.QGridLayout()
        self.vbox.setAlignment(QtCore.Qt.AlignTop)
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()/1.4
        mainwind_w = rec.width()/1.5
        self.setMaximumSize(QSize(mainwind_w/0.5, mainwind_h))

        group = QtGui.QGroupBox()
        group.setLayout(self.vbox)

        scroll = QtGui.QScrollArea()
        scroll.setWidget(group)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(mainwind_h*0.8)
        
        hbox=QtGui.QHBoxLayout()
        hbox.addWidget(scroll)
        
        self.setLayout(hbox)
               
    def add(self, my_coll):
        self.vbox.addWidget(CollButton(my_coll), self.j, self.i)
        self.i +=1
        if self.i > 3:
            self.i = 1
            self.j +=1

    def update(self):
        items = (self.vbox.itemAt(j).widget() for j in range(self.vbox.count()))
        for i in items:
            if isinstance(i, QCheckBox):
                i.update()


class SetButton(QtGui.QWidget):

    styler = "SetButton {background-color: white; border-bottom: 1px solid black;} " \
             "SetButton:hover {background-color : #ccff99;}"

    def __init__(self, my_set, parent=None):
        super(SetButton, self).__init__(parent=parent)
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()/1.4
        mainwind_w = rec.width()/1.5
        self.my_set = my_set
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()
        mainwind_w = rec.width()
        
        self.setB = QtGui.QPushButton(my_set.name)
        self.setB.setStatusTip("Select this set and show the collections inside")
        self.setB.clicked.connect(self.current_set)
        self.setB.setStyleSheet(self.styler)
        self.setB.setToolTip(my_set.name)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.setB)

        SSButton = QtGui.QPushButton()
        SSButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/up-arrow.png'))
        SSButton.clicked.connect(self.addSubet)
        SSButton.setStatusTip("Add sub set")
        SSButton.setFixedSize(QSize(mainwind_w/70, mainwind_h/30))
        hbox.addWidget(SSButton)

        NameButton = QtGui.QPushButton()
        NameButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/writing.png'))
        NameButton.clicked.connect(self.changeName)
        NameButton.setStatusTip("Change Set Name")
        NameButton.setFixedSize(QSize(mainwind_w/70, mainwind_h/30))
        hbox.addWidget(NameButton)

        self.SSList = QtGui.QComboBox()
        self.SSList.setStatusTip("Show all sub sets")
        self.SSList.setFixedSize(QSize(mainwind_w/100, mainwind_h/30))
        self.SSList.activated.connect(self.test)
        hbox.addWidget(self.SSList)
        
        self.setLayout(hbox)
        self.setMaximumSize(QSize(self.parent().frameGeometry().width()*0.8, mainwind_h/8))

    def test(self):
        print self.SSList.currentText()
    def current_set(self):
        set_current_set(self.my_set)

    def addSubet(self):
        text, ok = QInputDialog.getText(self, 'Create a Sub Set', "Enter a name for your sub set of set named "+str(self.my_set.name)+":")
        if(str(text)!=""):
            try:
                new_ok = True
                not_ok = ['^','[','<','>',':',';',',','?','"','*','|','/',']','+','$']
                for i in not_ok:
                    if i in str(text):
                        new_ok = False
                if new_ok and not exists_set(str(text)):
                    self.my_set.add_empty_subset(str(text))
                    self.SSList.addItem(str(text))
                else :
                    err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid (empty, invalid caracter or already exists)")
            except :
                err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid ("+str(sys.exc_info()[0])+")")

    def changeName(self):
        text, ok = QInputDialog.getText(self, 'Rename a set', "Enter a new name for your set currently named "+str(self.my_set.name)+":")
        if(str(text)!=""):
            try:
                new_ok = True
                not_ok = ['^','[','<','>',':',';',',','?','"','*','|','/',']','+','$']
                for i in not_ok:
                    if i in str(text):
                        new_ok = False
                if new_ok and not exists_set(str(text)):
                    self.my_set.set_name(str(text))
                    size = self.setB.size()
                    self.setB.setText(str(text))
                    rec = QApplication.desktop().availableGeometry()
                    mainwind_h = rec.height()
                    mainwind_w = rec.width()
                    self.setB.setMaximumSize(size)
                else :
                    err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid (empty, invalid caracter or already exists)")
            except :
                err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid ("+str(sys.exc_info()[0])+")")


        
class SetAccessBar(QtGui.QWidget):
    def __init__(self,parent=None):
        super(SetAccessBar, self).__init__(parent=parent)
        
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()/1.4
        mainwind_w = rec.width()/1.5
        
        group = QtGui.QGroupBox()
        self.vbox = QtGui.QVBoxLayout()

        my_set = newSet("default")
        set_current_set(my_set)

        group.setLayout(self.vbox)

        scroll = QtGui.QScrollArea()
        scroll.setWidget(group)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(mainwind_h*0.8)
        
        self.vbox.addWidget(SetButton(my_set,self))
        
        hbox=QtGui.QHBoxLayout()
        hbox.addWidget(scroll)

        self.setLayout(hbox)
        self.setMaximumSize(QSize(mainwind_w/3.76, mainwind_h))
               

    def add(self, my_set):
        self.vbox.addWidget(SetButton(my_set,self))

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

        self.setAccessBox = SetAccessBar()
        self.collectionsDisplayBox = CollectionsView()
        hbox = QtGui.QHBoxLayout()

        top = QtGui.QHBoxLayout()
        top.addStretch(1)
        title_style = "QLabel { background-color : #ffcc33 ; color : black;  font-style : bold; font-size : 14px;}"
        title1 = QtGui.QLabel('\t\tList of sets\t\t')
        title1.setStyleSheet(title_style)
        title2 = QtGui.QLabel('\t\t\t\t\tList of image collections\t\t\t\t\t\t')
        title2.setStyleSheet(title_style)
        top.addWidget(title1)
        top.addWidget(title2)
        
        
        splitter1 = QtGui.QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.setAccessBox)
        splitter1.addWidget(self.collectionsDisplayBox)
        hbox.addWidget(splitter1)
        containerVbox = QtGui.QVBoxLayout()
        containerVbox.addLayout(top)
        containerVbox.addLayout(hbox)
        containerVbox.addLayout(buttonsBox)
        #self.setStyleSheet("border:1px solid rgb(255,255,225);")
        self.setLayout(containerVbox)

    def buttonClicked(self):
        print "Test passed. SUCCESS!"

    def show_coll(self, coll):
        self.collectionsDisplayBox.add(coll)
    
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

    def update(self):
        self.collectionsDisplayBox.update()
