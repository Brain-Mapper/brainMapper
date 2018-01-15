# NAME
#        set
#
# DESCRIPTION
#
#       'set' contains methods and the class 'Set' that represent a collection of 'ImageCollection' and a collection
#       of 'Set'
#       It will allow us to store image data and other information as in-memory representations
#       of the users' NIfTI files
#
# HISTORY
#
# 28 december 2017 - Initial design and coding. (@yoshcraft, Raphael A.)
# 8 january 2018 - Creation of the generate_from_folder class method. (@yoshcraft, Raphael A.)

# Lib dependency imports
from imagecollection import ImageCollection
from nifimage import NifImage
import os

class Set(object):

    def __init__(self, name):
        """
        Constructor of the Set Class.
        :param name: name (String) of the Set.
        The Set contains two dictionary. The Goal of this representation is to make a folder/file like.
        subset_dict is a dictionary of Set, like list of folders.
        collection_dict is a dictionary of ImageCollection, like list of files.
        For the dictionaries, keys are the name the object linked.
        """
        self.name = name
        self.subset_dict = dict()
        self.collection_dict = dict()

    def add_empty_subset(self, name):
        """
        Method to create a empty subset into the Set.
        :param name : name (String) of the new subset.
        control if the name doesn't exist in subset_dict.
        """
        if name not in self.subset_dict.keys():
            self.subset_dict[name] = Set(name)
        else:
            print('The Subset name : %s already exist' % name)

    def add_empty_collection(self, name):
        """
        Method to create a empty image collection into the Set.
        :param name: name of the new ImageCollection.
        control if the name doesn't exist in collection_dict.
        """
        if name not in self.collection_dict.keys():
            self.collection_dict[name] = ImageCollection(name)
        else:
            print('The Image Collection name : %s already exist' % name)

    def add_subset(self, subset):
        """
        Method to add an existing Set.
        :param subset: objet from the Set Class.
        control if the subset name doesn't exist in subset_dict.
        """
        if subset.get_name not in self.subset_dict.keys():
            self.subset_dict[subset.get_name()] = subset
        else:
            print('The Subset name : %s already exist' % subset.get_name)

    def add_collection(self, collection):
        """
        Method to add an existing ImageCollection.
        :param collection: object from the ImageCollection Class.
        control if the collection name doesn't exist in collection_dict.
        """
        if collection.get_name() not in self.collection_dict.keys():
            self.collection_dict[collection.get_name()] = collection
        else:
            print('The Image Collection name : %s already exist' % collection.get_name)

    def batch_add_subset(self, subsets_array):
        """
        Method to add several Set at the same time using the add_subset method.
        :param subsets_array: array of Set to add into subset_dict.
        """
        for subset in subsets_array:
            self.add_subset(subset)

    def batch_add_collection(self, collection_array):
        """
        Method to add several ImageColection at the same time using the add_collection method.
        :param collection_array: array of ImageColletion to add into collection_dict.
        """
        for collection in collection_array:
            self.add_collection(collection)

    def remove_subset(self, name):
        """
        Method to remove a subset from subset_dict.
        :param name: name set to remove.
        """
        del self.subset_dict[name]

    def remove_collection(self, name):
        """
        Method to remove a collection from collection_dict.
        :param name: Set of the set to remove.
        """
        del self.collection_dict[name]

    def batch_remove_subset(self,subsets_array):
        """
        Method to remove several subset using remove subset_method.
        :param subsets_array: array of Set to remove from subset_dict.
        """
        for subset in subsets_array:
            self.remove_subset(subset)

    def batch_remove_collection(self,collection_array):
        """
        Method to remove several subset using remove collection_method.
        :param collection_array: array of ImageCollection to remove from collection_dict.
        """
        for collection in collection_array:
            self.remove_collection(collection)

    def get_name(self):
        """
        Getter for the name parameter.
        :return: name
        """
        return self.name

    def get_all_nifti_set(self):
        """
        Function to make a list of all the nifti image from collection-dict.
        :return: list of all the niftiImage of the Set. Don't take the nifti image of the subset.
        """
        all_collection = list()
        for collection in self.collection_dict.values():
            all_collection.append(collection)
        return all_collection

    def get_all_nifti_set_and_subset(self):
        """
        Function to make a list of all the nifti image of the Set.
        :return: list of all the nifti image of the Set and all its subset.
        """
        all_collection = self.get_all_nifti_set()
        for subset in self.subset_dict.values():
            all_collection.extend(subset.get_all_nifti_set_and_subset())
        return all_collection

    def number_of_subset(self):
        """
        Function to have the number of subset.
        :return: the number of subset.
        """
        return len(self.subset_dict.keys())

    def number_of_collection(self):
        """
        Function to have the number of collection.
        :return: the number of collection.
        """
        return len(self.collection_dict.keys())

    # TODO remove all the hidden file
    @classmethod
    def generate_from_folder(cls, set,  folder_path):
        """
        Method to build the all structure from a folder.
        :param folder_path: folder witch contains the needed data.
        """
        list = os.listdir(folder_path)
        for item in list:
            if item != '.DS_Store':
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    item_list = os.listdir(item_path)
                    # case for the set
                    n = 0
                    for sub_item in item_list:
                        n = n + os.path.isfile(os.path.join(item_path, sub_item))
                    # 1 because whe have one hidden file
                    if n == 1:
                        set.add_empty_subset(item)
                        set.generate_from_folder(set.subset_dict[item], item_path)
                    # case for the imageCollection
                    elif n == len(item_list):
                        set.add_empty_collection(item)
                        for sub_item in item_list:
                            if sub_item != '.DS_Store':
                                set.collection_dict[item].add(NifImage.from_file(os.path.join(item_path, sub_item)))

    def set_name(self,name):
        self.name = name

    def get_sub_set(self,name):
        for i in self.subset_dict.values():
            if(i.name == name):
                return i
        return None

    def get_coll(self):
        return self.collection_dict
