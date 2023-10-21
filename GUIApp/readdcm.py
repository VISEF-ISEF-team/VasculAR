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
        
    # define a function that returns the number in the file name
    def get_number(self, file):
        # use regular expression to find the digits in the file name
        match = re.search("\d+", file)
        # if there is a match, return the integer value of the digits
        if match:
            return int(match.group())
        # otherwise, return zero
        else:
            return 0

    def read(self):
        list_files = os.listdir(self.path)
        # sort the list of files by using the get_number function as the key
        list_files.sort(key=self.get_number)

        img = []
        for index in range(len(list_files)):
            if list_files[index].endswith('.dcm'):
                input = dcmread(self.path + '/' + list_files[index])
                input_array = input.pixel_array
                if len(input_array.shape) == 3: 
                    continue
                img.append(input_array)
            
        img = np.array(img)
        return img
    
    def convert_dcm_nii(self):
        img = self.read()
        converted_array = np.array(img, dtype=np.float32)
        converted_array = np.transpose(converted_array, (2,1,0))
        affine = np.eye(4)
        nifti_file = nib.Nifti1Image(converted_array, affine)
        nib.save(nifti_file, self.path + '/saved.nii.gz')
        img_raw = sitk.ReadImage(self.path + '/saved.nii.gz', sitk.sitkFloat32)
        img = sitk.GetArrayFromImage(img_raw)
        print(img.shape)
        
    def visualize(self):
        img = self.read()
        converted_array = np.transpose(img, (2,1,0))
        print(converted_array.shape)
        plt.imshow(converted_array[:,:, 300])
        plt.show()
        
instance = ReadDCM('D:\Downloads\VNRealData')
instance.visualize()
