# NAME
#        nif-image
#
# DESCRIPTION
#
#       'nif-image' contains methods and the class 'ImageCollection' that represent and allow to
#       open and save a single NIfTI file
#       It will allow us to store image data and other information as in-memory representations
#       of the users' NIfTI files
#
# HISTORY
#
# 2 december 2017 - Initial design and coding. (@vz-chameleon, Valentina Z.)


# System imports
import copy

# Lib dependency imports
import numpy as np
import nibabel as nib


class NifImage(object):
    # Declare class attributes

    # Initialize instance attributes
    def __init__(self, filename, nibabel_image):
        # type: (str, str, object) -> NifImage
        self.filename = filename
        self.nib_image = nibabel_image

    def set_filename(self, new_filename):
        self.filename=new_filename

    def get_affine_matrix(self):
        """
        Return the NIfTI images' affine
        An affine is the matrix that allows to pass from real world coordinates to
        the image coordinates (here, to MNI coordinates)
        :return: array
        """
        return self.nib_image.affine

    def get_header(self):
        return self.nib_image.header

    def get_img_class(self):
        return self.nib_image.__class__

    def get_copy_img_data(self, finite_values=False):
        """
        Get the image data safely by using copy.deepcopy() so that if we modify
        the data, it won't affect the original image
        :param finite_values: FALSE if NaN and inf values in data array must be kept,
                                TRUE if NaN and inf are to be replaced by 0
        :return: array
        """
        img_data = copy.deepcopy(self.nib_image.get_data())

        # Some nifti images have NaN and inf as data values...
        if finite_values:
            infinite_values_mask = np.logical_not(np.isfinite(img_data))
            img_data[infinite_values_mask] = 0

        return img_data

    def get_info(self):
        info = ""
        try:
            info = "Location : %s\nSpatial Image : %s\n(\n shape=%s,\n affine=%s\n)" % \
                   (self.filename,
                    self.nib_image.__class__.__name__,
                    repr(self.nib_image.shape),
                    repr(self.nib_image.affine))
        except:
            pass
        return info

    def save_to_file(self):
        self.nib_image.to_filename(self.filename)


# ----- METHODS THAT USE OR CREATE NifImages -----

# Create a NifImage from a filename
def create_img_from_file(one_filename):
    """
    Create a nibabel NIfTI1|2Image from file and store filename
    :param one_filename: the path to the .nii file to store
    :return: NifImage instance
    """
    return NifImage(one_filename, nib.load(one_filename))


def create_img_from_array(new_filename,image_data_array, affine, nifti_format=1):
    if nifti_format == 2:
        nib_nifti_class = nib.Nifti2Image
    elif nifti_format == 1:
        nib_nifti_class = nib.Nifti1Image
    else:
        raise ValueError('nifti_format must be 1 or 2,  %s was given' % nifti_format)

    return NifImage(new_filename, nib_nifti_class(image_data_array, affine))


def create_img_like(new_filename,ref_img,new_data,same_header):
    affine=ref_img.get_affine_matrix()

    header=None
    if same_header:
        header=copy.deepcopy(ref_img.get_header())

    nib_nifti_class = ref_img.get_img_class()

    return NifImage(new_filename, nib_nifti_class(new_data,affine,header=header))