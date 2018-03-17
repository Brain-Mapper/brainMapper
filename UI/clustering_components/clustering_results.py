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

import os


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
        self.assigned_cluster_labels = None
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

        hist_widget = QtGui.QWidget()
        hist_box = QtGui.QVBoxLayout()

        hist_title = QtGui.QLabel("Cluster assignments Histogram")
        hist_title.setStyleSheet("background-color : #99cccc; font-size: 14px;")

        self.graph1 = pg.GraphicsWindow()
        self.graph1.resize(300, 150)
        self.graph1.setStatusTip("Show an histogram representing the number of points in each cluster.")

        hist_box.addWidget(hist_title)
        hist_box.addWidget(self.graph1)
        hist_widget.setLayout(hist_box)

        sil_widget = QtGui.QWidget()
        sil_box = QtGui.QVBoxLayout()

        sil_title = QtGui.QLabel("Samples Silhouette")
        sil_title.setStyleSheet("background-color : #99cccc; font-size: 14px;")

        self.graph2 = pg.GraphicsWindow()
        self.graph2.resize(300, 150)
        self.graph2.setStatusTip("Show the silhouette of the clustering results")

        sil_box.addWidget(sil_title)
        sil_box.addWidget(self.graph2)
        sil_widget.setLayout(sil_box)


        # Set up for 3D graph, not used in final version
        # self.graph2 = gl.GLViewWidget()
        # self.graph2.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.grid.addWidget(hist_widget, 1, 0)
        self.grid.addWidget(sil_widget, 1, 1)

        graphBox.addWidget(graph_title)
        graphBox.addLayout(self.grid)
        self.graph2.show()
        # Set graph widgets's layout
        self.setLayout(graphBox)

    def clear_graph1(self):
        self.graph1.clear()

    def clear_graph2(self):
        self.graph2.clear()


class ClusteringResultsPopUp(QtGui.QWidget):
    """
    A custom popup window to display more details on clustering results
    """

    #CONSTRUCTOR
    def __init__(self, app_logo_path, save_icon_path):
        super(ClusteringResultsPopUp, self).__init__()

        # The directory to which we must export !
        self.directory_export = ""
        # The name of the text file to which we export
        self.filename = None

        self.setWindowTitle("Clustering Results")
        self.setWindowIcon(QtGui.QIcon(app_logo_path))

        vbox = QtGui.QVBoxLayout()
        savebox = QtGui.QHBoxLayout()
        infobox = QtGui.QHBoxLayout()

        self.save_button = QtGui.QPushButton('Save to text file')
        self.save_button.setIcon(QtGui.QIcon(save_icon_path))
        self.save_button.setStatusTip('Export validation indexes to text file')
        self.save_button.clicked.connect(self.export_as_textfile)

        savebox.addStretch(1)
        savebox.addWidget(self.save_button)

        self.info_panel = QtGui.QTextEdit()
        self.info_panel.setReadOnly(True)

        self.info_panel.setText("======= CLUSTERING VALIDATION INDEXES =======\n\n"
                                "No algorithm has been applied, no indexes were computed ...")

        infobox.addWidget(self.info_panel)
        vbox.addLayout(savebox)
        vbox.addLayout(infobox)

        self.setLayout(vbox)

    def update_details(self, clustering_method, user_values, centroids, validation_values):
        self.info_panel.setText("")

        self.info_panel.insertPlainText(clustering_method+"\n-----------------------------------------------------------------------------\n")

        for param_name in user_values.keys():
            self.info_panel.insertPlainText(param_name+"\t\t\t "+user_values[param_name]+"\n")

        self.info_panel.insertPlainText("-----------------------------------------------------------------------------\n\n")
        self.info_panel.insertPlainText(
            "Cluster centroids\n-----------------------------------------------------------------------------\n")
        count = 0
        for c in centroids:
            self.info_panel.insertPlainText("Cluster "+str(count)+": \t\t" + str(c)+"\n")
            count = count+1

        self.info_panel.insertPlainText(
            "-----------------------------------------------------------------------------\n\n")
        self.info_panel.insertPlainText("Validation Indexes\n-----------------------------------------------------------------------------\n")

        self.info_panel.insertPlainText("Mean Silhouette : \t\t "+str(validation_values[0])+"\n\n")
        self.info_panel.insertPlainText("Calzinski-Habaraz score: \t " + str(validation_values[1]) + "\n\n")
        self.info_panel.insertPlainText("Davies-Bouldin index: \t\t " + str(validation_values[2]) + "\n\n")


    def export_as_textfile(self):
        browser = QtGui.QMessageBox()
        browser.setWindowTitle('Export Validation Indexes as text file')
        # browser.setIcon(QtGui.QMessageBox_Icon(":ressources/logo.png"))

        l = browser.layout()
        l.setContentsMargins(20, 0, 0, 20)
        l.addWidget(QtGui.QLabel("Please select the directory of export and the text file's name \n"
                                 "(no special characters are allowed!)"),
                    l.rowCount() - 3, 0, 1, l.columnCount() - 2, Qt.AlignCenter)
        rb_box = QtGui.QGroupBox()

        # A file browser widget
        browse_files_widget = QtGui.QWidget()
        browseBox = QtGui.QHBoxLayout()

        self.file_path_display = QtGui.QLineEdit()
        browseBox.addWidget(self.file_path_display)

        browseButton = QtGui.QPushButton('Browse')
        # --- Connect to a class function when button is clicked on ---
        browseButton.clicked.connect(self.select_directory)
        browseBox.addWidget(browseButton)
        browse_files_widget.setLayout(browseBox)

        # A filename input prompt
        self.filename_display = QtGui.QLineEdit()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(browse_files_widget)
        vbox.addWidget(self.filename_display)

        rb_box.setLayout(vbox)
        l.addWidget(rb_box, l.rowCount() - 2, 0, Qt.AlignCenter)

        browser.setStandardButtons(QtGui.QMessageBox.Ok| QtGui.QMessageBox.Cancel)

        ret = browser.exec_()

        if ret == QtGui.QMessageBox.Ok:
            self.filename = str(self.filename_display.text())

            if self.filename is not None :
                filepath = os.path.join(self.directory_export,self.filename+'.txt')
                with open(filepath, 'w') as index_file:
                    index_file.write(self.info_panel.toPlainText())

    def select_directory(self):
        """
        Open a browser to select a directory path and put the result into directoryEdit
        """
        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Browse Directory"))
        self.directory_export = file
        self.file_path_display.setText(file)

