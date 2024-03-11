import numpy as np


def one_hot_encode(original_path, save_path):
    a = np.load(original_path)
    a_encode = (np.arange(12) == a[..., None]).astype(int)

    print(a_encode.shape)
    np.save(save_path, a_encode)


if __name__ == "__main__":
    original_path = "./output/intersection.npy"
    save_path = "./output/intersection_encode.npy"
    one_hot_encode(original_path, save_path)
