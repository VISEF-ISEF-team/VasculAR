import os
import SimpleITK as sitk
import nibabel as nib
import json
import numpy as np

class DiseaseDectection:
    def __init__(self):
        self.path = "D:/Documents/GitHub/VascuIAR/DeepLearning/Training/Defects Detection/input/data_label.json"
        self.main_path = "D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD_sep_labels"
        with open(self.path, 'r', encoding='utf-8') as file:
            self.data_label = json.load(file)
        
    def dice_coefficient(self, array1, array2):
        intersection = np.sum(array1 * array2)
        union = np.sum(array1) + np.sum(array2)
        return 2.0 * intersection / union if union > 0 else 1.0

    def read_img(self, path):
        img_raw = sitk.ReadImage(path, sitk.sitkFloat32)
        img = sitk.GetArrayFromImage(img_raw)
        return img

    def comparison(self, class_label, disease, input_img):
        for key, value in self.data_label.items():
            if key == disease:
                cnt_true=val_true=cnt_false=val_false=0
                for case, val in value.items():
                    if case == class_label:
                        continue
                    if cnt_false > 18: 
                        break
                    if val==True:
                        cnt_true += 1
                        val_true += (self.dice_coefficient(
                            input_img,
                            self.read_img(os.path.join(self.main_path, f"VHSCDD_{case}_label", f"ct_{case}_{class_label}.nii.gz"))
                        ))
                    else:
                        cnt_false += 1
                        val_false+=(self.dice_coefficient(
                            input_img,
                            self.read_img(os.path.join(self.main_path, f"VHSCDD_{case}_label", f"ct_{case}_{class_label}.nii.gz"))
                        ))
                return (val_true/cnt_true, val_false/cnt_false)
            
    def display(self, res, disease):
        print(f"Tỉ lệ mắc {disease}: {(res[0]/(res[0] + res[1]))*100}" , f"Tỉ lệ bình thường: {(res[1]/(res[0] + res[1]))*100}")


    def detection(self, class_label, input_img, defect_var):
        if class_label == 'label_7' and defect_var==11:
            self.display(self.comparison(class_label=class_label, disease='Cung động mạch chủ đôi', input_img=input_img), disease='Cung động mạch chủ đôi')
        if class_label == 'label_7' and defect_var==10:
            self.display(self.comparison(class_label=class_label, disease='Hẹp eo động mạch chủ', input_img=input_img), disease='Hẹp eo động mạch chủ')
            
        elif class_label == 'label_8':
            self.comparison(class_label=class_label, disease='Vòng thắt động mạch phổi', input_img=input_img)
        
        elif class_label == 'label_12':
            self.comparison(class_label=class_label, disease='Bất thường động mạch vành', input_img=input_img)
            
        elif class_label == 'label_10':
            self.comparison(class_label=class_label, disease='Tĩnh mạch chủ kép', input_img=input_img)
            
    def double_detection(self, class_label, input_img_1, input_img_2):            
        if class_label == ('label_8', 'label_9'):
            A = self.comparison(class_label=class_label[0], disease='Thân chung động mạch', input_img=input_img_1)
            B = self.comparison(class_label=class_label[1], disease='Thân chung động mạch', input_img=input_img_2)
            self.display(((A[0] + B[0])/2, (A[1] + B[1])/2), disease='Thân chung động mạch')
            
        elif class_label == ('label_7', 'label_8'):
            A = self.comparison(class_label=class_label[0], disease='Phình động mạch', input_img=input_img_1)
            B = self.comparison(class_label=class_label[1], disease='Phình động mạch', input_img=input_img_2)
            self.display(((A[0] + B[0])/2, (A[1] + B[1])/2), disease='Phình động mạch')
            
        elif class_label == ('label_4', 'label_10'):
            A = self.comparison(class_label=class_label[0], disease='Bất thường tĩnh mạch phổi trở về tuần hoàn', input_img=input_img_1)
            B = self.comparison(class_label=class_label[1], disease='Bất thường tĩnh mạch phổi trở về tuần hoàn', input_img=input_img_2)
            self.display(((A[0] + B[0])/2, (A[1] + B[1])/2), disease='Bất thường tĩnh mạch phổi trở về tuần hoàn')
            
        elif class_label == ('label_2', 'label_3'):
            A = self.comparison(class_label=class_label[0], disease='Thông liên thất', input_img=input_img_1)
            B = self.comparison(class_label=class_label[1], disease='Thông liên thất', input_img=input_img_2)
            self.display(((A[0] + B[0])/2, (A[1] + B[1])/2), disease='Thông liên thất')
            
    def triple_detection(self, class_label, input_img_1, input_img_2, input_img_3):
        if class_label == ('label_3', 'label_8', 'label_9'):
            A = self.comparison(class_label=class_label[0], disease='Thất phải hai đường ra', input_img=input_img_1)
            B = self.comparison(class_label=class_label[1], disease='Thất phải hai đường ra', input_img=input_img_2)
            C = self.comparison(class_label=class_label[2], disease='Thất phải hai đường ra', input_img=input_img_3)
            self.display(((A[0] + B[0] + C[0])/2, (A[1] + B[1] + C[1])/2), disease='Thất phải hai đường ra')
            
        elif class_label == ('label_7', 'label_8', 'label_9'):
            A = self.comparison(class_label=class_label[0], disease='Còn ống động mạch', input_img=input_img_1)
            B = self.comparison(class_label=class_label[1], disease='Còn ống động mạch', input_img=input_img_2)
            C = self.comparison(class_label=class_label[2], disease='Còn ống động mạch', input_img=input_img_3)
            self.display(((A[0] + B[0] + C[0])/2, (A[1] + B[1] + C[1])/2), disease='Còn ống động mạch')
            
    def quad_detection(self, class_label, input_img_1, input_img_2, input_img_3, input_img_4):
        if class_label == ('label_2', 'class_3', 'label_8', 'label_9'):
            A = self.comparison(class_label=class_label[0], disease='Đảo gốc động mạch', input_img=input_img_1)
            B = self.comparison(class_label=class_label[1], disease='Đảo gốc động mạch', input_img=input_img_2)
            C = self.comparison(class_label=class_label[2], disease='Đảo gốc động mạch', input_img=input_img_3)
            D = self.comparison(class_label=class_label[3], disease='Đảo gốc động mạch', input_img=input_img_4)
            self.display(((A[0] + B[0] + C[0] + D[0])/2, (A[1] + B[1] + C[1] + D[1])/2), disease='Đảo gốc động mạch')
        
    def main_process(self, specified_data, defect_var):
        if defect_var == 1:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_2.nii.gz")
            input_path_2 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_3.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            input_img_2 = self.read_img(input_path_2)
            class_label = (input_path_1[-14:-7], input_path_2[-14:-7])
            self.double_detection(class_label, input_img_1, input_img_2)
            
        elif defect_var == 2:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_7.nii.gz")
            input_path_2 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_8.nii.gz")
            input_path_3 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_9.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            input_img_2 = self.read_img(input_path_2)
            input_img_3 = self.read_img(input_path_3)
            class_label = (input_path_1[-14:-7], input_path_2[-14:-7], input_path_3[-14:-7])
            self.triple_detection(class_label, input_img_1, input_img_2, input_img_3)
            
        elif defect_var == 3:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_8.nii.gz")
            input_path_2 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_9.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            input_img_2 = self.read_img(input_path_2)
            class_label = (input_path_1[-14:-7], input_path_2[-14:-7])
            self.double_detection(class_label, input_img_1, input_img_2)
            
        elif defect_var == 4:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_12.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            class_label = input_path_1[-14:-7]
            self.detection(class_label, input_img_1, defect_var=None)
            
        elif defect_var == 5:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_7.nii.gz")
            input_path_2 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_8.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            input_img_2 = self.read_img(input_path_2)
            class_label = (input_path_1[-14:-7], input_path_2[-14:-7])
            self.double_detection(class_label, input_img_1, input_img_2)
    
        elif defect_var == 6:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_4.nii.gz")
            input_path_2 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_10.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            input_img_2 = self.read_img(input_path_2)
            class_label = (input_path_1[-14:-7], input_path_2[-14:-7])
            self.double_detection(class_label, input_img_1, input_img_2)
            
        elif defect_var == 7:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_10.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            class_label = input_path_1[-14:-7]
            self.detection(class_label, input_img_1, defect_var=None)
            
        elif defect_var == 8:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_2.nii.gz")
            input_path_2 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_3.nii.gz")
            input_path_3 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_8.nii.gz")
            input_path_4 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_9.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            input_img_2 = self.read_img(input_path_2)
            input_img_3 = self.read_img(input_path_3)
            input_img_4 = self.read_img(input_path_4)
            class_label = (input_path_1[-14:-7], input_path_2[-14:-7], input_path_3[-14:-7], input_path_4[-14:-7])
            self.triple_detection(class_label, input_img_1, input_img_2, input_img_3, input_img_4)
            
        elif defect_var == 9:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_8.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            class_label = input_path_1[-14:-7]
            self.detection(class_label, input_img_1, defect_var=None)
            
        elif defect_var == 10:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_9.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            class_label = input_path_1[-14:-7]
            self.detection(class_label, input_img_1, defect_var=10)
            
        elif defect_var == 11:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_9.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            class_label = input_path_1[-14:-7]
            self.detection(class_label, input_img_1, defect_var=11)
            
        elif defect_var == 12:
            input_path_1 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_3.nii.gz")
            input_path_2 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_8.nii.gz")
            input_path_3 = os.path.join(self.main_path, f"VHSCDD_{specified_data}_label", f"ct_{specified_data}_label_9.nii.gz")
            input_img_1 = self.read_img(input_path_1)
            input_img_2 = self.read_img(input_path_2)
            input_img_3 = self.read_img(input_path_3)
            class_label = (input_path_1[-14:-7], input_path_2[-14:-7], input_path_3[-14:-7])
            self.triple_detection(class_label, input_img_1, input_img_2, input_img_3)
    
