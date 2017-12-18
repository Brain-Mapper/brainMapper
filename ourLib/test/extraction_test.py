import time

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path

        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from dataExtraction import extractor as xt
        from niftiHandlers.nifimage import NifImage
        from niftiHandlers.imagecollection import ImageCollection
    else:
        from ..dataExtraction import extractor as xt
        from ..niftiHandlers.nifimage import NifImage
        from ..niftiHandlers.imagecollection import ImageCollection


mni_template = NifImage.from_file('ImagesTest/Template_mni_icbm_152.nii')
ni_patient = NifImage.from_file('ImagesTest/Image_patient.nii')
ni1 = NifImage.from_file('ImagesTest/P92_SA_RMN_1.nii')
ni2 = NifImage.from_file('ImagesTest/P92_SA_RMN_1.nii')
ni3 = NifImage.from_file('ImagesTest/P92_UL_M0_1.nii')
ni4 = NifImage.from_file('ImagesTest/P92_UL_M0_2.nii')
ni5 = NifImage.from_file('ImagesTest/P92_F_M0_1.nii')
ni6 = NifImage.from_file('ImagesTest/P92_F_M0_2.nii')
ni7 = NifImage.from_file('ImagesTest/P92_UL_RMN_1.nii')
ni8 = NifImage.from_file('ImagesTest/P92_UL_RMN_2.nii')

imgc_4 = ImageCollection()
imgc_4.add(ni7)
imgc_4.add(ni8)

start_time = time.time()  # To time extraction
extracted_data_ni7 = xt.extract(ni7)
print(extracted_data_ni7)
print("Extraction from single nifti file '"+ ni7.filename +"' in ---- %s seconds ----" % (time.time() - start_time))


start_time = time.time()  # To time extraction
extracted_data_coll4 = xt.extract_from_collection(imgc_4)
print(extracted_data_coll4)
print("Extraction from collection (size : 2) in ---- %s seconds ----" % (time.time() - start_time))