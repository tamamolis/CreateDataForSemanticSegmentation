from PIL import Image
from scipy.misc import imsave
import numpy as np
import os
import cv2


def binary_table(img):
    h, w, z = np.shape(img)
    new_array = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            buf = binary_metric(img[i][j])
            # print(buf)
            new_array[i][j] = buf
    return new_array


def binary_metric(input):
    legend_list = [[255, 255, 255], [255, 255, 0], [0, 255, 0], [0, 0, 255], [255, 0, 0], [0, 255, 255], [0, 0, 0],
                   [255, 0, 255], [128, 128, 0], [0, 128, 128]]

    if input[0] == 255 and input[1] == 255 and input[2] == 255:
        # print('road')
        return 0
    else:
        return 1


def out_binary_table(img):
    h, w, z = np.shape(img)
    new_array = np.zeros((h, w, 3))
    for i in range(h):
        for j in range(w):
            buf = out_binary_metric(img[i][j])
            # print(buf)
            new_array[i][j] = buf
    return new_array


def out_binary_metric(input):
    legend_list = [[255, 255, 255], [255, 255, 0], [0, 255, 0], [0, 0, 255], [255, 0, 0], [0, 255, 255], [0, 0, 0],
                   [255, 0, 255], [128, 128, 0], [0, 128, 128]]
    color = legend_list[input[0]]
    return color


root = 'data/'


if __name__ == '__main__':

    color_pictures = 'data/for_vadim/'
    files = os.listdir(color_pictures)
    save_dir = 'data/for_vadim_save/'
    i = 0

    for file in files:
        i += 1
        print(color_pictures + file)

        img = cv2.imread(color_pictures + file)
        img = np.array(img)

        new_img = out_binary_table(img)
        print(new_img)
        cv2.imwrite(save_dir + file, new_img)