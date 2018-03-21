import os
import cv2
import numpy as np
import shutil


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
            buf = metric(img[i][j])
            # print(buf)
            new_array[i][j] = buf
    return new_array


def metric(input):
    legend_list = [[0, 0, 255], [0, 255, 0], [255, 255, 0], [255, 255, 255], [0, 255, 255], [255, 0, 255], [255, 0, 0]]

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


def sliding_window(image, stepSize, windowSize):
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


def algoritm(path, path_save):
    files = os.listdir(path)
    for file in files:
        print(file)
        img = cv2.imread(path + file)
        print(path + file)

        h, w, channels = img.shape
        print('ширина и высота: ', w, h)

        print(path)

        windowSize = [360, 480]
        stepSize = 50

        for y in range(0, img.shape[0], stepSize):
            for x in range(0, img.shape[1], stepSize):
                try:
                    crop_img = img [y:y + windowSize[0], x:x + windowSize[1]]
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


root = 'Test_data/test/'

if __name__ == '__main__':

    path = root + 'crop_color/'
    moveto = root + 'trash_color/'

    n = 1400  # останется 927
    move_pictures(path, moveto, n)

    ############################

    path = root + 'crop_masks/'
    moveto = root + 'trash_masks/'

    n = 1400  # останется 927
    move_pictures(path, moveto, n)
