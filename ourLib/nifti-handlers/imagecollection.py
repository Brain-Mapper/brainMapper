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


# Lib dependency imports
from nifimage import NifImage


class ImageCollection(object):
    def __init__(self):
        # It's better to have a dictionnary, to associate an ID (here, just a number)
        # and the NIfTI Image instance
        # WARNING ! 'ID' MUST be unique, since if we have the same key it will
        # replace the precedent associated value
        self.nifimage_dict = dict()
        self.index = 1

    def add(self, a_nif_image):
        if isinstance(a_nif_image,NifImage):
            self.nifimage_dict[self.index] = a_nif_image
            self.index = self.index + 1  # IMPORTANT !!
        else:
            raise ValueError('Image Collection takes NifImages, an object of class %s was '
                             'given'% a_nif_image.__class__.__name__ )

    def remove(self, number):
        del self.nifimage_dict[number]

    def add_from_file(self, filename):
        self.nifimage_dict[self.index] = NifImage.from_file(filename)
        self.index = self.index + 1  # IMPORTANT !!

    def batch_add_from_files(self, filenames_array):
        for filename in filenames_array:
            self.add_from_file(filename)

    def add_from_array(self, img_name, data_array, affine, nif_format=1):
        self.nifimage_dict[self.index] = NifImage.from_array(img_name, data_array, affine, nif_format)
        self.index = self.index + 1  # IMPORTANT !!

    def add_one_like(self, img_name, ref_nif_img, data_array, copy_header=False):
        self.nifimage_dict[self.index] = NifImage.like(img_name, ref_nif_img, data_array, copy_header)
        self.index = self.index + 1  # IMPORTANT !!

    def batch_save_collection(self, output_folder):
        for nifImage in self.nifimage_dict.values():
            nifImage.save_to_file(output_folder)

    def batch_save_n_images(self, indexes_array, output_folder):
        if len(indexes_array) > len(self.nifimage_dict):
            raise ValueError('specified parameters number is bigger than collection size')
        else:
            for i in indexes_array :
                self.nifimage_dict[i].save_to_file(output_folder)