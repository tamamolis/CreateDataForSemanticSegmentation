from PIL import Image
from scipy.misc import imsave
import numpy as np
import os
import cv2

def delete_clone(path_img, path_mask):
    files_img = os.listdir(path_img)
    files_mask = os.listdir(path_mask)

    print(files_img)
    print(files_mask)

    return 0


def algoritm(path, path_save):
    files = os.listdir(path)
    for file in files:

        print(file)
        img = cv2.imread(path + file)
        print(path + file)

        h, w, channels = img.shape
        print('ширина и высота: ', w, h)

        crop_arr = np.zeros((w // 512, h // 512, 2))
        print(crop_arr.shape)
        print(3000 // 512)

        w_list = []
        h_list = []

        for i in np.arange(0, w, 512):
            w_list.append(i)

        for j in np.arange(0, h, 512):
            h_list.append(j)

        print(h_list, w_list)
        count = 0

        print(path)

        for j in range(len(h_list)):
            for i in range(len(w_list)):
                try:
                    count+=1
                    crop_img = img[h_list[i]: h_list[i+1], w_list[j]: w_list[j+1]]
                    l = len(str(file))
                    name = file[:l-4]
                    cv2.imwrite(path_save + name + str(i) + str(j) + '.png', crop_img)
                except:
                    IndexError

        print(count)
    return 0


def binary_table(img):
    h, w, z = np.shape(img)
    new_array = np.zeros((h, w, 3))
    for i in range(h):
        for j in range(w):
            buf = binary_metric(img[i][j])
            # print(buf)
            new_array[i][j] = buf
    return new_array


def binary_metric(input):
    legend_list = [[255, 255, 255], [255, 255, 0], [0, 255, 0], [0, 0, 255], [255, 0, 0], [0, 255, 255], [0, 0, 0],
                   [255, 0, 255], [128, 128, 0], [0, 128, 128]]

    white = [255, 255, 255]
    m = white - input

    if m[0] < 30 and m[1] < 30 and m[2] < 30:
        #print('road')
        return [255, 255, 255]
    else:
        return [0, 0, 0]


def lens():

    n = []

    n.append(len([name for name in os.listdir('Unet_data/crop_images') if os.path.isfile(os.path.join('Unet_data/crop_images', name))]))
    n.append(len([name for name in os.listdir('Unet_data/crop_mask') if os.path.isfile(os.path.join('Unet_data/crop_mask', name))]))

    return n


root = 'Unet_data/'


if __name__ == '__main__':

    mask = 'Unet_data/crop_mask/'
    files = os.listdir(mask)
    save_dir = 'Unet_data/test_mask/'
    i = 0

    print(lens())



    # for file in files:
    #     i += 1
    #     print(mask + file)
    #
    #     img = cv2.imread(mask + file)
    #     img = np.array(img)
    #
    #     new_img = binary_table(img)
    #     #print(new_img)
    #     cv2.imwrite(save_dir + file, new_img)