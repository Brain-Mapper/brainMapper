# System imports
import os
import sys
import string


# Lib dependency imports
import numpy as np
import nibabel as nib

# Our own modules import
from . import nifti2Collection as nifcoll 


filenames=[]
filenames.append('P92_SA_RMN_1.nii')
filenames.append('P92_UL_M0_1.nii')

collection= nifcoll(filenames)
collection.printHeaders()
