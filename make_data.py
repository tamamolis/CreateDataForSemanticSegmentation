from PIL import Image
from scipy.misc import imsave
import numpy as np
import os
import cv2
import shutil

#find /Users/kate/PycharmProjects/make_data -name '.DS_Store' -delete


def make_txt(path, path_an_not, dir):

    f = open('prepare_data/' + str(dir) + '.txt', 'w')
    n = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])

    list_path = []
    list_pathannot = []

    for name in os.listdir(path):
        list_path.append('/make_data/' + str(path) + str(name))

    for name in os.listdir(path_an_not):
        list_pathannot.append('/make_data/' + str(path_an_not) + str(name))

    print(list_path)
    print(list_pathannot)

    for i in range(n):
        print(i)
        f.write(str(list_path[i]) + ' ' + str(list_pathannot[i]) + '\n')


def black_and_white(out_dir, save_dir):
    color_pictures = out_dir
    files = os.listdir(color_pictures)
    print(out_dir)
    i = 0

    for file in files:
        i += 1
        print(save_dir + file)

        img = cv2.imread(color_pictures + file)
        img = np.array(img)

        new_img = table(img)
        cv2.imwrite(save_dir + file, new_img)


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


def crop_img(dir):
    # dir = 'notPotsdam/notmasks/'

    path = 'other_data/' + dir
    path_save = dir
    algoritm(path, path_save)

    dir = 'notPotsdam/masks/'

    path = 'other_data/' + dir
    path_save = dir
    algoritm(path, path_save)

    dir = 'Potsdam/notmasks/'

    path = 'other_data/' + dir
    path_save = dir
    algoritm(path, path_save)

    dir = 'Potsdam/masks/'

    path = 'other_data/' + dir
    path_save = dir
    algoritm(path, path_save)


def metric(input):
    legend_list = [[255, 255, 255], [255, 255, 0], [0, 255, 0], [0, 0, 255], [255, 0, 0], [0, 255, 255]]

    for legend in legend_list:
        m = legend - input

        if m[0] < 128 and m[1] < 128 and m[2] < 128:
            index = legend_list.index(legend)
            # print(index)
            if index not in [0, 1, 2, 3, 4, 5]:
                print('нужно искать баг, Катя', legend, input)
                index = 4
            return index


def table(img):
    h, w, z = np.shape(img)
    new_array = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            buf = metric(img[i][j])
            # print(buf)
            new_array[i][j] = buf
    return new_array


def move_pictures(path, moveto, n):

    files = os.listdir(path)
    files.sort()
    k = 0
    for f in files:
        src = path + f
        dst = moveto + f
        shutil.move(src, dst)
        if k == n:
            break
        k += 1


root = '/Volumes/Mac/WORK/'


if __name__ == '__main__':

    print('kxe-kxe')
    n = 600

    path = root + "train/"
    moveto = "prepare_data/" + "train/"

    move_pictures(path, moveto, n)

    path = root + "trainmask/"
    moveto = "prepare_data/trainmask/"

    move_pictures(path, moveto, n)

    n = 100

    path = root + "test/"
    moveto = "prepare_data/" + "test/"

    move_pictures(path, moveto, n)

    path = root + "testmask/"
    moveto = "prepare_data/testmask/"

    move_pictures(path, moveto, n)

    n = 200

    path = root + "val/"
    moveto = "prepare_data/" + "val/"

    move_pictures(path, moveto, n)

    path = root + "valmask/"
    moveto = "prepare_data/valmask/"

    move_pictures(path, moveto, n)

    dir = 'test'
    path = 'prepare_data/' + dir + '/'
    path_mask = 'prepare_data/' + dir + 'mask/'
    # #
    # # black_and_white(path_mask, path_mask)
    make_txt(path, path_mask, dir)
    # #
    dir = 'train'
    path = 'prepare_data/' + dir + '/'
    path_mask = 'prepare_data/' + dir + 'mask/'
    # #
    # # black_and_white(path_mask, path_mask)
    make_txt(path, path_mask, dir)
    # #
    dir = 'val'
    path = 'prepare_data/' + dir + '/'
    path_mask = 'prepare_data/' + dir + 'mask/'
    # #
    # # black_and_white(path_mask, path_mask)
    make_txt(path, path_mask, dir)