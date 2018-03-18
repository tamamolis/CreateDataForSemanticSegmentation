from __future__ import absolute_import
from __future__ import print_function
from helper import *
import os

DataPath = '/Users/kate/PycharmProjects/make_data/SegNet_data/'
data_shape = 360*480


def load_data(mode):
    data = []
    label = []
    with open(DataPath + mode + '.txt') as f:
        txt = f.readlines()
        txt = [line.split(' ') for line in txt]

    for i in range(len(txt)):
        print(txt[i][0][10:])
        data.append(np.rollaxis(normalized(cv2.imread(os.getcwd() + '/' + txt[i][0][11:])), 2))
        label.append(one_hot_it(cv2.imread(os.getcwd() + '/' + txt[i][1][11:][:-1])[:, :, 0]))

    return np.array(data), np.array(label)


def lens():
    n = []

    n.append(len([name for name in os.listdir(DataPath + '/train') if os.path.isfile(os.path.join(DataPath + '/train', name))]))
    n.append(len([name for name in os.listdir(DataPath + '/trainmask') if os.path.isfile(os.path.join(DataPath + '/trainmask', name))]))

    n.append(len([name for name in os.listdir(DataPath + '/test/') if os.path.isfile(os.path.join(DataPath + '/test/', name))]))
    n.append(len([name for name in os.listdir(DataPath + '/testmask/') if os.path.isfile(os.path.join(DataPath + '/testmask/', name))]))

    n.append(len([name for name in os.listdir(DataPath + '/val/') if os.path.isfile(os.path.join(DataPath + '/val/', name))]))
    n.append(len([name for name in os.listdir(DataPath + '/valmask/') if os.path.isfile(os.path.join(DataPath + '/valmask/', name))]))

    return n


if __name__ == '__main__':

    n = lens()
    print(n, n[0], n[2], n[4])

    # test_data, test_label = load_data("test")
    # test_label = np.reshape(test_label, (n[2], data_shape, 6))
    #
    # np.save(DataPath + "/test_data", test_data)
    # np.save(DataPath + "/test_label", test_label)

    val_data, val_label = load_data("val")
    val_label = np.reshape(val_label, (n[4], data_shape, 6))

    np.save(DataPath + "/val_data", val_data)
    np.save(DataPath + "/val_label", val_label)

    # train_data, train_label = load_data("train")
    # train_label = np.reshape(train_label, (n[0], data_shape, 6))
    #
    # np.save(DataPath + "/train_data", train_data)
    # np.save(DataPath + "/train_label", train_label)

    # FYI they are:
    # Impervious surfaces (RGB: 255, 255, 255)
    # Building (RGB: 0, 0, 255)
    # Low vegetation (RGB: 0, 255, 255)
    # Tree (RGB: 0, 255, 0)
    # Car (RGB: 255, 255, 0)
    # Clutter/background (RGB: 255, 0, 0)