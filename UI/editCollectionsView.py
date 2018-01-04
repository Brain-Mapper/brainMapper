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

import resources


# class CollectionAccessButton(QtGui.QPushButton):
#
#
# class CollectionsAccessBar(QtGui.QVBoxLayout):


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

        # - Horizontal box for go back home button
        buttonsBox = QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        runClusteringButton = QtGui.QPushButton('Run')
        runClusteringButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/play.png'))
        runClusteringButton.setToolTip("Run selected clustering")

        goHomeButton = QtGui.QPushButton('Go back')
        goHomeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/home-2.png'))
        goHomeButton.setToolTip("Return to main page")
        goHomeButton.clicked.connect(self.showMain.emit)  # When go back home button is clicked, change central views

        buttonsBox.addWidget(runClusteringButton)
        buttonsBox.addWidget(goHomeButton)

        hbox = QtGui.QHBoxLayout()

        topleft = QtGui.QFrame()
        topleft.setFrameShape(QtGui.QFrame.StyledPanel)
        bottom = QtGui.QFrame()
        bottom.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter1 = QtGui.QSplitter(Qt.Horizontal)
        textedit = QtGui.QTextEdit()
        splitter1.addWidget(topleft)
        splitter1.addWidget(textedit)
        splitter1.setSizes([100, 200])

        splitter2 = QtGui.QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)

        containerVbox = QtGui.QVBoxLayout()
        containerVbox.addLayout(buttonsBox)
        containerVbox.addLayout(hbox)

        self.setLayout(containerVbox)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = EditCollectionsView()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()