# NAME
#		  calculationView
#
# DESCRIPTION
#
#		 'calculationView' contains the Qwidget for the calculation view
#
# HISTORY
#
# 15 january 2018 - Initial design and coding. (@maximeCluchague, Maxime C.)

from PyQt4 import QtGui
from PyQt4.Qt import *

import sys
from nibabel import Nifti1Image,load
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from BrainMapper import *

import resources
import time


class CalculationView(QtGui.QWidget):
    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to know when to change the central view (central widget) of our app
    # In our custom widgets (like this one), buttons will emit a given signal, and the change of views will be handled
    # by the HomePage widgets' instances (see UI.py, class HomePage)

    showMain = pyqtSignal()

    def __init__(self):
        super(CalculationView, self).__init__()
        self.leftlist = QListWidget()
        self.leftlist.insertItem(0, 'Addition')
        self.leftlist.insertItem(1, 'Boolean Intersection')
        self.leftlist.insertItem(2, 'Boolean Union')
        self.leftlist.insertItem(3, 'Centroide')
        self.leftlist.insertItem(4, 'Closing')
        self.leftlist.insertItem(5, 'Dilation')
        self.leftlist.insertItem(6, 'Entropy')
        self.leftlist.insertItem(7, 'Erosion')
        self.leftlist.insertItem(8, 'Linear combination')
        self.leftlist.insertItem(9, 'Mask')
        self.leftlist.insertItem(10, 'Mean')
        self.leftlist.insertItem(11, 'Normalization')
        self.leftlist.insertItem(12, 'Opening')
        self.leftlist.insertItem(13, 'Threshold')
        

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        self.stack5 = QWidget()
        self.stack6 = QWidget()
        self.stack7 = QWidget()
        self.stack8 = QWidget()
        self.stack9 = QWidget()
        self.stack10 = QWidget()
        self.stack11 = QWidget()
        self.stack12 = QWidget()
        self.stack13 = QWidget()
        self.stack14 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()
        self.stack5UI()
        self.stack6UI()
        self.stack7UI()
        self.stack8UI()
        self.stack9UI()
        self.stack10UI()
        self.stack11UI()
        self.stack12UI()
        self.stack13UI()
        self.stack14UI()
        
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)
        self.Stack.addWidget(self.stack5)
        self.Stack.addWidget(self.stack6)
        self.Stack.addWidget(self.stack7)
        self.Stack.addWidget(self.stack8)
        self.Stack.addWidget(self.stack9)
        self.Stack.addWidget(self.stack10)
        self.Stack.addWidget(self.stack11)
        self.Stack.addWidget(self.stack12)
        self.Stack.addWidget(self.stack13)
        self.Stack.addWidget(self.stack14)

        self.goHomeButton = QtGui.QPushButton('Go back')
        self.goHomeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/home-2.png'))
        self.goHomeButton.setToolTip("Return to main page")
        self.goHomeButton.clicked.connect(self.showMain.emit)

        self.runOpperationButton = QtGui.QPushButton('Calculate')
        self.runOpperationButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/calculator.png'))
        self.runOpperationButton.setToolTip("Run selected opperation")
        self.runOpperationButton.clicked.connect(lambda: self.runCalculation())

        # self.saveFile = QtGui.QPushButton('Save file')
        # self.saveFile.setIcon(QtGui.QIcon(':ressources/app_icons_png/download.png'))
        # self.saveFile.setToolTip("Save the calculated resulting file")

        vbox = QVBoxLayout(self)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)
        
        hbox.addWidget
        
        
        vbox.addLayout(hbox)

        self.console = QTextEdit(">>>")
        self.console.setReadOnly(True)
        self.console.setFixedHeight(180)
        vbox.addWidget(self.console)        
        
        buttonbox = QtGui.QHBoxLayout()
        buttonbox.addStretch(0)
        buttonbox.addWidget(self.goHomeButton)

        buttonbox.addStretch(1)
        buttonbox.addWidget(self.runOpperationButton)

        vbox.addLayout(buttonbox)

        self.setLayout(vbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.show()

    # ----- Addition ------------------------------------
    def stack1UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)

        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("The Addition algorithm make a addition with a collection of nifti makes the term some term of each voxel")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)
        
        descbox.addWidget(description)
        algorithm = QLabel("Example")
        algorithm.setStyleSheet("background-color: #FFCC33;")
        
        calcul = QTextEdit("")
        calcul.setText("\t[5, 3, 0]   [0, 4, 0]       [5, 8, 0]\n\t[0, 0, 3]   [0, 7, 4]       [0, 7, 7]\nAddition ( \t[1, 1, 2] , [3, 0, 0] ) = [4, 1, 2]")
        calcul.setReadOnly(True)
        calcul.setFixedHeight(70)
        descbox.addWidget(algorithm)
        descbox.addWidget(calcul)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack1.setLayout(vbox)

    # ----- Boolean Intersection -----------------------
    def stack2UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)

        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("The Boolean intersection takes a set of files and returns a binary file of 0 and 1. A voxel with 1 value means that for every file this voxels have strictely positive intensity")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)
        
        descbox.addWidget(description)
        algorithm = QLabel("Example")
        algorithm.setStyleSheet("background-color: #FFCC33;")
        
        calcul = QTextEdit("")
        calcul.setText("\t[5, 9, 0]   [0, 4, 0]       [0, 1, 0]\n\t[0, 0, 3]   [0, 7, 4]       [0, 0, 1]\nBoolInter( \t[1, 1, 2] , [3, 0, 0] ) = [1, 0, 0]")
        calcul.setReadOnly(True)
        calcul.setFixedHeight(70)
        descbox.addWidget(algorithm)
        descbox.addWidget(calcul)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack2.setLayout(vbox)

    # ----- Boolean Union ----------------------------
    def stack3UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)

        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("The Boolean union takes a set of files and returns a binary file of 0 and 1. A voxel with 1 value means that there exists in at least some files nifti a voxel whose intensity is strictly positive")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)
        
        descbox.addWidget(description)
        algorithm = QLabel("Example")
        algorithm.setStyleSheet("background-color: #FFCC33;")
        
        calcul = QTextEdit("")
        calcul.setText("\t[5, 9, 0]   [0, 4, 0]       [1, 1, 0]\n\t[0, 0, 3]   [0, 7, 0]       [0, 1, 1]\nBoolUnion( \t[0, 1, 2] , [0, 0, 0] ) = [0, 1, 1]")
        calcul.setReadOnly(True)
        calcul.setFixedHeight(70)
        descbox.addWidget(algorithm)
        descbox.addWidget(calcul)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack3.setLayout(vbox)

    # ----- Centroide ------------------------------------
    def stack4UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)

        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("This algorithm calculates the centroid of each cluster present in one or a set of nifti files")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)
        
        descbox.addWidget(description)
        algorithm = QLabel("Example")
        algorithm.setStyleSheet("background-color: #FFCC33;")
        
        calcul = QTextEdit("")
        calcul.setText("\t[0, 1, 0]\n\t[5, 2, 3]\nCentroid ( \t[0, 1, 0] ) = (1,1,1)")
        calcul.setReadOnly(True)
        calcul.setFixedHeight(70)
        descbox.addWidget(algorithm)
        descbox.addWidget(calcul)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack4.setLayout(vbox)
    
    # ----- Closing ------------------------------------
    def stack5UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)
        layout.addWidget(QLabel("Number of Iteration :"))
        self.paramClosing = QLineEdit("1")
        layout.addWidget(self.paramClosing)
        
        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("TO WRITE")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)
        
        descbox.addWidget(description)
        algorithm = QLabel("Example")
        algorithm.setStyleSheet("background-color: #FFCC33;")
        
        calcul = QTextEdit("")
        calcul.setText("Opening(n) = Erosion(Dilation(n))")
        calcul.setReadOnly(True)
        calcul.setFixedHeight(70)
        descbox.addWidget(algorithm)
        descbox.addWidget(calcul)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack5.setLayout(vbox)

    # ----- Dilatation ---------------------------
    def stack6UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)
        layout.addWidget(QLabel("Number of Iteration :"))
        self.paramDilation = QLineEdit("1")
        layout.addWidget(self.paramDilation)
        
        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)
        

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("NO IMPLEMENTED")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)

        descbox.addWidget(description)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack6.setLayout(vbox)

    # ----- Entropy -----------------------------
    def stack7UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)

        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("The entropy of an image is a decimal value that allows to characterize the degree of disorganization, or unpredictability of the information content of a system.")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)
        
        descbox.addWidget(description)
        algorithm = QLabel("Example")
        algorithm.setStyleSheet("background-color: #FFCC33;")
        
        calcul = QTextEdit("")
        calcul.setText("Entropy(Nifti img) = SUM(-Pi * log2(Pi))\nWhere Pi is the probability for the value i in the image to appear.")
        calcul.setReadOnly(True)
        calcul.setFixedHeight(70)
        descbox.addWidget(algorithm)
        descbox.addWidget(calcul)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack7.setLayout(vbox)

    # ----- Erosion ------------------------------
    def stack8UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)
        layout.addWidget(QLabel("Number of Iteration :"))
        self.paramErosion = QLineEdit("1")
        layout.addWidget(self.paramErosion)
        
        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("NO IMPLEMENTED")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)

        descbox.addWidget(description)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack8.setLayout(vbox)

    # ----- Linear combination ---------------------------
    def stack9UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)

        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("This algorithm makes the sum of a set of nifti files by associating a weight to each one of them (to caracterizes the importance)")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)
        
        descbox.addWidget(description)
        algorithm = QLabel("Example")
        algorithm.setStyleSheet("background-color: #FFCC33;")
        
        calcul = QTextEdit("")
        calcul.setText("Linear(img1, .., imgN] , [c1, .., cN]) = c1*Ni_1 + .. + cN*Ni_N")
        calcul.setReadOnly(True)
        calcul.setFixedHeight(70)
        descbox.addWidget(algorithm)
        descbox.addWidget(calcul)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack9.setLayout(vbox)
    # ----- Mask ---------------------------------
    def stack10UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)

        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("The Mask process need two file : one named mask that permit to define which voxels in the second one will be selected. Only the voxels in the second one where the voxels in the mask with the same coordinates and a value > 0 will be selected.")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)
        
        descbox.addWidget(description)
        algorithm = QLabel("Example")
        algorithm.setStyleSheet("background-color: #FFCC33;")
        
        calcul = QTextEdit("")
        calcul.setText("\t[1, 1, 0]   [2, 4, 9]       [2, 4, 0]\n\t[0, 0, 1]   [3, 7, 5]       [0, 0, 5]\nMaskProc ( \t[1, 0, 1] , [6, 8, 4] ) = [6, 0, 4]")
        calcul.setReadOnly(True)
        calcul.setFixedHeight(70)
        descbox.addWidget(algorithm)
        descbox.addWidget(calcul)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack10.setLayout(vbox)
        
    # ----- Mean ---------------------------------
    def stack11UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)

        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("The Mean process averages a set of nifti files. The algorithm performs the sum for all voxels present in each file the divides the value obtained by the number of files")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)
        
        descbox.addWidget(description)
        algorithm = QLabel("Example")
        algorithm.setStyleSheet("background-color: #FFCC33;")
        
        calcul = QTextEdit("")
        calcul.setText("\t[5, 9, 0]   [0, 4, 0]       [2.5, 6.5, 0.0]\n\t[0, 0, 3]   [0, 7, 0]       [0.0, 3.5, 1.5]\nMeanProc ( \t[0, 1, 2] , [0, 0, 0] ) = [0.0, 0.5, 1.0]")
        calcul.setReadOnly(True)
        calcul.setFixedHeight(70)
        descbox.addWidget(algorithm)
        descbox.addWidget(calcul)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack11.setLayout(vbox)

    # ----- Normalization ------------------------------------
    def stack12UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)

        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("The normalization algorithm creates one nifti file result for each input nifti file. This algorithm create a file where the values for each voxel are between 0 and 1. Different ways exit to normalize a nifti file, you can select in the options panel the desired method")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)

        descbox.addWidget(description)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack12.setLayout(vbox)

    # ----- Opening ------------------------------------
    def stack13UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)
        layout.addWidget(QLabel("Number of Iteration :"))
        self.paramOpening = QLineEdit("1")
        layout.addWidget(self.paramOpening)
        
        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("TO WRITE")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)
        
        descbox.addWidget(description)
        algorithm = QLabel("Example")
        algorithm.setStyleSheet("background-color: #FFCC33;")
        
        calcul = QTextEdit("")
        calcul.setText("Opening(n) = Dilation(Erosion(n))")
        calcul.setReadOnly(True)
        calcul.setFixedHeight(70)
        descbox.addWidget(algorithm)
        descbox.addWidget(calcul)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack13.setLayout(vbox)    
    
    # ----- Threshold ------------------------------------
    def stack14UI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()
        vbox.addLayout(layout)

        options = QLabel("Arguments")
        options.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(options)
        layout.addWidget(QLabel("Min :"))
        self.thresholdMin = QLineEdit("")
        layout.addWidget(self.thresholdMin)
        
        layout.addWidget(QLabel("Max :"))
        self.thresholdMax = QLineEdit("")
        layout.addWidget(self.thresholdMax)
        
        descrip = QLabel("Description")
        descrip.setStyleSheet("background-color: #FFCC33;")
        layout.addRow(descrip)

        descbox = QtGui.QVBoxLayout()
        description = QTextEdit("TO WRITE")
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        description.setReadOnly(True)
        
        descbox.addWidget(description)
        algorithm = QLabel("Example")
        algorithm.setStyleSheet("background-color: #FFCC33;")
        
        calcul = QTextEdit("")
        calcul.setText("TO WRITE")
        calcul.setReadOnly(True)
        calcul.setFixedHeight(70)
        descbox.addWidget(algorithm)
        descbox.addWidget(calcul)
        description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
        vbox.addLayout(descbox)
        self.stack14.setLayout(vbox)    
    
    def display(self, i):
        self.Stack.setCurrentIndex(i)
        
    def popUpSaveFileResultCalculation(self,algorithm,result):
        choice = QtGui.QMessageBox()
        choice.setWindowTitle('Success !') 
        l = choice.layout()
        l.setContentsMargins(20, 10, 10, 20)
        l.addWidget(QLabel(algorithm +" algorithm has been correctly applicated on nifti(s) file(s)\n\n\n\nDo you want save the algorithm's result as Set ?"),
        l.rowCount() - 3, 0, 1, l.columnCount() - 2, Qt.AlignCenter)
        choice.setStandardButtons(QMessageBox.Cancel | QMessageBox.Save)
        wantToSave = choice.exec_()
        if wantToSave == QtGui.QMessageBox.Save:
            setCalculation = Set("calc_")
            setCalculation.set_name("calc_"+str(id(setCalculation)))
            coll = ImageCollection("coll_",setCalculation)
            coll.set_name("coll_"+str(id(coll)))
            for matrixData in result:
                template_mni_path = 'ressources/template_mni/mni_icbm152_t1_tal_nlin_asym_09a.nii'          
                template_data = load(template_mni_path)
                template_affine = template_data.affine
                recreate_image = Nifti1Image(matrixData, template_affine)
                ni_image = NifImage(""+str(time.time()*1000), recreate_image)
                ni_image.set_filename("file_"+algorithm+"_"+str(id(ni_image)))             
                coll.add(ni_image)
            setCalculation.add_collection(coll)
            makeCalculResultSet(setCalculation)

    # --------------------- Action for CALCULATE button -------------------
    def runCalculation(self):
        print("calculation in progress...")
        algorithm = self.leftlist.selectedItems()[0].text()
        # extraction of arguments here
        #
        #  ... TO DO ...
        #
        arguments = []
        nifti_selected = []
        
        for collection in selected:
            for nifti in collection.nifimage_dict.values():
                #COPIE nifti_selected.append(nifti.filename)
                nifti_selected.append(nifti)
        
        if algorithm=="Mean":
            if len(nifti_selected)<2:
                    QtGui.QMessageBox.warning(self, "Error",
                                              algorithm + "algorithm "+ " must have two or more input file")
            else:
                try:
                        algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                        self.console.setText(">>> \n"+output)
                        self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
                        
                except:
                    QtGui.QMessageBox.warning(self, "Error",
                                              "Impossible to execute "+algorithm+" algorithm")                
        if algorithm=="Mask":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n"+output)
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm. This algorithm can only takes 2 File : The mask and the one which will be applied the mask. Please verify that you have select just 2 file in your collection.")
                                      
        if algorithm=="Linear combination":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm. Please check if you have correctly entering the coefficent list")
                                          
        if algorithm=="Boolean Intersection":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm")
        if algorithm=="Boolean Union":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm")
        if algorithm=="Normalization":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm")
        if algorithm=="Centroide":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm")
        if algorithm=="Addition":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm")
        if algorithm=="Entropy":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, arguments)
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm")
        if algorithm=="Erosion":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, self.paramErosion.text() )
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm")
        if algorithm=="Dilation":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, self.paramDilation.text() )
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm")
        if algorithm=="Opening":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, self.paramOpening.text() )
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm")
        if algorithm=="Closing":
            try:
                algorithm_result, output = run_calculation(algorithm, nifti_selected, self.paramClosing.text() )
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm")
        if algorithm=="Threshold":
            try:
                min =  float(self.thresholdMin.text())
                max =  float(self.thresholdMax.text())
                algorithm_result, output = run_calculation(algorithm, nifti_selected, [min,max] )
                self.console.setText(">>> \n"+output)                
                self.popUpSaveFileResultCalculation(algorithm,algorithm_result)
            except:
                QtGui.QMessageBox.warning(self, "Error",
                                          "Impossible to execute "+algorithm+" algorithm\nPlease enter the lower bound (Min) and higher bound (Max). These two arguments must be double value (ex: 5.63)")



