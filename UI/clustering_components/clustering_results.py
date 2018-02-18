# NAME
#
#        clustering_datatable
#
# DESCRIPTION
#
#       'clustering_datatable' contains the custom QTableWdget for the clustering data table
#
# HISTORY
#
# 2 january 2018 - Initial design and coding. (@vz-chameleon, Valentina Z.)
# 5 january 2018 - Added functions to fill table with extracted data

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

import pyqtgraph as pg
import pyqtgraph.opengl as gl


# Inherits QTableWidget
class ClusteringDataTable(QtGui.QTableWidget):
    """
    ClusteringDataTable : the custom QTableWidget that will have all extracted data
    """

    # CONSTRUCTOR
    def __init__(self):
        super(ClusteringDataTable, self).__init__()

        # The usable dataset we are displaying
        self.clustering_usable_dataset = None
        self.setRowCount(20)
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(["Image Coll ID", "Origin filename", "X", "Y", "Z", "Intensity", "Assigned cluster"])

    # CLASS FUNCTIONS
    def fill_with_extracted_data(self, a_usable_dataset_instance):
        """
        Fills this custom table with the data of a UsableDataSet obtained after data extraction
        :param a_usable_dataset_instance: see UsableData for more details
        :return: Nothing
        """
        self.clustering_usable_dataset = a_usable_dataset_instance
        self.setRowCount(a_usable_dataset_instance.get_row_num())

        row_count = 0

        for udcoll in self.clustering_usable_dataset.get_usable_data_list():

            extracted_data_dictionary = udcoll.get_extracted_data_dict()

            for origin_file in extracted_data_dictionary.keys():
                data_array = extracted_data_dictionary[origin_file]
                for data_rows in range(0, data_array.shape[0]):
                    self.setItem(row_count, 0, QtGui.QTableWidgetItem(udcoll.get_imgcoll_name()))
                    self.setItem(row_count, 1, QtGui.QTableWidgetItem(str(origin_file.filename)))
                    self.setItem(row_count, 2, QtGui.QTableWidgetItem(str(data_array[data_rows, 0]))) # X coordinate at column 0
                    self.setItem(row_count, 3, QtGui.QTableWidgetItem(str(data_array[data_rows, 1]))) # Y coordinate at column 1
                    self.setItem(row_count, 4, QtGui.QTableWidgetItem(str(data_array[data_rows, 2]))) # Z coordinate at column 2
                    self.setItem(row_count, 5, QtGui.QTableWidgetItem(str(data_array[data_rows, 3]))) # Intensity at column 3
                    self.setItem(row_count, 6, QtGui.QTableWidgetItem("None yet"))
                    row_count = row_count+1

    def fill_clust_labels(self, assigned_labels_array):
        """
        Fill the 'Assigned cluster' column once we have the clustering labels result
        :param assigned_labels_array:
        :return:
        """

        # The following function is only needed here !
        def generate_random_hex_dict(n):
            import random   #local import (reduced scope)
            ra = lambda: random.randint(0, 255)
            hex_dict = dict()
            for i in range(0, n):
                # Mixing with white to have pastel colors
                hex_string = '#%02X%02X%02X' % ((ra()+255)/2, (ra()+255)/2, (ra()+255)/2)
                hex_dict[str(i)] = hex_string
            return hex_dict

        # Generate one random pastel color for each cluster
        colors = generate_random_hex_dict(len(assigned_labels_array))

        row_count = 0
        for label in assigned_labels_array:
            item = QtGui.QTableWidgetItem(str(label))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QtGui.QColor(colors[str(label)]))

            self.setItem(row_count, 6, item)
            row_count = row_count + 1
            

class ClusteringGraphs(QtGui.QWidget):
    
    def __init__(self, title_style):
        super(ClusteringGraphs, self).__init__()

        # Horizontal box for mini graphs display
        graphBox = QtGui.QVBoxLayout()

        graph_title = QtGui.QLabel('Results Graphs')
        graph_title.setStyleSheet(title_style)

        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(8)

        self.graph1 = pg.GraphicsWindow()
        self.graph1.resize(300, 150)
        self.graph1.setStatusTip("Show an histogramm representing the number of points in each cluster.")
        self.graph2 = gl.GLViewWidget()
        self.graph2.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.grid.addWidget(self.graph1, 1, 0)
        self.grid.addWidget(self.graph2, 1, 1)

        graphBox.addWidget(graph_title)
        graphBox.addLayout(self.grid)
        self.graph2.show()
        # Set graph widgets's layout
        self.setLayout(graphBox)

    def clear_graph1(self):
        self.graph1.clear()