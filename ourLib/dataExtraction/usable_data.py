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
# 18 december 2017 - Initial design and coding. (@vz-chameleon, Valentina Z.)
# 26 december 2017 - Restructuring for further complexity handling (@vz-chameleon, Valentina Z.)
# 12 feb 2018 - Adding method to make a set from a UsableDataSet (@Graziella-Husson)

import numpy as np
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from niftiHandlers.imagecollection import ImageCollection
    from niftiHandlers.nifimage import NifImage
    from niftiHandlers.set import Set
else:
    from ..niftiHandlers.nifimage import NifImage
    from ..niftiHandlers.imagecollection import ImageCollection
    from ..niftiHandlers.set import Set

class UsableDataCollection(object):
    def __init__(self, an_imgcollection_name):
        self.imgcoll_origin=an_imgcollection_name
        # A dictionary to contain the pair key: name of file of origin (ex: 'P92_UL_MN0.nii'),
        #                                  value : usable data array (numpy array containing extracted data)
        self.extracted_data_dict = dict()

        self.rownum=0

    def add_extracted_data_entry(self, origin_filename, usable_data_array):
        # Check whether the given array passed in argument has 4 columns (X,Y,Z, Intensity)
        colnum=(usable_data_array.shape)[1]
        if (colnum > 4) or (colnum < 4):
            raise ValueError('UsableDataCollection.addExtracted_data_entry : array given as argument'
                             ' has more or less than 4 columns')

        self.rownum = self.rownum + (usable_data_array.shape)[0]
        self.extracted_data_dict[origin_filename] = usable_data_array

    def remove_extracted_data_entry(self,origin_filename):
        del self.extracted_data_dict[origin_filename]

    def get_imgcoll_name(self):
        return self.imgcoll_origin

    def get_extracted_data_dict(self):
        return self.extracted_data_dict

    def get_row_num(self):
        return self.rownum

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
        self.usable_data_list = []
        self.rownum = 0

    def add_usable_data_collection(self, aUsableDataCollection_instance):
        if not type(aUsableDataCollection_instance) is UsableDataCollection:
            raise ValueError('UsableData.add_usable_data_collection : given argument is not an instance of '
                             'UsableDataCollection class')

        self.rownum = self.rownum + aUsableDataCollection_instance.get_row_num()
        self.usable_data_list.append(aUsableDataCollection_instance)

    def get_usable_data_list(self):
        return self.usable_data_list

    def get_row_num(self):
        return self.rownum

    def export_as_clusterizable(self):
        clusterizable = np.zeros(shape=(1, 4))  # An empty line of zeros to start with

        for udcoll in self.usable_data_list:
            clusterizable = np.concatenate((clusterizable, udcoll.export_as_clusterizable()), axis=0)

        # Delete the first row containing only zeros
        clusterizable = np.delete(clusterizable, 0, axis=0)

        return clusterizable

    def extract_set_images_by_cluster(self, label):
        new_set = Set("Res Clust")
        setName = str(new_set).split("0x")
        setName = setName[1]
        setName = "Res Clust" + setName[:-1]
        new_set.set_name(setName)
        found = False
        colls = []
        for udcoll in self.get_usable_data_list():
            extracted_data_dictionary = udcoll.get_extracted_data_dict()
            row_cont = 0
            for origin_file in extracted_data_dictionary.keys():
                data_array = extracted_data_dictionary[origin_file]
                for data_rows in range(0, data_array.shape[0]):
                    coll_name= str(label[row_cont])
                    row_cont = row_cont + 1
                    for i in colls:
                        if(i.name == coll_name):
                            found = True
                            if not i.imExists(origin_file.filename):
                                i.add(origin_file)       
                    if not found:
                        c = ImageCollection(coll_name, new_set)
                        c.add(origin_file)
                        colls.append(c)
                    else:
                        found = False
        for i in colls:
            new_set.add_collection(i)
        return new_set



