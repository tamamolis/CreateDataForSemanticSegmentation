from __future__ import absolute_import
from __future__ import print_function

import cv2
import numpy as np
import itertools

from helper import *
import os


def normalized(rgb):
    # return rgb/255.0
    norm = np.zeros((rgb.shape[0], rgb.shape[1], 3), np.float32)

    b = rgb[:, :, 0]
    g = rgb[:, :, 1]
    r = rgb[:, :, 2]

    norm[:, :, 0] = cv2.equalizeHist(b)
    norm[:, :, 1] = cv2.equalizeHist(g)
    norm[:, :, 2] = cv2.equalizeHist(r)

    return norm


def one_hot_it(labels):
    x = np.zeros([512, 512, 6])  # здесь 6, хотя в оригинале 12, мне кажется, это ошибка, ведь классов 13, и
                                 #  в этом случае указывается кол-во, т.е. нумерация не с нуля
    for i in range(512):
        for j in range(512):
            try:
                if labels[i][j] > 5:
                    print(labels[i][j], i, j)
                    labels[i][j] = 5

                x[i, j, labels[i][j]] = 1
            except IndexError:
                print(i, j, np.shape(labels))
                x[i, j, 5] = 1
    return x
