# NAME
#        image_recreation
#
# DESCRIPTION
#
#
# HISTORY
#
# 14 feb 2018 - Initial design and coding. (@yoshcraft, Raphael A.)

from ourLib.niftiHandlers.imagecollection import ImageCollection
from nibabel import save
from os import path


def image_recreation(folder_path, image_collection):

    for key in image_collection.nifimage_dict.keys():
        name = image_collection.nifimage_dict[key].get_name()

        save(image_collection.nifimage_dict[key].get_nib_image(), path.join(folder_path,path.basename(name).split('.')[0])+".nii.gz")


