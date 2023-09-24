import ants
import sys
import os

SYS_PATH = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))
sys.path.append(SYS_PATH + '/' + 'supporters')
import image_file_processing

def ants_preprocess(raw_img_path):
    raw_img_ants = ants.image_read(raw_img_path)
    print(raw_img_ants)

    raw_img_ants_arr = raw_img_ants.numpy()
    print(f'type = {type(raw_img_ants_arr)}')
    print(f'shape = {raw_img_ants_arr.shape}')


examples = os.listdir('../assets/raw_examples')
ants_preprocess("../assets/raw_examples/" + examples[2])