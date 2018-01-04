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
# 2 january 2018- Initial design and coding. (@vz-chameleon, Valentina Z.)
import os
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal
from PyQt4.Qt import *

import resources


class ClusteringDataTable(QtGui.QTableWidget):
    def __init__(self, row_num):
        super(ClusteringDataTable, self).__init__()
        self.setRowCount(row_num)
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["PatientID_imgColl", "X", "Y", "Z", "Intensity"])


class ClusteringView(QtGui.QWidget):
    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to know when to change the central view (central widget) of our app
    # In our custom widgets (like this one), buttons will emit a given signal, and the change of views will be handled
    # by the HomePage widgets' instances (see UI.py, class HomePage)

    showMain = pyqtSignal()

    def __init__(self):
        super(ClusteringView, self).__init__()

        self.initClusteringView()

    def initClusteringView(self):

        title_style = "QLabel { background-color : #ffcc33 ; color : black;  font-style : bold; font-size : 14px;}"
        # ---------- Box Layout Set up ---------
        # Here, the instance IS a Widget, so we'll add the layouts to itself

        # - Horizontal box for go back home button
        buttonsBox= QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        runClusteringButton = QtGui.QPushButton('Run')
        runClusteringButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/play.png'))
        runClusteringButton.setToolTip("Run selected clustering")

        goHomeButton = QtGui.QPushButton('Go back')
        goHomeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/home-2.png'))
        goHomeButton.setToolTip("Return to main page")
        goHomeButton.clicked.connect(self.showMain.emit)# When go back home button is clicked, change central views

        buttonsBox.addWidget(runClusteringButton)
        buttonsBox.addWidget(goHomeButton)


        # -------------- Script Environemment Widget --------------
        scriptWidget=QtGui.QWidget()
        # - Vertical box for future script Environnement
        scriptEnvBox = QtGui.QVBoxLayout()

        scriptEnv_title = QtGui.QLabel('Script Environment')
        scriptEnv_title.setStyleSheet(title_style)

        editor = QtGui.QVBoxLayout()
        edit_input=QtGui.QTextEdit()

        editor.addWidget(scriptEnv_title)
        editor.addWidget(edit_input)

        scriptEnvBox.addLayout(editor)

        # Add the layout to script widget
        scriptWidget.setLayout(scriptEnvBox)


        # -------------- Clustering Widget -----------------------
        clustWidget = QtGui.QWidget()

        # - A splitter for clustering results display
        clust_res_splitter = QtGui.QSplitter(Qt.Vertical)

        # === A table widget ===
        table_clust=QtGui.QWidget()

        # Horizontal box for table display
        tableBox = QtGui.QVBoxLayout()

        table_title = QtGui.QLabel('Data - Clustering Results')
        table_title.setStyleSheet(title_style)
        table_displayer = ClusteringDataTable(20)
        tableBox.addWidget(table_title)
        tableBox.addWidget(table_displayer)

        # set table clust widget's layout
        table_clust.setLayout(tableBox)

        # === A graphs widget ===
        graphWidget=QtGui.QWidget()

        # Horizontal box for mini graphs display
        graphBox = QtGui.QVBoxLayout()

        graph_title = QtGui.QLabel('Results Graphs')
        graph_title.setStyleSheet(title_style)

        grid = QtGui.QGridLayout()
        grid.setSpacing(8)

        graph1 = QtGui.QTextEdit()
        graph2 = QtGui.QTextEdit()
        graph3 = QtGui.QTextEdit()
        grid.addWidget(graph1, 1, 0)
        grid.addWidget(graph2, 1, 1)
        grid.addWidget(graph3, 1, 2)

        graphBox.addWidget(graph_title)
        graphBox.addLayout(grid)

        # Set graph widgets's layout
        graphWidget.setLayout(graphBox)

        # Add the previous widgets to clustering splitter
        clust_res_splitter.addWidget(table_clust)
        clust_res_splitter.addWidget(graphWidget)

        hbox=QtGui.QHBoxLayout()
        hbox.addWidget(clust_res_splitter)
        clustWidget.setLayout(hbox)


        # ----- Now that we have our two main widgets, we can add them to the main splitter of this view -----

        # Set the layout of clustering widget and set it as the central widget for QtMainWindow
        main_splitter = QtGui.QSplitter(Qt.Horizontal)
        main_splitter.addWidget(scriptWidget)
        main_splitter.addWidget(clustWidget)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(main_splitter)

        containerVbox = QtGui.QVBoxLayout()
        containerVbox.addLayout(buttonsBox)
        containerVbox.addLayout(hbox)

        self.setLayout(containerVbox)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = ClusteringView()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
