import customtkinter
import SimpleITK as sitk
import numpy as np

class filtering:
    def __init__(self, segmentation): 
        self.segmentation=segmentation
        
    def get(self):
        array_1d = self.segmentation.flatten()
        unique_values, counts = np.unique(array_1d, return_counts=True)
        label_arrays = []
        for value in unique_values: 
            label_array = np.copy(self.segmentation) 
            label_array = np.where(label_array==value, label_array, 0)
            label_arrays.append(label_array)
        return label_arrays
            

            
         