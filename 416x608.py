import os
import cv2
import numpy as np
import shutil

legend_list = [[0, 0, 255], [0, 255, 0], [255, 255, 0], [255, 255, 255], [0, 255, 255], [255, 0, 255], [255, 0, 0]]


def only_name_txt(root, path_an_not, dir):

    f = open(root + str(dir) + '.txt', 'w')
    m = len([name for name in os.listdir(path_an_not) if os.path.isfile(os.path.join(path_an_not, name))])

    print(m)

    list_pathannot = []

    for name in os.listdir(path_an_not):
        list_pathannot.append(str(name))

    for i in range(m):
        f.write(str(list_pathannot[i]) + '\n')


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


def table(img):
    h, w, z = np.shape(img)
    new_array = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            buf = euclidean_metric(img[i][j])
            # print(buf)
            new_array[i][j] = buf
    return new_array


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


def algoritm(path, path_save):
    files = os.listdir(path)
    for file in files:
        print(file)
        img = cv2.imread(path + file)
        print(path + file)

        h, w, channels = img.shape

        print('ширина и высота: ', w, h)
        print(path)

        windowSize = [416, 608]
        stepSize = 50

        for y in range(0, img.shape[0], stepSize):
            for x in range(0, img.shape[1], stepSize):
                try:
                    crop_img = img[y:y + windowSize[0], x:x + windowSize[1]]
                    l = len(str(file))
                    name = file[:l-4]
                    cv2.imwrite(path_save + name + str(y) + str(x) + '.png', crop_img)
                except:
                    IndexError
    return 0


def delete_img(path):
    files = os.listdir(path)
    for file in files:
        img = cv2.imread(path + file)
        # print(np.shape(img))
        if np.shape(img) != (360, 480, 3):
            os.remove(path + file)
    return 0


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


def make_txt(root, path, path_an_not, dir):

    f = open(root + str(dir) + '.txt', 'w')
    n = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    m = len([name for name in os.listdir(path_an_not) if os.path.isfile(os.path.join(path_an_not, name))])

    print(n, m)

    list_path = []
    list_pathannot = []

    for name in os.listdir(path):
        list_path.append('/make_data/' + str(path) + str(name))

    for name in os.listdir(path_an_not):
        list_pathannot.append('/make_data/' + str(path_an_not) + str(name))

    for i in range(n):
        f.write(str(list_path[i]) + ' ' + str(list_pathannot[i]) + '\n')


root = 'SegNet_data/'

# всего 927
# 300 на валидацию
# 27 на тест

if __name__ == '__main__':

    make_txt(root, root + 'test/', root + 'testmask/', 'test')
    make_txt(root, root + 'train/', root + 'trainmask/', 'train')
    make_txt(root, root + 'val/', root + 'valmask/', 'val')