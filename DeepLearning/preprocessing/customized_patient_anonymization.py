import pydicom as dicom
from glob import glob
from tqdm import tqdm
import os

# Function to anonymize dicom file
def anonymize_dcm(in_path, out_path, patient_name="Anonymous"):
    dcm_file = dicom.dcmread(in_path)
    dcm_file.PatientName = patient_name
    dcm_file.save_as(out_path)
    
# # Function to anonymize dicom file
# def anonymize_all_patients():
#     all_patients = os.listdir('../data/PatientsDCM')
#     for patient in all_patients:
#         path_to_folder_dicoms = "../data/PatientsDCM/" + patient + "/*"
#         for slice_ in tqdm(glob(path_to_folder_dicoms)):
#             anonymize_dcm(slice_, slice_)



path_to_folder_dicoms = "../data/PatientsDCM/PAT016/*"
for slice_ in tqdm(glob(path_to_folder_dicoms)):
    anonymize_dcm(slice_, slice_)