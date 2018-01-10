# NAME
#
#        image-collection
#
# DESCRIPTION
#
#       'image-collection' contains methods and the class 'ImageCollection' that represent
# 		a -series of NIfTI 2 Images that were loaded by the user
# 		(often associated to one patient, but this is optional)
# 		and that allows to have a group of in-memory representations of NIfTI Images
#    	(see nif-image.py)
#
# HISTORY
#
# 22 november 2017- Initial design and coding. (@vz-chameleon, Valentina Z.)
# 24 november 2017- Replaced classic lists by a dictionary (@vz-chameleon, Valentina Z.)
# 2 december 2017- Changed paradigms to include NifImage objects (@vz-chameleon, Valentina Z.)
# 28 decembre 2017- Rework with no use of index to fit the Set implementation (@yoshcraft, Raphael A.)


# Lib dependency imports
from nifimage import NifImage


class ImageCollection(object):
    def __init__(self, name):
        # It's better to have a dictionary, to associate an ID (here, just a name)
        # and the NIfTI Image instance
        self.nifimage_dict = dict()
        self.name = name

    def add(self, a_nif_image):
        """
        Method to add a nifimage to the dictionary
        :param a_nif_image:
        """
        self.nifimage_dict[a_nif_image.filename] = a_nif_image

    def remove(self, name):
        """
        Method to remove a nifimage from the dictionary
        :param name: name (file name) of the nifimage
        :return:
        """
        del self.nifimage_dict[name]

    def add_from_file(self, filename):
        """
        Method to add a nifimage from a file name to the dictionary
        :param filename:
        :return:
        """
        self.nifimage_dict[filename] = NifImage.from_file(filename)

    def batch_add_from_files(self, filenames_array):
        for filename in filenames_array:
            self.add_from_file(filename)

    def batch_save_collection(self, output_folder):
        for nifImage in self.nifimage_dict.values():
            nifImage.save_to_file(output_folder)

    def get_name(self):
        return self.name

    def get_img_list(self):
        return self.nifimage_dict

    def set_name(self, new):
        self.name = new
    
