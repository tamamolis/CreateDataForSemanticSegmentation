from PIL import Image
from scipy.misc import imsave
import numpy as np
import os
import cv2
import shutil


#  find /Users/kate/PycharmProjects/make_data -name '.DS_Store' -delete
legend_list = [[0, 0, 255], [0, 255, 0], [255, 255, 0], [255, 255, 255], [0, 255, 255], [255, 0, 255], [255, 0, 0], [0, 0, 0]]


def lens(root):
    n = []

    n.append(len([name for name in os.listdir(root + 'train') if os.path.isfile(os.path.join(root + 'train', name))]))
    n.append(len([name for name in os.listdir(root + 'trainmask') if os.path.isfile(os.path.join(root + 'trainmask', name))]))

    n.append(len([name for name in os.listdir(root + 'test/') if os.path.isfile(os.path.join(root + 'test/', name))]))
    n.append(len([name for name in os.listdir(root + 'testmask/') if os.path.isfile(os.path.join(root + 'testmask/', name))]))

    n.append(len([name for name in os.listdir(root + 'val/') if os.path.isfile(os.path.join(root + 'val/', name))]))
    n.append(len([name for name in os.listdir(root + 'valmask/') if os.path.isfile(os.path.join(root + 'valmask/', name))]))

    return n


def make_txt(path, path_an_not, dir):

    f = open('SegNet_data/' + str(dir) + '.txt', 'w')
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


def euclidean_metric(input):

    #  сумма модулей разности
    total = 100000
    index = -1

    for legend in legend_list:
        new_total = abs(input[0] - legend[0])**2 + abs(input[1] - legend[1])**2 + abs(input[2] - legend[2])**2
        if new_total < total:
            total = new_total
            index = legend_list.index(legend)
    return index


def metric(input):

    for legend in legend_list:
        m = legend - input

        if m[0] == 0 and m[1] == 0 and m[2] == 0:
            index = legend_list.index(legend)
            if index not in [0, 1, 2, 3, 4, 5, 6]:
                print('нужно искать баг, Катя', legend, input)
                index = 4
            if index == 5:
                print('magenta!')
            return index


def table(img):
    h, w, z = np.shape(img)
    new_array = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            buf = euclidean_metric(img[i][j])
            # print(buf)
            new_array[i][j] = buf
    return new_array


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
        cv2.imwrite(save_dir + 'new' + file, new_img)


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


def out_metric(input):
    # print(input)
    color = legend_list[input[0]]
    return color


def out_table(img):

    h = np.shape(img)[0]
    w = np.shape(img)[1]
    new_array = np.zeros((h, w, 3))
    for i in range(h):
        for j in range(w):
            # print(img[i][j])
            buf = out_metric(img[i][j])
            # print(buf)
            new_array[i][j] = buf
    return new_array


def out_black_and_white(out_dir, save_dir):
    color_pictures = out_dir
    files = os.listdir(color_pictures)
    print(out_dir)
    i = 0

    for file in files:
        i += 1
        print(save_dir + file)

        img = cv2.imread(color_pictures + file)
        img = np.array(img)

        new_img = out_table(img)
        cv2.imwrite(save_dir + 'new' + file, new_img)


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


root = 'Test_data/'


if __name__ == '__main__':

    out_dir = root + 'test/'
    save_dir = root + 'test_save/'

    out_black_and_white(out_dir, save_dir)