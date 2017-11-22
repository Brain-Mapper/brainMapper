# NAME
#
#        nifti2Collection
#
# DESCRIPTION
#
#        'nifti2Collection' is a class that represents a series of NIfTI 2 Images that w
#
# HISTORY
#
# 22 november 2017 - Initial design and coding.
#

# System imports
import os
import sys
import string

# Lib dependency imports
import numpy as np
import nibabel as nib


class nifti2Collection(object):

	def __init__(self, aPatientName):
		self.patientName=aPatientName
		self.niftiFilesList=[]
		self.niftiImageList=[]

	## ----- Functions to add NIfTIs from files ----
	def addNIfTIFromFile(self, filename):
		self.niftiFilesList.append(filename)
		self.niftiImageList.append(nib.load(filename))

	def batchAddNIfTIsFromFiles(self, filenames_array):
		for filename in filenames_array:
			self.addNIfTIFromFile(filename)


	## ----- Functions to add a NIfTI from array -----

	def addNIfTIfromArray(self, newNIfTIfilename, image_array,affine):
		"""This function allows to create a NIfTI2 Image from a data array and add it to the niftiImageList of the class instance
			It requires the new NIfTI2 Image filename (saved for future export), the image data array from which we'll create the image and the affine array, which
			is required by NiBabel and is used to transform given coordinate values into values from a certain coordinate system (for us, usually MNI)"
		 """
		self.niftiFilesList.append(newNIfTIfilename)
		self.niftiImageList.append(nib.Nifti2Image(image_array,affine))

	## ---- Functions to batch Save the collections' Images
	def batchSaveWholeCollection(self,outputFolderName):
		i=1
		for niftiImage in self.niftiImageList:
			outputFile=patientName+'_NIfTIPoints'+str(i)
			niftiImage.to_filename(os.path.join(outputFolderName,outputFile))
			i=i+1

	## TODO : search how to make the 'mean' of a collection of NIfTI and export to a single file
	# def mergeCollectionIntoOneFile(self,outputFolderName):





	def printHeaders(self):
		print('------------'+ self.patientName+' NIfTI Images collection -------------- ')
		i=1
		for niftiImage in self.niftiImageList:
			print('====================== Image '+ str(i) +' header =====================')
			nImHeader=niftiImage.header
			print(nImHeader)
			print('===========================================================')
			i=i+1
