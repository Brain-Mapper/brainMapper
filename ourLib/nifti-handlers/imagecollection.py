# NAME
#
#        image-collection
#
# DESCRIPTION
#
#       'image-collection' contains methods and the class 'ImageCollection' that represent
# 		a series of NIfTI 2 Images that were loaded by the user
# 		(often associated to one patient, but this is optional)
# 		and that allows to have a group of in-memory representations of NIfTI Images
#    	(see nif-image.py)
#
# HISTORY
#
# 22 november 2017- Initial design and coding. (@vz-chameleon, Valentina Z.)
# 24 november 2017- Replaced classic lists by a dictionary (@vz-chameleon, Valentina Z.)
# 2 december 2017- Changed paradigms to include NifImage objects (@vz-chameleon, Valentina Z.)

# System imports
import os

# Lib dependency imports
import nibabel as nib
from nifimage import NifImage


class ImageCollection(object):

    def __init__(self):
        # It's better to have a dictionnary, to associate an ID (here, just a number) and the NIfTI Image instance
        # WARNING ! 'ID' MUST be unique, since if we have the same key it will replace the precedent associated value
        self.nifimage_dict = dict()
		self.index=1;

    def add_from_file(self, filename):
        self.nifimage_dict[self.index] = NifImage(filename);

    def batchAddNIfTIsFromFiles(self, filenames_array):
        for filename in filenames_array:
            self.addNIfTIFromFile(filename)

    ## ----- Functions to add a NIfTI from array -----

    def addNIfTIfromArray(self, newNIfTIfilename, image_array, affine):
        """This function allows to create a NIfTI2 Image from a data array and add it to the niftiImageList of the class instance
			It requires the new NIfTI2 Image filename (saved for future export), the image data array from which we'll create the image and the affine array, which
			is required by NiBabel and is used to transform given coordinate values into values from a certain coordinate system (for us, usually MNI)"
		"""
        self.niftiList[newNIfTIfilename] = nib.Nifti2Image(image_array, affine)

    ## ---- Functions to batch Save the collections' Images
    def batchSaveWholeCollection(self, outputFolderName):

        for outputFile, niftiImage in niftiList.items():
            niftiImage.to_filename(os.path.join(outputFolderName, outputFile))

    ## TODO : search how to make the 'mean' of a collection of NIfTI and export to a single file
    # def mergeCollectionIntoOneFile(self,outputFolderName):


    def printHeaders(self):
        print('------------' + self.patientName + ' NIfTI Images collection -------------- ')
        i = 1
        for niftiImage in self.niftiList.values():
            print('====================== Image ' + str(i) + ' header =====================')
            nImHeader = niftiImage.header
            print(nImHeader)
            print('===========================================================')
            i = i + 1
