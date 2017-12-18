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
# 2 december 2017 - Initial design and coding. (@vz-chameleon, Valentina Z.)
# 16 december 2017 - Modified to encapsulate subset or image collection dict (Raph Agathon)

# Lib dependency imports
from imagecollection import ImageCollection


class Set(object):
    def __init__(self, name):
        self.name = name

        self.subset_dict = dict()
        self.index_subset = 1

        self.collection_dict = dict()
        self.index_collection = 1

    def add(self, a_object):
        if isinstance(a_object, Set):
            self.subset_dict[self.index_subset] = a_object
            self.index_subset = self.index_subset + 1
        elif isinstance(a_object, ImageCollection):
            self.collection_dict[self.index_collection] = a_object
            self.index_collection = self.index_collection + 1
        else:
            raise ValueError('This add method takes a Set or ImageCollection object, but an object of class %s was'
                             'given' % a_object.__class__.__name__)

    def batch_add_subset(self, subsets_array):
        for subset in subsets_array:
            self.add(subset)

    def remove_subset(self, number):
        if number < 0 or number > self.index_subset:
            raise ValueError('No such Subset Index : %d' % number)
        else:
            del self.subset_dict[number]
            self.index_subset = self.index_subset - 1

    def remove_collection(self, number):
        if number < 0 or number > self.index_collection:
            raise ValueError('No such Collection Index : %d' % number)
        else:
            del self.collection_dict[number]
            self.index_collection = self.index_collection - 1

# def export_to_csv(self,filename):
