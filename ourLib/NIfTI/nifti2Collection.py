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
# 14 november 2017 - Initial design and coding.
# 21 november 2017 - Added transformation to jpg
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

	def addNIfTI(self, filename):
		self.niftiFilesList.append(filename)
		self.niftiImageList.append(nib.load(filename))

	def batchAddNIfTIs(self, filenames_array):
		for filename in filenames_array:
			self.addNIfTI(filename)

	def printHeaders(self):
		print('------------'+ self.patientName+' NIfTI Images collection -------------- ')
		i=1
		for niftiImage in self.niftiImageList:
			print('====================== Image '+ str(i) +' header =====================')
			nImHeader=niftiImage.header
			print(nImHeader)
			print('===========================================================')
			i=i+1
