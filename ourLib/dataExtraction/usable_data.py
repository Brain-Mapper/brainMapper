# NAME
#        usable_data
#
# DESCRIPTION
#
#       'usable_data.py' contains the class declaration of the class UsableDataCollection, which is a collection
#       of numpy arrays containing the extracted data of a SINGLE .nii file, associated with the origin filename.
#       For example,when the user wants to use all images in a collection, an UsableDataCollection is returned
#       Finally the class UsableData contains a dictionary of ImageCollections used for extraction and their
#       UsableDataColleciton instances
#       These objects simplified all calculations on a given patient for example.
#
# HISTORY
#
# 18 december 2018 - Initial design and coding. (@vz-chameleon, Valentina Z.)
# 26 december 2017 - Restructuring for further complexity handling (@vz-chameleon, Valentina Z.)

import numpy as np


class UsableDataCollection(object):
    def __init__(self, an_imgcollection_name):
        self.imgcoll_origin=an_imgcollection_name
        # A dictionary to contain the pair key: name of file of origin (ex: 'P92_UL_MN0.nii'),
        #                                  value : usable data array (numpy array containing extracted data)
        self.extracted_data_dict = dict()

    def add_extracted_data_entry(self, origin_filename, usable_data_array):
        # Check whether the given array passed in argument has 4 columns (X,Y,Z, Intensity)
        colnum=(usable_data_array.shape)[1]
        if (colnum > 4) or (colnum < 4):
            raise ValueError('UsableDataCollection.addExtracted_data_entry : array given as argument'
                             ' has more or less than 4 columns')

        self.extracted_data_dict[origin_filename]=usable_data_array

    def remove_extracted_data_entry(self,origin_filename):
        del self.extracted_data_dict[origin_filename]

    def get_imgcoll_name(self):
        return self.imgcoll_origin

    def get_extracted_data_dict(self):
        return self.extracted_data_dict

    def export_as_clusterizable(self):
        clusterizable = np.zeros(shape=(1, 4))  # An empty line of zeros to start with
        for data_array in self.extracted_data_dict.values():
            clusterizable = np.concatenate((clusterizable, data_array), axis=0)

        # Delete the first row containing only zeros
        clusterizable = np.delete(clusterizable, 0, axis=0)

        return clusterizable


class UsableDataSet(object):
    def __init__(self,dataset_name):
        self.dataset_name = dataset_name
        # A dictionary to contain the pair key: name of ImageCollection of origin, value : UsableDataCollection instance
        self.usable_data_list=[]

    def add_usable_data_collection(self, aUsableDataCollection_instance):
        if not type(aUsableDataCollection_instance) is UsableDataCollection:
            raise ValueError('UsableData.add_usable_data_collection : given argument is not an instance of '
                             'UsableDataCollection class')

        self.usable_data_list.append(aUsableDataCollection_instance)

    def get_usable_data_list(self):
        return self.usable_data_list

    def export_as_clusterizable(self):
        clusterizable = np.zeros(shape=(1, 4))  # An empty line of zeros to start with

        for udcoll in self.usable_data_list:
            clusterizable = np.concatenate((clusterizable, udcoll.export_as_clusterizable()), axis=0)

        # Delete the first row containing only zeros
        clusterizable = np.delete(clusterizable, 0, axis=0)

        return clusterizable