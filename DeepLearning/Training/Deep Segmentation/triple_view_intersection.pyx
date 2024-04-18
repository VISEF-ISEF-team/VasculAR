# Import necessary packages
import numpy as np
import nibabel as nib
cimport numpy as cnp
from libc.math cimport floor
import time
cnp.import_array()


cpdef triple_view_intersection():
    cdef dict axial_dice_score = {
        0: 0.9967,
        1: 0.7099,
        2: 0.8344,
        3: 0.7705,
        4: 0.8097,
        5: 0.7976,
        6: 0.8566,
        7: 0.7515,
        8: 0.6153,
        9: 0.5389,
        10: 0.8317,
        11: 0.6057
    }

    # saggital_dice_score = {
    #     0: -1, 1: -1, 2: -1, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: -1, 9: 7, 10: -1, 11: 11
    # }

    cdef dict saggital_dice_score = {
        0: 0.9956,
        1: 0.7777,
        2: 0.7950,
        3: 0.8008,
        4: 0.9298,
        5: 0.9220,
        6: 0.9429,
        7: 0.8701,
        8: 0.8039,
        9: 0.8414,
        10: 0.8424,
        11: 0.6679
    }

    # coronal_dice_score = {
    #     0: -1, 1: 1, 2: 2, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: 8, 9: -1, 10: 10, 11: -1
    # }
    cdef dict coronal_dice_score = {
        0: 0.9921,
        1: 0.9201,
        2: 0.8975,
        3: 0.7834,
        4: 0.8924,
        5: 0.9001,
        6: 0.8395,
        7: 0.7513,
        8: 0.8934,
        9: 0.7765,
        10: 0.8574,
        11: 0.6390
    }

    cdef cnp.ndarray axial = np.load("./output/axial_predict.npy")
    cdef cnp.ndarray saggital = np.load("./output/saggital_predict.npy")
    cdef cnp.ndarray coronal = np.load("./output/coronal_predict.npy")

    cdef cnp.ndarray[cnp.double_t, ndim=3] axial_v = np.vectorize(axial_dice_score.__getitem__)(axial)
    cdef cnp.ndarray[cnp.double_t, ndim=3] saggital_v = np.vectorize(saggital_dice_score.__getitem__)(saggital)
    cdef cnp.ndarray[cnp.double_t, ndim=3] coronal_v = np.vectorize(coronal_dice_score.__getitem__)(coronal)

    cdef cnp.ndarray[cnp.double_t, ndim=3] max_values = np.maximum.reduce([axial_v, saggital_v, coronal_v])

    cdef int i, j, k 
    cdef cnp.ndarray[cnp.int32_t, ndim=1] counter
    cdef cnp.ndarray[cnp.int32_t, ndim=1] choice
    cdef int max_index

    # how about counting most common and not necessarily the same for 3 models ?

    start_time = time.time()
    cdef cnp.ndarray[cnp.uint8_t, ndim=3] intersection = np.empty_like(axial)

    for i in range(axial.shape[0]):
        for j in range(axial.shape[1]):
            for k in range(axial.shape[2]):
                counter = np.zeros(11, dtype=np.int32)
                counter[axial[i][j][k]] += 1
                counter[saggital[i][j][k]] += 1
                counter[coronal[i][j][k]] += 1

                choice = np.argwhere(
                    counter == max(counter)).squeeze(axis=-1).astype(np.int32) 

                if len(choice) == 1:
                    intersection[i][j][k] = choice[0]
                else:
                    max_index = np.argmax(
                        [axial_v[i, j, k], saggital_v[i, j, k], coronal_v[i, j, k]])
                    if max_index == 0:
                        intersection[i][j][k] = axial[i][j][k]
                    elif max_index == 1:
                        intersection[i][j][k] = saggital[i][j][k]
                    else:
                        intersection[i][j][k] = coronal[i][j][k]

    end_time = time.time()

    print(f"Time: {end_time - start_time}")

    new_image = nib.Nifti1Image(intersection, affine=np.eye(4))
    nib.save(new_image, "./output/intersection.nii")

    np.save("./output/intersection.npy", intersection)
