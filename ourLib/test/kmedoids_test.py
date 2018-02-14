import time

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path

        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from ourLib import clustering as clust
        from ourLib.dataExtraction import extractor as xt
        from ourLib.niftiHandlers.nifimage import NifImage
        from ourLib.niftiHandlers.imagecollection import ImageCollection
    else:
        from ..dataExtraction import extractor as xt
        from ..niftiHandlers.nifimage import NifImage
        from ..niftiHandlers.imagecollection import ImageCollection


#---- Load NIfTI Images -----
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


# --- Image Collections ------------
imgc_1 = ImageCollection()
imgc_1.set_label('P92_SA_RMN')
imgc_1.add(ni1)
imgc_1.add(ni2)

imgc_2 = ImageCollection()
imgc_2.set_label('P92_UL_M0')
imgc_2.add(ni3)
imgc_2.add(ni4)

imgc_3 = ImageCollection()
imgc_3.set_label('P92_F_M0')
imgc_3.add(ni5)
imgc_3.add(ni6)

imgc_4 = ImageCollection()
imgc_4.set_label('P92_UL_RMN')
imgc_4.add(ni7)
imgc_4.add(ni8)

imgc_list = [imgc_1, imgc_2, imgc_3, imgc_4]

# ------ List of collection's extraction test-------------
start_time = time.time()  # To time extraction
extracted_dataset = xt.extract_from_collection_list_using_centroids(imgc_list)
print("----------------------------------------------------------------------")
print("Extraction from coll list (size : 4) in ---- %s seconds ----" % (time.time() - start_time))
print("Obtained object : "+ str(extracted_dataset))
print("Extracted data (clusterizable) using centroids: " + str(extracted_dataset.export_as_clusterizable()))
print("----------------------------------------------------------------------")


# ------ Perform K_medoids ----------

clust.perform_kmedoids({"n_clusters": "3", "metric": "euclidian"}, extracted_dataset)


