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
# 2 january 201- Initial design and coding. (@vz-chameleon, Valentina Z.)

import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from BrainMapper import *
    else:
        from ..BrainMapper import *


class ClusteringView(QtGui.QMainWindow):
    def __init__(self):
        super(ClusteringView, self).__init__()

        self.initClusteringView()

    def initClusteringView(self):

        # ---------- Box Layout Set up ---------
        # Since we cannot change the layout of a QtMainWindow, we will use a CENTRAL WIDGET (var homepage)
        # to which we will add a box layout containing other boxes with their own widgets

        clustering_view = QtGui.QWidget()


        # - Vertical box for future script Environnement
        scriptEnvBox = QtGui.QVBoxLayout()

        scriptEnv_title = QtGui.QLabel('Script Environment')

        editor = QtGui.QVBoxLayout()
        edit_input=QtGui.QTextEdit()

        editor.addWidget(scriptEnv_title)
        editor.addWidget(edit_input)

        scriptEnvBox.addLayout(editor)

        # - Vertical box for clustering results display
        clustResultsBox = QtGui.QVBoxLayout()

        # Horizontal box for table display
        tableBox = QtGui.QVBoxLayout()

        table_title = QtGui.QLabel('Data - Clustering Results')
        table_displayer = QtGui.QTextEdit()
        tableBox.addWidget(table_title)
        tableBox.addWidget(table_displayer)

        # Horizontal box for mini graphs display
        graphBox = QtGui.QVBoxLayout()

        graph_title = QtGui.QLabel('Results Graphs')

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

        # Add the previous vertical boxes to horizontal box
        clustResultsBox.addLayout(tableBox)
        clustResultsBox.addLayout(graphBox)

        # Set the layout of clustering widget and set it as the central widget for QtMainWindow
        containerVbox = QtGui.QHBoxLayout()
        containerVbox.addLayout(scriptEnvBox)
        containerVbox.addLayout(clustResultsBox)

        clustering_view.setLayout(containerVbox)

        self.setCentralWidget(clustering_view)
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = ClusteringView()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
