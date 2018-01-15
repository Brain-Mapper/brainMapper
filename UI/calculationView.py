# NAME
#
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

from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from BrainMapper import *

import resources

class CalculationView(QtGui.QWidget):
	 # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

	 # ------ pyqt Signals ------
	 # We will use signals to know when to change the central view (central widget) of our app
	 # In our custom widgets (like this one), buttons will emit a given signal, and the change of views will be handled
	 # by the HomePage widgets' instances (see UI.py, class HomePage)

	showMain = pyqtSignal()

	def __init__(self):
		super(CalculationView, self).__init__()
		self.leftlist = QListWidget ()
		self.leftlist.insertItem (0, 'Addition' )
		self.leftlist.insertItem (1, 'Morphologie' )
		self.leftlist.insertItem (2, 'Mean' )
		
		self.stack1 = QWidget()
		self.stack2 = QWidget()
		self.stack3 = QWidget()
			
		self.stack1UI()
		self.stack2UI()
		self.stack3UI()
			
		self.Stack = QStackedWidget (self)
		self.Stack.addWidget (self.stack1)
		self.Stack.addWidget (self.stack2)
		self.Stack.addWidget (self.stack3)
		
		self.goHomeButton = QtGui.QPushButton('Go back')
		self.goHomeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/home-2.png'))
		self.goHomeButton.setToolTip("Return to main page")
		self.goHomeButton.clicked.connect(self.showMain.emit)
		
		self.runOpperationButton = QtGui.QPushButton('Calculate')
		self.runOpperationButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/calculator.png'))
		self.runOpperationButton.setToolTip("Run selected opperation")

		self.runOpperationButton.clicked.connect(lambda: self.runCalculation('test','test'))

		vbox = QVBoxLayout(self)

		hbox = QHBoxLayout(self)
		hbox.addWidget(self.leftlist)
		hbox.addWidget(self.Stack)

		vbox.addLayout(hbox)

		buttonbox= QtGui.QHBoxLayout()
        	buttonbox.addStretch(0)
		buttonbox.addWidget(self.goHomeButton)

		buttonbox.addStretch(1)
		buttonbox.addWidget(self.runOpperationButton)
		
		vbox.addLayout(buttonbox)
	
		self.setLayout(vbox)
		self.leftlist.currentRowChanged.connect(self.display)
		self.show()

	def stack1UI(self):
		vbox = QVBoxLayout(self)
		layout = QFormLayout()
		vbox.addLayout(layout)

		options = QLabel("Options")
		options.setStyleSheet("background-color: #FFCC33;")
		layout.addRow(options)
		layout.addRow("option1",QLineEdit())
		layout.addRow("option2",QLineEdit())

		descrip = QLabel("Description")
		descrip.setStyleSheet("background-color: #FFCC33;")
		layout.addRow(QLabel("\n"))
		layout.addRow(descrip)

		descbox = QtGui.QVBoxLayout()
		description = QTextEdit("A description for this opperation .........................................")
		description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		descbox.addWidget(description)
		description.setStyleSheet("background-color: #e2dfdd; padding:5px; border-radius:7px; border: solid #bdbbb6; ")
		vbox.addLayout(descbox)
		#self.setTabText(0,"Calculation Details")
		self.stack1.setLayout(vbox)
		
	def stack2UI(self):
		layout = QFormLayout()
		sex = QHBoxLayout()
		sex.addWidget(QRadioButton("option1"))
		sex.addWidget(QRadioButton("option2"))
		layout.addRow(QLabel("blabla"),sex)
		layout.addRow("blabla",QLineEdit())
		
		self.stack2.setLayout(layout)
		
	def stack3UI(self):
		layout = QFormLayout()#QHBoxLayout()
		layout.addWidget(QLabel("option1"))
		layout.addWidget(QCheckBox("option2"))
		layout.addWidget(QCheckBox("option2"))
		self.stack3.setLayout(layout)
		
	def display(self,i):
		self.Stack.setCurrentIndex(i)

	def runCalculation(self, selectedMethod, param_list):
		print("Opperation execution :"+self.leftlist.selectedItems()[0].text())
		#Appliquer les fonctions sur l'objet selected qui contient des images Collections
		print(selected)
		#self.table_displayer.fill_clust_labels(labs)



	def main():
		app = QApplication(sys.argv)
		ex = stackedExample()
		sys.exit(app.exec_())
	
	if __name__ == '__main__':
		main()

 
