from pydicom import dcmread
import numpy as np
import os
import matplotlib.pyplot as plt
import re
import nibabel as nib
import SimpleITK as sitk


class ReadDCM:
    def __init__(self, path):
        self.path = path

    def get_number(self, file):
        match = re.search("\d+", file)
        if match:
            return int(match.group())
        else:
            return 0

    def load_scan(self):
        slices = [dcmread(self.path + '/' + s) for s in os.listdir(self.path)]
        slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
        try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        for s in slices:
            s.SliceThickness = slice_thickness
        return slices


    def get_pixels_hu(self, slices):
        image = np.stack([s.pixel_array for s in slices])
        image = image.astype(np.int16)
        image[image == -2000] = 0
        for slice_number in range(len(slices)):
            intercept = slices[slice_number].RescaleIntercept
            slope = slices[slice_number].RescaleSlope
            if slope != 1:
                image[slice_number] = slope * image[slice_number].astype(np.float64)
                image[slice_number] = image[slice_number].astype(np.int16)
            image[slice_number] += np.int16(intercept)  
        return np.array(image, dtype=np.int16)

    
    def convert_dcm_nii(self):
        # Read Volumn
        img = self.load_scan()
        img = self.get_pixels_hu(img)
        
        file = os.listdir(self.path)
        dict_info = {}
    
        # Read information
        input = dcmread(self.path + '/' + file[0])
        list_info = [['0x0010', '0x0010'], ['0x0008', '0x0060'], ['0x0010', '0x0020'], ['0x0018', '0x0015'], ['0x0008', '0x0022']]
        for i in range(len(list_info)):
            if (list_info[i][0], list_info[i][1]) in input:
                category = input[list_info[i][0], list_info[i][1]]
                dict_info[category.name] = category.value
        
        converted_array = np.array(img, dtype=np.float32)
        converted_array = np.transpose(converted_array, (2,1,0))
        affine = np.eye(4)
        nifti_file = nib.Nifti1Image(converted_array, affine)
        nib.save(nifti_file, self.path + '/patient.nii.gz')
        img_raw = sitk.ReadImage(self.path + '/patient.nii.gz', sitk.sitkFloat32)
        img = sitk.GetArrayFromImage(img_raw)
        return img_raw, img, dict_info
        
    def save_nii(self, path_to_save, nifti_file):
        nib.save(nifti_file, path_to_save + '/patient.nii.gz')
        img_raw = sitk.ReadImage(path_to_save + '/patient.nii.gz', sitk.sitkFloat32)
        img = sitk.GetArrayFromImage(img_raw)
        print(img.shape)
