# NAME
#        excelExport
#
# DESCRIPTION
#
#       The module 'excelExport.py' contains all the functions export the data to the CSV format.
#
#
# HISTORY
#
# 16 january 2018 - Initial design and coding. (@yoshcraft, Raphael A.)
# 18 january 2018 - Add method for clustering export. (@yoshcraft, Raphael A.)


import os
import csv
import nibabel as nib
import numpy as np
from ourLib.niftiHandlers.imagecollection import ImageCollection


def export_control(name, path):
    """
    Method to control all the os data to verify if the user can export is file
    at path/name
    :param name: file name
    :param path: path of the directory link to this file name
    """
    if name == '':
        # TODO raise an error, instead of a print
        print('Please enter a file name')
        return False
    elif path == '':
        # TODO raise an error, instead of a print
        print ('Please choose a directory')
        return True
    else:
        if os.path.exists(path):
            # TODO extract all the data
            csv_name = str(name) + '.csv'
            if csv_name in os.listdir(path):
                # TODO extract all the data
                print('A file with this name already exist in this directory')
                return True
            else:
                return True
        else:
            # TODO raise an error, instead of a print
            print ('Please enter a valid directory path')
            return False

def simple_export(name, path, a_usable_dataset):

    if export_control(name, path):
        file_path = os.path.join(str(path), str(name) + '.csv')

        header = [
            u'File_Name_Nifti',
            u'Surgeon_ID',
            u'Patient_ID',
            u'Localisation',
            u'Point_Name',
            u'Type_Of_Answer',
            u'X',
            u'Y',
            u'Z',
            u'Intensity'
        ]
        f = open(file_path, 'w')
        f.write(",".join(header) + "\n")

        for udcoll in a_usable_dataset.get_usable_data_list():

            extracted_data_dictionary = udcoll.get_extracted_data_dict()

            for origin_file in extracted_data_dictionary.keys():
                data_array = extracted_data_dictionary[origin_file]
                new_line = [u'', u'', u'', u'', u'', u'', u'', u'', u'', u'']
                for data_rows in range(0, data_array.shape[0]):

                    (f_path, f_name) = os.path.split(str(origin_file.filename))
                    new_line[0] = f_name  # file name

                    new_line[1] = u'Null'  # TODO we don't use this value at this time
                    new_line[2] = u'Null'  # TODO can be set if only the collection name is Patient ID
                    new_line[3] = u'Null'  # TODO
                    new_line[4] = u'Null'  # TODO
                    new_line[5] = u'Null'  # TODO can be set if save somewhere the directory workspace

                    new_line[6] = str(data_array[data_rows, 0])  # X coordinate
                    new_line[7] = str(data_array[data_rows, 1])  # Y coordinate
                    new_line[8] = str(data_array[data_rows, 2])  # Z coordinate
                    new_line[9] = str(data_array[data_rows, 3])  # Intensity

                    f.write(",".join(new_line) + "\n")
        f.close()

def clustering_export(name, path, a_usable_dataset, label):

    if export_control(name, path):
        file_path = os.path.join(str(path), str(name) + '.csv')

        header = [
            u'Image Coll ID',
            u'Origin filename',
            u'X',
            u'Y',
            u'Z',
            u'Intensity',
            u'Assigned cluster'
        ]
        f = open(file_path, 'w')
        f.write(",".join(header) + "\n")
        row_cont = 0

        for udcoll in a_usable_dataset.get_usable_data_list():

            extracted_data_dictionary = udcoll.get_extracted_data_dict()

            for origin_file in extracted_data_dictionary.keys():
                data_array = extracted_data_dictionary[origin_file]
                new_line = [u'', u'', u'', u'', u'', u'', u'']
                for data_rows in range(0, data_array.shape[0]):

                    (f_path, f_name) = os.path.split(str(origin_file.filename))
                    new_line[0] = udcoll.get_imgcoll_name()

                    new_line[1] = f_name  # file name

                    new_line[2] = str(data_array[data_rows, 0])  # X coordinate
                    new_line[3] = str(data_array[data_rows, 1])  # Y coordinate
                    new_line[4] = str(data_array[data_rows, 2])  # Z coordinate
                    new_line[5] = str(data_array[data_rows, 3])  # Intensity
                    new_line[6] = str(label[row_cont])
                    row_cont = row_cont + 1

                    f.write(",".join(new_line) + "\n")
        f.close()
