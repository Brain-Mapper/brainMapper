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
from numpy import zeros

from nibabel import Nifti1Image,load
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
    """
    A data structure for containing all relevant information in a usable format for calculations and clustering
    from ImageCollection instances
    """
    def __init__(self, an_imgcollection_name):

        # The image coll ID from which the data comes
        self.imgcoll_origin = an_imgcollection_name
        # A dictionary to contain the pair key: name of file of origin (ex: 'P92_UL_MN0.nii'),
        #                                  value : usable data array (numpy array containing extracted data)
        self.extracted_data_dict = dict()
        self.rownum = 0

    def add_extracted_data_entry(self, origin_filename, usable_data_array):
        """
        Add an entry to the usable data collection
        :param origin_filename: The filename from which the data comes
        :param usable_data_array: a shape=(lines x 4) array to add to the structure
        :return:
        """
        # Check whether the given array passed in argument has 4 columns (X,Y,Z, Intensity)
        colnum=(usable_data_array.shape)[1]
        if (colnum > 4) or (colnum < 4):
            raise ValueError('UsableDataCollection.addExtracted_data_entry : array given as argument'
                             ' has more or less than 4 columns')

        self.rownum = self.rownum + (usable_data_array.shape)[0]
        self.extracted_data_dict[origin_filename] = usable_data_array

    def remove_extracted_data_entry(self, origin_filename):
        """
        Remove the data entry coming from a specific NIfTI file
        :param origin_filename: The filename from which the data comes
        :return: Nothing
        """
        del self.extracted_data_dict[origin_filename]

    def get_imgcoll_name(self):
        return self.imgcoll_origin

    def get_extracted_data_dict(self):
        return self.extracted_data_dict

    def get_row_num(self):
        return self.rownum

    def export_as_clusterizable(self):
        """
        Export a single array using all others to the format used by scikit-learn lib clustering algorithms
        :return: An array with several lines and 4 columns stacked to be used with sklearn algorithms
        """
        clusterizable = np.zeros(shape=(1, 4))  # An empty line of zeros to start with
        for data_array in self.extracted_data_dict.values():
            clusterizable = np.concatenate((clusterizable, data_array), axis=0)

        # Delete the first row containing only zeros
        clusterizable = np.delete(clusterizable, 0, axis=0)

        return clusterizable


class UsableDataSet(object):
    """
    A data structure for keeping extracted data to be used in calculations and clustering
    """
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
        """
        Export this data structure as an array that can be used in scikit-learn clustering algorithms
        :return: a list of n_features-dimensional data (each row corresponds to a single data point)
        """
        clusterizable = np.zeros(shape=(1, 4))  # An empty line of zeros to start with

        for udcoll in self.usable_data_list:
            clusterizable = np.concatenate((clusterizable, udcoll.export_as_clusterizable()), axis=0)

        # Delete the first row containing only zeros
        clusterizable = np.delete(clusterizable, 0, axis=0)

        return clusterizable

    def extract_set_images_by_cluster(self, label, template_mni_path):
        new_set = Set("Clust")
        setName = str(new_set).split("0x")
        setName = setName[1]
        setName = "Clust" + setName[:-1]
        new_set.set_name(setName)
        found = False        
        colls = []
        point_dict = dict()
        template_data = load(template_mni_path)
        template_affine = template_data.affine
        template_shape = template_data.shape
        
        for udcoll in self.get_usable_data_list():
            extracted_data_dictionary = udcoll.get_extracted_data_dict()
            row_cont = 0
            for origin_file in extracted_data_dictionary.keys():
                data_array = extracted_data_dictionary[origin_file]
                for data_rows in range(0, data_array.shape[0]):
                    point = [int(float(data_array[data_rows, 0])), int(float(data_array[data_rows, 1])), int(float(data_array[data_rows, 2])), int(float(data_array[data_rows, 3]))]
                    coll_name= str(label[row_cont])
                    row_cont = row_cont + 1
                    for i in colls:
                        if(i.name == coll_name):
                            found = True
                            point_dict[coll_name].append(point)
                    if not found:
                        c = ImageCollection(coll_name, new_set)
                        point_dict[coll_name] = []
                        point_dict[coll_name].append(point)
                        colls.append(c)
                    else:
                        found = False
        # recreate nifti image from this points
        for key in point_dict.keys():
            print key
            recreate_affine = template_affine
            recreate_data = zeros(template_shape)

            for point in point_dict[key]:
                recreate_data[point[0], point[1], point[2]] = point[3]

            recreate_image = Nifti1Image(recreate_data, recreate_affine)
            ni_image = NifImage(key + ".nii", recreate_image)

            for c in colls:
                if(str(key) == c.name):
                    # put nifti images into a imageCollection
                    c.add(ni_image)
            
        for i in colls:
            new_name = str(i).split("0x")
            new_name = new_name[1]
            new_name = str(i.name)+"_"+ new_name[:-1]
            i.set_name(new_name)
            new_set.add_collection(i) 
        return new_set

    def extract_points(self, label):
        def make_colors(n):
            import random
            col_dict = dict()
            for i in range(0, n):
                col= (random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1),1)
                col_dict[str(i)] = col
            return col_dict
        colors = make_colors(len(label))
        l = len(label)
        pos = np.empty((l, 3))
        size = np.empty((l))
        color = np.empty((l,4))
        for udcoll in self.get_usable_data_list():
            extracted_data_dictionary = udcoll.get_extracted_data_dict()
            row_cont = 0
            for origin_file in extracted_data_dictionary.keys():
                data_array = extracted_data_dictionary[origin_file]
                for data_rows in range(0, data_array.shape[0]):
                    pos[row_cont] = (int(float(data_array[data_rows, 0])), int(float(data_array[data_rows, 1])), int(float(data_array[data_rows, 2]))); size[row_cont] =5 ; color[row_cont] = colors[str(label[row_cont])]
                    row_cont = row_cont + 1
        res = [pos,size,color]
        return res
