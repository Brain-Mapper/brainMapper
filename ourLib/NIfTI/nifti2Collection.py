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
# 24 november 2017 - Replaced classic lists by a dictionary

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

		## It's better to have a dictionnary, to associate the NIfTI file name and the NIfTI Image instance
		# WARNING : filename MUST be unique, since if we have the same key it will replace the precedent associated value
		self.niftiList=dict()

		self.niftiFilesList=[]
		self.niftiImageList=[]

	## ----- Functions to add NIfTIs from files ----
	def addNIfTIFromFile(self, filename):
		self.niftiList[filename]=nib.load(filename)

	def batchAddNIfTIsFromFiles(self, filenames_array):
		for filename in filenames_array:
			self.addNIfTIFromFile(filename)


	## ----- Functions to add a NIfTI from array -----

	def addNIfTIfromArray(self, newNIfTIfilename, image_array,affine):
		"""This function allows to create a NIfTI2 Image from a data array and add it to the niftiImageList of the class instance
			It requires the new NIfTI2 Image filename (saved for future export), the image data array from which we'll create the image and the affine array, which
			is required by NiBabel and is used to transform given coordinate values into values from a certain coordinate system (for us, usually MNI)"
		"""
		self.niftiList[newNIfTIfilename]=nib.Nifti2Image(image_array,affine)

	## ---- Functions to batch Save the collections' Images
	def batchSaveWholeCollection(self,outputFolderName):

		for outputFile, niftiImage in niftiList.items():
			niftiImage.to_filename(os.path.join(outputFolderName,outputFile))


	## TODO : search how to make the 'mean' of a collection of NIfTI and export to a single file
	# def mergeCollectionIntoOneFile(self,outputFolderName):


	def printHeaders(self):
		print('------------'+ self.patientName+' NIfTI Images collection -------------- ')
		i=1
		for niftiImage in self.niftiList.values():
			print('====================== Image '+ str(i) +' header =====================')
			nImHeader=niftiImage.header
			print(nImHeader)
			print('===========================================================')
			i=i+1
