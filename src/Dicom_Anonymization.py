import pydicom as dicom
from glob import glob
from tqdm import tqdm
import os

path = "../data/dicom/PAT034/D0024.dcm"

file = dicom.dcmread(path)
print(file.PatientName)
print(file.PatientBirthDate)

'''
file.PatientName = "Anonymous"
out_path_dicom_saved = "anony_slice.dcm"
file.save_as(out_path_dicom_saved)

path = "anony_slice.dcm"
file = dicom.dcmread(path)
print(file.PatientName)
'''


# Function to anonymize dicom file
def anonymize_dcm(in_path, out_path, patient_name="Anonymous"):
    dcm_file = dicom.dcmread(in_path)
    dcm_file.PatientName = patient_name
    dcm_file.save_as(out_path)
    
        
def anonymize_all_patients():
    all_patients = os.listdir()
    # path_to_folder_dicoms = "../data/dicom/PAT034/*"
    # for slice_ in tqdm(glob(path_to_folder_dicoms)):
    #     anonymize_dcm(slice_, slice_)