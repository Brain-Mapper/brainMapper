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

	def __init__(self, filenames):
		for file in filenames :
			self.NiftiList.append(nib.load(file))
	
	def printHeaders():
		for niftiImage in self.NiftiList :
			print(niftiImage.header+"\n ----------------- \n")