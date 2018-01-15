# NAME
#
#        clusteringView
#
# DESCRIPTION
#
#       'clusteringView' contains the Qwidget for the clustering view
#
# HISTORY
#
# 2 january 2018 - Initial design and coding. (@vz-chameleon, Valentina Z.)

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
	
	goHomeButton = QtGui.QPushButton('Go back')
        goHomeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/home-2.png'))
        goHomeButton.setToolTip("Return to main page")
        goHomeButton.clicked.connect(self.showMain.emit)# When go back home button is clicked, change central views
	
	hbox = QtGui.QHBoxLayout()
	hbox.addWidget(goHomeButton)
	self.setLayout(hbox)


 
