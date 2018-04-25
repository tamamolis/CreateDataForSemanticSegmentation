from __future__ import absolute_import
from __future__ import print_function
from helper import *
import os

data_shape = 360*480


def load_data(mode):
    data = []
    label = []
    with open(DataPath + mode + ".txt") as f:
        txt = f.readlines()
        txt = [line.split(" ") for line in txt]

    for i in range(len(txt)):
        print(os.getcwd() + '/' + txt[i][0][11:])
        data.append(np.rollaxis(normalized(cv2.imread(os.getcwd() + '/' + txt[i][0][11:])), 2))
        # label.append(one_hot_it(cv2.imread(os.getcwd() + "/" + txt[i][1][49:][:-1])[:, :, 0]))
    return np.array(data), np.array(label)


def lens():
    n = []

    n.append(len([name for name in os.listdir(DataPath + "train/") if os.path.isfile(os.path.join(DataPath + "train/", name))]))
    n.append(len([name for name in os.listdir(DataPath + "trainmask/") if os.path.isfile(os.path.join(DataPath + "trainmask/", name))]))

    n.append(len([name for name in os.listdir(DataPath + "test/") if os.path.isfile(os.path.join(DataPath + "test/", name))]))
    n.append(len([name for name in os.listdir(DataPath + "testmask/") if os.path.isfile(os.path.join(DataPath + "testmask/", name))]))

    n.append(len([name for name in os.listdir(DataPath + "val/") if os.path.isfile(os.path.join(DataPath + "val/", name))]))
    n.append(len([name for name in os.listdir(DataPath + "valmask/") if os.path.isfile(os.path.join(DataPath + "valmask/", name))]))

    return n


DataPath = "Test/"


if __name__ == "__main__":

    # n = lens()
    # print(n, n[0], n[2], n[4])

    test_data, test_label = load_data("test")
    np.save(DataPath + "/crop", test_data)