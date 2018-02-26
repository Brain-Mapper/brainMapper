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
# 14 january 2018 - Began the interface (@Graziella-Husson)
# 15-16 january 2018 - Redo all the interface (@Graziella-Husson)
# 30 january 2018 - Added tabs to interface for results of calculation and clustering (@Graziella-Husson)
# 13 february 2018 - Change of the way of exporting a to CSV (@yoshcraft, Raphael A.)

from PyQt4 import QtGui
from PyQt4.Qt import *
from PyQt4.QtCore import pyqtSignal
from PyQt4 import QtCore

from datetime import *
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from BrainMapper import *
import resources
import ourLib.ExcelExport.excelExport as ee
import time
from ourLib.dataExtraction.image_recreation import *


class CollButton(QtGui.QCheckBox):
    # -- The CollButton class is a QCheckBox that show all collection info

    def __init__(self, coll, parent=None):
        super(CollButton, self).__init__(parent=parent)
        self.coll = coll
        self.toggle()
        self.stateChanged.connect(self.selectColl)

        list = self.coll.get_img_list()

        try :
            dates = []
            for l in list :
                dates.append(creation_date(str(l)))
            date = max(dates)
            d = datetime.fromtimestamp(int(round(date))).strftime('%Y-%m-%d')
        except :
            d = datetime.fromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d')
        label = "Name : "+str(self.coll.name)+"\nNIfTI : "+str(len(list))+"\nLast modified : "+str(d)
        self.setText(label)
        self.setStyleSheet("CollButton {background-color : #eee; spacing: 5px;border: 2px solid #99cccc;border-radius: 8px;padding: 1px 18px 1px 3px;max-width: 225%;}; CollButton::indicator {width: 13px; height: 13px;};")

    def selectColl(self):
        # -- This selectColl will add or delete the collection from the selected ones
        if (self.isChecked()):
            add_coll(self.coll)
        else:
            rm_coll(self.coll)

    def update(self):
        # -- This update will update the information of the collection if they have changed in the edit collection view
        list = self.coll.get_img_list()
        try:
            if list :
                dates = []
                for l in list :
                    dates.append(creation_date(str(l)))
                date = max(dates)
                d = datetime.fromtimestamp(int(round(date))).strftime('%Y-%m-%d')
            else :
                d = datetime.fromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d')
        except:
            d = datetime.fromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d')
        self.setText("Name : "+str(self.coll.name)+"\nNIfTI : "+str(len(list))+"\nLast modified : "+str(d))


class CollectionsView(QtGui.QWidget):
    # -- The CollectionsView class will display all the collections in the current set
    def __init__(self, label):

        self.i = 1
        self.j = 1
        super(CollectionsView, self).__init__()

        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height() / 1.4
        mainwind_w = rec.width() / 1.5
        self.setMinimumSize(QSize(mainwind_w / 1.35, mainwind_h * 0.9))
        self.max = int((mainwind_w / 1.35)/150)
        print self.max

        buttonsBox = QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        deselectButton = QtGui.QPushButton("Deselect all")
        deselectButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/circle.png'))
        deselectButton.clicked.connect(self.deselectAll)
        deselectButton.setStatusTip("Deselect all Image Collections in THIS set")
        deselectButton.setFixedSize(QSize(mainwind_w / 8, mainwind_h / 20))
        buttonsBox.addWidget(deselectButton,0, Qt.AlignRight)

        selectButton = QtGui.QPushButton("Select all")
        selectButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/checking.png'))
        selectButton.clicked.connect(self.selectAll)
        selectButton.setStatusTip("Select all Image Collections in THIS set")
        selectButton.setFixedSize(QSize(mainwind_w / 8, mainwind_h / 20))
        buttonsBox.addWidget(selectButton,0, Qt.AlignRight)

        self.name = label
        set_current_vizu(self)

        title_style = "QLabel { background-color : #ffcc33 ; color : black;  font-style : bold; font-size : 14px;}"
        self.title2 = QtGui.QLabel("List of image collections for set " + str(self.name))
        self.title2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.title2.setMinimumWidth(self.width())
        self.title2.setFixedHeight(20)
        self.title2.setAlignment(QtCore.Qt.AlignCenter)
        self.title2.setStyleSheet(title_style)
        
        self.vbox = QtGui.QGridLayout()
        self.vbox.setAlignment(QtCore.Qt.AlignTop)

        group = QtGui.QGroupBox()
        group.setLayout(self.vbox)

        scroll = QtGui.QScrollArea()
        scroll.setWidget(group)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(mainwind_h * 0.8)

        hbox = QtGui.QVBoxLayout()
        hbox.addWidget(self.title2)
        hbox.addLayout(buttonsBox)
        hbox.addWidget(scroll)

        self.setLayout(hbox)


    def add(self, my_coll):
        # -- This add will add a collection to vizualize according to the grid 3 x X where X is unlimited thanks to the scroll bar
        self.vbox.addWidget(CollButton(my_coll), self.j, self.i)
        self.i += 1
        if self.i > self.max:
            self.i = 1
            self.j += 1

    def update(self):
        # -- This update will update the collection view and deleted the ones that have to be deleted
        items = (self.vbox.itemAt(j).widget() for j in range(self.vbox.count()))
        for i in items:
            if isinstance(i, QCheckBox):
                tRM = get_toRM()
                if tRM:  # List not empty
                    coll_to_RM = tRM[0]
                    if (i.coll == coll_to_RM):
                        print i.coll
                        i.setParent(None)
                        del i
                    else:
                        i.update()
                else:
                    i.update()

    def update_label(self, label):
        # -- This update_label will update only the label at the top of the screen with the current set name
        self.name = label
        self.title2.setText("List of image collections for set " + str(label))

    def deselectAll(self):
        items = (self.vbox.itemAt(j).widget() for j in range(self.vbox.count()))
        for i in items:
            if isinstance(i, QCheckBox):
                if (i.isChecked()):
                    i.toggle()
                    rm_coll(i.coll)

    def selectAll(self):
        items = (self.vbox.itemAt(j).widget() for j in range(self.vbox.count()))
        for i in items:
            if isinstance(i, QCheckBox):
                if not (i.isChecked()):
                    i.toggle()
                    add_coll(i.coll)   

class SetButton(QtGui.QWidget):
    # -- The SetButton class will display all info for a set

    styler = "SetButton {background-color: white; border-bottom: 1px solid black;} " \
             "SetButton:hover {background-color : #ccff99;}"

    def __init__(self, my_set, parent=None):
        # -- Will create all objects we need
        super(SetButton, self).__init__(parent=parent)
        self.vizu = CollectionsView(my_set.name)
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
        SSButton.setFixedSize(QSize(mainwind_w / 70, mainwind_h / 30))
        hbox.addWidget(SSButton)

        NameButton = QtGui.QPushButton()
        NameButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/writing.png'))
        NameButton.clicked.connect(self.changeName)
        NameButton.setStatusTip("Change Set Name")
        NameButton.setFixedSize(QSize(mainwind_w / 70, mainwind_h / 30))
        hbox.addWidget(NameButton)

        self.SSList = QtGui.QComboBox()
        self.SSList.setStatusTip("Show all sub sets")
        self.SSList.setFixedSize(QSize(mainwind_w / 100, mainwind_h / 30))
        self.SSList.activated.connect(self.showSubSet)
        hbox.addWidget(self.SSList)

        self.setLayout(hbox)
        self.setFixedSize(QSize(self.parent().frameGeometry().width() * 0.8, mainwind_h / 8))

    def showSubSet(self):
        # -- When we click on an item in the list of subset, we update current vizu and set
        new_set = getSetByName(self.SSList.currentText())
        set_current_set(new_set)
        self.parent().parent().parent().parent().parent().parent().parent().updateSet(new_set)

    def updateSubSetName(self):
        # -- Update the list of subsets shown. Usefull when a sub set is renamed
        self.SSList.clear()
        SSets = self.my_set.getAllSubSets()
        for i in SSets:
            self.SSList.addItem(str(i.get_name()))

    def current_set(self):
        # -- This current_set will vizualize the set and the collections inside when pressed
        set_current_set(self.my_set)
        set_current_vizu(self.vizu)
        self.parent().parent().parent().parent().parent().parent().parent().parent().parent().updateVizu(self.vizu)
        self.parent().parent().parent().parent().parent().parent().parent().parent().parent().upCollLabel()

    def addSubet(self):
        # -- This addSubet will add a subset to the set selected. 
        text, ok = QInputDialog.getText(self, 'Create a Sub Set',
                                        "Enter a name for your sub set of set named " + str(self.my_set.name) + ":")
        if (str(text) != ""):
            try:
                new_ok = True
                not_ok = ['^', '[', '<', '>', ':', ';', ',', '?', '"', '*', '|', '/', ']', '+', '$']
                for i in not_ok:
                    if i in str(text):
                        new_ok = False
                if new_ok and not exists_set(str(text)):
                    self.my_set.add_empty_subset(str(text))
                    self.SSList.addItem(str(text))
                    ssSet = self.my_set.get_sub_set(str(text))
                    self.my_set.get_sub_set(str(text)).setParent(self.my_set)
                    add_set(ssSet)
                    set_current_set(ssSet)
                    self.parent().parent().parent().parent().parent().parent().parent().add(ssSet)
                else :
                    err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid (empty, invalid caracter or already exists)")
            except :
                err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid ("+str(sys.exc_info()[0])+")")

    def addFullSubSet(self,ssSet):
        text = ssSet.get_name()
        self.SSList.addItem(str(text))
        self.my_set.get_sub_set(str(text)).setParent(self.my_set)
        add_set(ssSet)


    def changeName(self):
        # -- This changeName will change the name of the set selected. 
        text, ok = QInputDialog.getText(self, 'Rename a set',
                                        "Enter a new name for your set currently named " + str(self.my_set.name) + ":")
        if (str(text) != ""):
            try:
                new_ok = True
                not_ok = ['^', '[', '<', '>', ':', ';', ',', '?', '"', '*', '|', '/', ']', '+', '$']
                for i in not_ok:
                    if i in str(text):
                        new_ok = False
                if new_ok and not exists_set(str(text)):
                    rm_set(self.my_set)
                    if(self.my_set.getParent() != None): #if its a subset
                        self.my_set.getParent().remove_subset(self.my_set.get_name())
                        self.my_set.set_name(str(text))
                        self.my_set.getParent().add_subset(self.my_set)
                    else:
                        self.my_set.set_name(str(text))
                    size = self.setB.size()
                    self.setB.setText(str(text))
                    rec = QApplication.desktop().availableGeometry()
                    mainwind_h = rec.height()
                    mainwind_w = rec.width()
                    self.setB.setMaximumSize(size)
                    add_set(self.my_set)
                    self.parent().parent().parent().parent().parent().parent().update()
                else :
                    err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid (empty, invalid caracter or already exists)")
            except :
                err = QtGui.QMessageBox.critical(self, "Error", "The name you entered is not valid ("+str(sys.exc_info()[0])+")")


class SetAccessBar(QtGui.QWidget):
    # -- The SetAccessBar class will display all sets created
    def __init__(self, parent=None):
        # -- Creates all abjects we need
        super(SetAccessBar, self).__init__(parent=parent)

        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height() / 1.4
        mainwind_w = rec.width() / 1.5
        
        self.qtab = QtGui.QTabWidget()
        self.qtab.tab1 = QWidget()
        self.qtab.tab1.setMaximumSize(QSize(mainwind_w / 3.76, mainwind_h))
        self.qtab.addTab(self.qtab.tab1, "Tab 1")
        self.qtab.setTabText(0, "All")
        self.qtab.tab2 = QWidget()
        self.qtab.tab2.setMaximumSize(QSize(mainwind_w / 3.76, mainwind_h))
        self.qtab.addTab(self.qtab.tab2, "Tab 2")
        self.qtab.setTabText(1, "Clustering")
        self.qtab.tab3 = QWidget()
        self.qtab.tab3.setMaximumSize(QSize(mainwind_w / 3.76, mainwind_h))
        self.qtab.addTab(self.qtab.tab3, "Tab 3")
        self.qtab.setTabText(2, "Calculation")

        
        self.setMaximumSize(QSize(mainwind_w / 3.76, mainwind_h))

        buttonsBox = QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        deselectButton = QtGui.QPushButton("Deselect all")
        deselectButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/circle.png'))
        deselectButton.clicked.connect(self.deselectAll)
        deselectButton.setStatusTip("Deselect all Image Collections in ALL sets")
        deselectButton.setFixedSize(QSize(mainwind_w / 8, mainwind_h / 20))
        buttonsBox.addWidget(deselectButton,0, Qt.AlignRight)

        selectButton = QtGui.QPushButton("Select all")
        selectButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/checking.png'))
        selectButton.clicked.connect(self.selectAll)
        selectButton.setStatusTip("Select all Image Collections in ALL sets")
        selectButton.setFixedSize(QSize(mainwind_w / 8, mainwind_h / 20))
        buttonsBox.addWidget(selectButton,0, Qt.AlignRight)

        group = QtGui.QGroupBox()
        group2 = QtGui.QGroupBox()
        group3 = QtGui.QGroupBox()
        self.qtab.tab1.vbox = QtGui.QVBoxLayout()
        self.qtab.tab2.vbox2 = QtGui.QVBoxLayout()
        self.qtab.tab3.vbox3 = QtGui.QVBoxLayout()

        default_name = datetime.fromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d %H:%M:%S')
        
        my_set = newSet(default_name[2:])
        set_current_set(my_set)

        group.setLayout(self.qtab.tab1.vbox)
        group2.setLayout(self.qtab.tab2.vbox2)
        group3.setLayout(self.qtab.tab3.vbox3)

        scroll = QtGui.QScrollArea()
        scroll.setWidget(group)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(mainwind_h*0.8)
        
        scroll2 = QtGui.QScrollArea()
        scroll2.setWidget(group2)
        scroll2.setWidgetResizable(True)
        scroll2.setFixedHeight(mainwind_h*0.8)
        
        scroll3 = QtGui.QScrollArea()
        scroll3.setWidget(group3)
        scroll3.setWidgetResizable(True)
        scroll3.setFixedHeight(mainwind_h*0.8)
        
        self.qtab.tab1.vbox.addWidget(SetButton(my_set,self))

        hbox = QtGui.QVBoxLayout()

        title_style = "QLabel { background-color : #ffcc33 ; color : black;  font-style : bold; font-size : 14px;}"
        title1 = QtGui.QLabel('List of sets and sub sets')
        title1.setFixedWidth(self.width() - 12)
        title1.setFixedHeight(20)
        title1.setAlignment(QtCore.Qt.AlignCenter)
        title1.setStyleSheet(title_style)
        hbox.addWidget(title1)
        hbox.addWidget(scroll)
        self.qtab.tab1.setLayout(hbox)

        hbox2=QtGui.QVBoxLayout()
        title2 = QtGui.QLabel('Sets results of clustering')
        title2.setFixedWidth(self.width()-12)
        title2.setFixedHeight(20)
        title2.setAlignment(QtCore.Qt.AlignCenter)
        title2.setStyleSheet(title_style)
        hbox2.addWidget(title2)
        hbox2.addWidget(scroll2)
        self.qtab.tab2.setLayout(hbox2)

        hbox3=QtGui.QVBoxLayout()
        title3 = QtGui.QLabel('Sets results of calculation')
        title3.setFixedWidth(self.width()-12)
        title3.setFixedHeight(20)
        title3.setAlignment(QtCore.Qt.AlignCenter)
        title3.setStyleSheet(title_style)
        hbox3.addWidget(title3)
        hbox3.addWidget(scroll3)
        self.qtab.tab3.setLayout(hbox3)

        glob = QtGui.QVBoxLayout()
        glob.addWidget(self.qtab)
        glob.addLayout(buttonsBox)
        self.setLayout(glob)
               

    def add(self, my_set):
        # -- This add will add a SetButton
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height()
        mainwind_w = rec.width()
        new_set_button = SetButton(my_set,self)
        if (my_set.number_of_collection() != 0):
            for i in my_set.get_coll().values() :
                new_set_button.vizu.add(i)
                add_coll(i)
        if (my_set.number_of_subset() != 0 ):
            for i in my_set.getAllSubSets():
                new_set_button.addFullSubSet(i)
                self.add(i)
        
        new_set_button.setMinimumSize(QSize(225, mainwind_h / 8))
        self.qtab.tab1.vbox.addWidget(new_set_button)

    def add2(self):
        for j in getClusterResultSets():
            s = SetButton(j,self)
            for c in j.get_all_nifti_set():
                s.vizu.add(c)
                add_coll(c)
            self.qtab.tab2.vbox2.addWidget(s)
            rmClusterResultSets(j)

    def add3(self):
        for j in getCalculResultSets():
            s = SetButton(j,self)
            for c in j.get_all_nifti_set():
                s.vizu.add(c)
                add_coll(c)
            self.qtab.tab3.vbox3.addWidget(s)
        rmAllCalculResultSets()
    
    def update(self):
        # -- Update the list of subsets shown. Usefull when a sub set is renamed
        items = (self.qtab.tab1.vbox.itemAt(j).widget() for j in range(self.qtab.tab1.vbox.count()))
        for i in items:
            if isinstance(i, SetButton):
                i.updateSubSetName()
        self.parent().parent().parent().upCollLabel()

    def updateSet(self,new_set):
        # -- Update the list of subsets shown. Usefull when a sub set is renamed
        items = (self.qtab.tab1.vbox.itemAt(j).widget() for j in range(self.qtab.tab1.vbox.count()))
        for i in items:
            if isinstance(i, SetButton):
                if i.my_set.get_name() == new_set.get_name():
                    set_current_vizu(i.vizu)
                    self.parent().parent().updateVizu(i.vizu)
                    self.parent().parent().upCollLabel()
    
    def deselectAll(self):
        tabs = [self.qtab.tab1.vbox, self.qtab.tab2.vbox2, self.qtab.tab3.vbox3]
        for tab in tabs :
            set_buttons = (tab.itemAt(j).widget() for j in range(tab.count()))
            for set_button in set_buttons:
                set_button.vizu.deselectAll()

    def selectAll(self):
        tabs = [self.qtab.tab1.vbox, self.qtab.tab2.vbox2, self.qtab.tab3.vbox3]
        for tab in tabs :
            set_buttons = (tab.itemAt(j).widget() for j in range(tab.count()))
            for set_button in set_buttons:
                set_button.vizu.selectAll()

class MainView(QtGui.QWidget):
    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to know when to change the central view (central widget) of our app
    # In our custom widgets (like this one), buttons will emit a given signal, and the change of views will be handled
    # by the HomePage widgets' instances (see UI.py, class HomePage)
    showClust = pyqtSignal()
    showEdit = pyqtSignal()
    showExport = pyqtSignal()
    showCalcul = pyqtSignal()

    def __init__(self):
        super(MainView, self).__init__()

        self.initMainView()

    def initMainView(self):
        # -- We create all objects we need
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height() / 1.4
        mainwind_w = rec.width() / 1.5
        buttonsBox = QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        # - Buttons to access other windows
        editButton = QtGui.QPushButton("Edit")
        editButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/writing.png'))
        editButton.setStatusTip("Edit selected image collections")
        editButton.clicked.connect(self.edit_pannel)  # When editButton is clicked, change central views

        exportButton = QtGui.QPushButton("Export data")
        exportButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/libreoffice.png'))
        exportButton.setStatusTip("Export as xlsx or NIfTI")
        exportButton.clicked.connect(self.export)

        calcButton = QtGui.QPushButton("Calculations")
        calcButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/calculator.png'))
        calcButton.setStatusTip("Perform calculations on selected data")
        calcButton.clicked.connect(self.calcul)  # When calculation is clicked, change central views

        clusterButton = QtGui.QPushButton("Clustering")
        clusterButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/square.png'))
        clusterButton.setStatusTip("Apply clustering on selected data")
        clusterButton.clicked.connect(self.extract_and_cluster)  # When clusterButton is clicked, change central views

        buttonsBox.addWidget(editButton)
        buttonsBox.addWidget(exportButton)
        buttonsBox.addWidget(calcButton)
        buttonsBox.addWidget(clusterButton)

        self.setAccessBox = SetAccessBar()
        self.collectionsDisplayBox = get_current_vizu()
        hbox = QtGui.QHBoxLayout()

        self.splitter1 = QtGui.QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(self.setAccessBox)
        self.splitter1.addWidget(self.collectionsDisplayBox)
        hbox.addWidget(self.splitter1)
        containerVbox = QtGui.QVBoxLayout()
        containerVbox.addLayout(hbox)
        containerVbox.addLayout(buttonsBox)
        self.setLayout(containerVbox)

    def buttonClicked(self):
        print "Test passed. SUCCESS!"

    def show_coll(self, coll):
        # -- This show_coll will adda collection to the current vizu
        get_current_vizu().add(coll)

    def export(self):
        if get_selected():
            export_choice = QtGui.QMessageBox()
            export_choice.setWindowTitle('Export dataSet')

            nifti_opt = QRadioButton("Export to Nifti")
            excel_opt = QRadioButton("Export to CSV")
            nifti_opt.setChecked(True)

            l1 = export_choice.layout()
            l1.setContentsMargins(20, 0, 0, 20)
            l1.addWidget(QLabel("You have selected (" + str(len(
                get_selected())) + ") image collections. \nPlease select the way "
                                   "you would like to export these files : "),
                        l1.rowCount() - 3, 0, 1, l1.columnCount() - 2, Qt.AlignCenter)
            rb_box = QtGui.QGroupBox()
            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(nifti_opt)
            vbox.addWidget(excel_opt)

            rb_box.setLayout(vbox)
            l1.addWidget(rb_box, l1.rowCount() - 2, 0, Qt.AlignCenter)

            export_choice.setStandardButtons(QMessageBox.Cancel | QMessageBox.Apply)

            ret = export_choice.exec_()

            if ret == QtGui.QMessageBox.Apply:

                if nifti_opt.isChecked():

                    folder_path = str(QFileDialog.getExistingDirectory())
                    image_recreation_from_list(folder_path, selected)

                    export_nifti()

                elif excel_opt.isChecked():
                    type_choice = QtGui.QMessageBox()
                    type_choice.setWindowTitle('Export excel all or centroid')

                    all_opt = QRadioButton("Export all points")
                    centroid_opt = QRadioButton("Export only the centroid of each file")
                    all_opt.setChecked(True)

                    l2 = type_choice.layout()
                    l2.setContentsMargins(20, 0, 0, 20)
                    l2.addWidget(QLabel(" Excel Export \nPlease select the type of export"),
                                 l2.rowCount() - 3, 0, 1, l2.columnCount() - 2, Qt.AlignCenter)

                    rb_box = QtGui.QGroupBox()
                    vbox = QtGui.QVBoxLayout()
                    vbox.addWidget(all_opt)
                    vbox.addWidget(centroid_opt)

                    rb_box.setLayout(vbox)
                    l2.addWidget(rb_box, l2.rowCount() - 2, 0, Qt.AlignCenter)

                    type_choice.setStandardButtons(QMessageBox.Cancel | QMessageBox.Apply)

                    ret = type_choice.exec_()

                    if ret == QtGui.QMessageBox.Apply:

                        (f_path, f_name) = os.path.split(str(QFileDialog.getSaveFileName(self, "Browse Directory")))

                        if all_opt.isChecked():
                            extract_data_from_selected()
                        elif centroid_opt.isChecked():
                            extract_data_as_centroids_from_selected()

                    ee.simple_export(f_name, f_path, get_current_usableDataset())
                    export_excel()

                else:
                    print "WTF ?!!?"

        else:
            QtGui.QMessageBox.information(self, "Selection empty", "There's nothing to export.")



    def extract_and_cluster(self):
        if get_selected():
            choice = QtGui.QMessageBox()
            choice.setWindowTitle('Extract data for clustering')

            centroid_opt = QRadioButton("Use centroids as file representation")
            all_points_opt = QRadioButton("Use all region points for each file")
            all_points_opt.setChecked(True)

            l = choice.layout()
            l.setContentsMargins(20, 0, 0, 20)
            l.addWidget(QLabel("You have selected (" + str(len(
                                                    get_selected())) + ") image collections. \nPlease select the way "
                                                                       "you would like each file to be represented : "),
                        l.rowCount() - 3, 0, 1, l.columnCount() - 2, Qt.AlignCenter)
            rb_box = QtGui.QGroupBox()
            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(all_points_opt)
            vbox.addWidget(centroid_opt)

            rb_box.setLayout(vbox)
            l.addWidget(rb_box, l.rowCount()-2, 0, Qt.AlignCenter)
            # l.addWidget(QtGui.QSpacerItem(500, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), l.rowCount()-1, 0, 1, l.columnCount(), Qt.AlignCenter)

            choice.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            ret = choice.exec_()

            if ret == QtGui.QMessageBox.Yes:

                if all_points_opt.isChecked():
                    extract_data_from_selected()

                elif centroid_opt.isChecked():
                    extract_data_as_centroids_from_selected()

                else :
                    print "WTF ?!!?"

                self.showClust.emit()

        else:
            QtGui.QMessageBox.information(self, "Selection empty", "There's no data to extract and clusterize.")

    def calcul(self):
        if (get_selected()):
            self.showCalcul.emit()

        else:
            QtGui.QMessageBox.information(self, "Selection empty", "There's no data to calculation.")

    def edit_pannel(self):
        # -- This edit_pannel will show the edit view if selected is not empty
        if (get_selected()):
            self.showEdit.emit()
        else:
            QtGui.QMessageBox.information(self, "Selection empty", "There's no data to edit.")

    def show_set(self, new_set):
        # -- This show_set will add the new_set to the setAccessBox and display the current vizu that changed in the process
        set_current_set(new_set)
        self.setAccessBox.add(new_set)
        self.updateVizu(get_current_vizu())

    def update(self):
        # -- This update will call the update function of collectionsDisplayBox
        self.collectionsDisplayBox.update()

    def updateVizu(self, newVizu):
        # -- This updateVizu will display the newVizu but not delete the old one to be able to chow it again later
        newVizu.update()
        self.collectionsDisplayBox = newVizu
        delete_me = self.splitter1.widget(1)
        delete_me.setParent(None)
        # DO NOT DO delete_me.deleteLater() -> we need it alive!
        self.splitter1.addWidget(newVizu)

    def upCollLabel(self):
        # -- This upCollLabel will display the name of the current set at top of the screen
        label = get_current_set().name
        limit = 500
        if (len(label) > limit):
            nb = limit - len(label) + 1
            label = label[:nb] + "-"
        self.collectionsDisplayBox.update_label(label)


    def updateClusterRes(self):
        self.setAccessBox.add2()

    def updateCalculRes(self):
        self.setAccessBox.add3()

