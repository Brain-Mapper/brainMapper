# NAME
#        nif-image
#
# DESCRIPTION
#
#       'nif-image' contains methods and the class 'ImageCollection' that represent and allow to
#       open, create and save a single NIfTI file
#       It will allow us to have a folder representation of the NIfTI files
#
# HISTORY
#
# 12 december 2017 - Initial design and coding. (Valentina Zelaya, @vz-chameleon)


# System imports
import copy
import os

# Lib dependency imports
import numpy as np
import nibabel as nib
#import nilearn.plotting as nilplot


class NifImage(object):
    # Declare class attributes

    # Initialize instance attributes with empty values because several constructors needed
    def __init__(self, filename=None, nibabel_image=None):
        # type: (str, object) -> NifImage
        self.filename = filename
        self.nib_image = nibabel_image

    @classmethod
    def from_file(cls, one_filename):
        """
           Create a new NifImage from file path
           Nibabel chooses automatically to create a Spatial Image of class NIfTI1 or NIfTI2
           :param one_filename: the path to the .nii file to store
           :return: a NifImage instance
           """
        return cls(one_filename, nib.load(one_filename))

    @classmethod
    def from_array(cls, new_filename, image_data_array, affine, nifti_format=1):
        """
        Create a new NifImage from a data array
        Default format is NIfTI1
        :param new_filename: the new image's filename (for future saving)
        :param image_data_array: the new image's data
        :param affine: the affine transformation matrix (real world -> MNI)
        :param nifti_format: the NIfTI file format required (1 or 2, other values raise error)

        :return: a NifImage instance
        """
        if nifti_format == 2:
            nib_nifti_class = nib.Nifti2Image
        elif nifti_format == 1:
            nib_nifti_class = nib.Nifti1Image
        else:
            raise ValueError('nifti_format must be 1 or 2,  %s was given' % nifti_format)

        return cls(new_filename, nib_nifti_class(image_data_array, affine))

    @classmethod
    def like(cls, new_filename, ref_img, image_data_array, same_header=False):
        """
        :param new_filename: the new image's filename (for future saving)
        :param ref_img: a NifImage instance that will serve as reference
        :param image_data_array: the new image's data
        :param same_header: TRUE if we must use the same header as the ref_img's, FALSE if not (default)

        :return: a new NifImage instance
        """
        affine = ref_img.get_affine_matrix()

        header = None
        if same_header:
            header = copy.deepcopy(ref_img.get_header)

        nib_nifti_class = ref_img.get_img_class()

        return cls(new_filename, nib_nifti_class(image_data_array, affine, header=header))

    def set_filename(self, new_filename):
        self.filename = new_filename

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
        img_data = np.array(copy.deepcopy(self.nib_image.get_data()))

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

    def is_binary_image(self):
        return np.array_equal(self.nib_image.get_data(), self.get_copy_img_data().astype(bool))

    def save_to_file(self, folder_path):
        self.nib_image.to_filename(os.path.join(folder_path, self.filename))

##    def plot_img(self):
##        nilplot.plot_img(self.nib_image, title=self.filename)
##        nilplot.show()
##
##    def plot_glass(self):
##        nilplot.plot_glass_brain(self.nib_image, title="Glass brain plot")
##        nilplot.show()

    def get_img_data(self):
        data = self.nib_image.get_data()
        data = np.transpose(data, [2,0,1])
        d2 = np.empty(data.shape + (4,), dtype=np.ubyte)
        d2[..., 0] = data * (255./(data.max()/1))
        d2[..., 1] = d2[..., 0]
        d2[..., 2] = d2[..., 0]
        d2[..., 3] = d2[..., 0]
        d2[..., 3] = (d2[..., 3].astype(float) / 255.)**2 * 255

        # RGB orientation lines (optional)
        d2[:, 0, 0] = [255, 0, 0, 255]
        d2[0, :, 0] = [0, 255, 0, 255]
        d2[0, 0, :] = [0, 0, 255, 255]
        return d2
