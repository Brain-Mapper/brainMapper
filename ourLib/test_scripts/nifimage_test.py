if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from niftiHandlers.nifimage import NifImage
    else:
        from ..niftiHandlers.nifimage import NifImage

ni_patient = NifImage.from_file('ImagesTest/Image_patient.nii')
ni1 = NifImage.from_file('ImagesTest/P92_SA_RMN_1.nii')
ni2 = NifImage.from_file('ImagesTest/P92_SA_RMN_1.nii')
ni3 = NifImage.from_file('ImagesTest/P92_UL_M0_1.nii')
ni4 = NifImage.from_file('ImagesTest/P92_UL_M0_1.nii')
ni5 = NifImage.from_file('ImagesTest/P92_F_M0_1.nii')

# print affine matrices
print(ni1.get_affine_matrix())
print(ni2.get_affine_matrix())
print(ni3.get_affine_matrix())
print(ni4.get_affine_matrix())
print(ni_patient.get_affine_matrix())
print(ni5.get_affine_matrix())

# print NifTi class or format
print(ni1.get_img_class())
print(ni2.get_img_class())
print(ni3.get_img_class())
print(ni4.get_img_class())
print(ni_patient.get_img_class())

#print data
print(ni_patient.get_copy_img_data())

## Testing if given image contains only 0 and 1
print('patient binary ? '+ str(ni_patient.is_binary_image()))  #expected :false

print('P92_UL_RMI1 binary ? '+ str(ni3.is_binary_image()))     #expected : true

# Masking and fast extraction
mask = ni3.get_copy_img_data(True)>0
print(mask)
us_data=ni3.get_copy_img_data(True)[mask].T
print(us_data)






