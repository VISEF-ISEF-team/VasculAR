from pydicom import dcmread
import numpy as np
import os

path = 'D:/Downloads/VnRealData'
input = dcmread(path + '/' + 'File0.dcm')
input_2 = dcmread('D:/Documents/GitHub/VascuIAR/DeepLearning/data/PatientsDCM/PAT001/D0001.dcm')

patient_name = input[0x0010, 0x0010]
patient_name_2 = input_2[0x0010, 0x0010]

if patient_name.name == "Patient's Name":
    print(patient_name.value)
    
if patient_name_2.name == "Patient's Name":
    print(patient_name_2.value)

acquisition_date = input[0x0008, 0x0022]
if acquisition_date.name == "Acquisition Date":
    print(acquisition_date.value)
    
acquisition_date_2 = input_2[0x0008, 0x0022]
if acquisition_date_2.name == "Acquisition Date":
    print(acquisition_date_2.value)
    
manufacturer = input[0x0008, 0x0070]
if manufacturer.name == "Manufacturer":
    print(manufacturer.value)
    
manufacturer_2 = input_2[0x0008, 0x0070]
if manufacturer_2.name == "Manufacturer":
    print(manufacturer_2.value)
    
modality = input[0x0008, 0x0060]
if modality.name == "Modality":
    print(modality.value)
    
modality_2 = input_2[0x0008, 0x0060]
if modality_2.name == "Modality":
    print(modality_2.value)
    
patient_id = input[0x0010, 0x0020]
if patient_id.name == "Patient ID":
    print(patient_id.value)
    
patient_id_2 = input_2[0x0010, 0x0020]
if patient_id_2.name == "Patient ID":
    print(patient_id_2.value)
    
body_part_examined = input[0x0018, 0x0015]
if body_part_examined.name == "Body Part Examined":
    print(body_part_examined.value)

if (0x0018, 0x0015) in input_2:
    body_part_examined_2 = input_2[0x0018, 0x0015]
    if body_part_examined_2.name == "Body Part Examined":
        print(body_part_examined_2.value)



