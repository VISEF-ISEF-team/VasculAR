import SimpleITK as sitk
import sys
import os


SYS_PATH = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))
sys.path.append(SYS_PATH + '/' + 'supporters')
import image_file_processing

def stk_preprocess(raw_img_path):
    raw_img_sitk = sitk.ReadImage(raw_img_path, sitk.sitkFloat32)
    image_file_processing.show_sitk_img_info(raw_img_sitk)

    raw_img_sitk_arr = sitk.GetArrayFromImage(raw_img_sitk)
    print(f'type = {type(raw_img_sitk_arr)}')
    print(f'shape = {raw_img_sitk_arr.shape}')


examples = os.listdir('../assets/raw_examples')
stk_preprocess("../assets/raw_examples/" + examples[2])