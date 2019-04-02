import cv2
import numpy as np
import os
import random
from os import listdir
from os.path import isfile, join
from scipy.ndimage import rotate
import shutil


def flip(path, path_save, axis): # axis = 0 (горизонтально), axis = 1 (вертикально), axis = -1 (оба?)
    if axis != 0 | axis != 1 | axis != -1:
        print("axis должен быть равен 0, 1 или -1!\n")
        return 0
    files = [f for f in listdir(path) if isfile(join(path, f))]
    files.sort()
    for name in files:
        print(path + name)
        img = cv2.imread(path + name, cv2.IMREAD_UNCHANGED)
        out = cv2.flip(img, axis)

        name, format = name.split(".", 1)
        cv2.imwrite(path_save + name + 'flip' + str(axis) + '.' + format, out)


def rot(path, path_save, angle):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    files.sort()
    i = 0
    for name in files:
        # print(path + name)
        image = cv2.imread(path + name, cv2.IMREAD_UNCHANGED)
        im_rot = rotate(image, angle, reshape=True)

        name, format = name.split(".", 1)
        print("img: ", path + name, np.shape(im_rot))
        cv2.imwrite(path_save + name + 'rot' + str(i) + '.' + format, im_rot)
        i += 1


def image_illumination(path, path_save, path_mask, path_save_mask, level):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    files.sort()
    i = 0
    for file in files:
        # print(path + name)
        name, format = file.split(".", 1)

        in_img = cv2.imread(path + file, cv2.IMREAD_UNCHANGED)
        a = np.double(in_img)
        b = a + level
        out = b

        print("img: ", path + name, np.shape(out))
        cv2.imwrite(path_save + name + 'illumination' + str(level) + str(i) + '.' + format, out)

        # теперь надо скопировать маски, неизменнённые!
        # причём они должны называться также

        img_seg = cv2.imread(path_mask + name + '.png')
        cv2.imwrite(path_save_mask + name + 'illumination' + str(level) + str(i) + '.' + format, img_seg)

        i += 1


def zoom (path, path_save, zoom_factor):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    files.sort()
    for name in files:
        img = cv2.imread(path + name, cv2.IMREAD_UNCHANGED)
        # print(path + name)

        height, width = img.shape[:2] # It's also the final desired shape
        new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)

        y1, x1 = max(0, new_height - height) // 2, max(0, new_width - width) // 2
        y2, x2 = y1 + height, x1 + width
        bbox = np.array([y1,x1,y2,x2])

        bbox = (bbox / zoom_factor).astype(np.int)
        y1, x1, y2, x2 = bbox
        cropped_img = img[y1:y2, x1:x2]

        resize_height, resize_width = min(new_height, height), min(new_width, width)
        pad_height1, pad_width1 = (height - resize_height) // 2, (width - resize_width) // 2
        pad_height2, pad_width2 = (height - resize_height) - pad_height1, (width - resize_width) - pad_width1
        pad_spec = [(pad_height1, pad_height2), (pad_width1, pad_width2)] + [(0,0)] * (img.ndim - 2)

        result = cv2.resize(cropped_img, (resize_width, resize_height))
        result = np.pad(result, pad_spec, mode='constant')
        assert result.shape[0] == height and result.shape[1] == width

        name, format = name.split(".", 1)

        print("img: ", path + name, np.shape(result))
        cv2.imwrite(path_save + name + 'zoom' + str(zoom_factor) + '.' + format, result)


if __name__ == '__main__':
    os.system("find /Users/kate/PycharmProjects/make_data -name '.DS_Store' -delete")

    path_orig_img = 'Airports/!MINEhelsinki/img/'
    path_orig_mask = 'Airports/!MINEhelsinki/mask/'

    path_save_aug_img = 'Airports/!MINEhelsinki/b&w_aug/img/'
    path_save_aug_mask = 'Airports/!MINEhelsinki/b&w_aug/mask/'

    files_img = [f for f in listdir(path_save_aug_img) if isfile(join(path_save_aug_img, f))]
    files_mask = [f for f in listdir(path_save_aug_mask) if isfile(join(path_save_aug_mask, f))]

    assert len(files_img) == len(files_mask)

    # работает, не трогать
    # for i in np.arange(-100, 100, 20):
    #     image_illumination(path_orig_img, path_save_aug_img, path_orig_mask, path_save_aug_mask, level=i)

    # работает, не трогать
    for i in np.arange(1.5, 8.5, 2.5):
        zoom(path_orig_img, path_save_aug_img, zoom_factor=i)
        zoom(path_orig_mask, path_save_aug_mask, zoom_factor=i)

    # работает, не трогать
    for i in np.arange(-1, 1, 1):
        flip(path_orig_img, path_save_aug_img, axis=i)
        flip(path_orig_mask, path_save_aug_mask, axis=i)