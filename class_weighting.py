import math
import os
import cv2
import numpy as np
from sklearn.utils import class_weight
from sklearn.preprocessing import LabelEncoder

# {'1': 1.0, '0': 1.0, '4': 1.0, '3': 1.0, '5': 2.898633430298013, '2': 1.0} RESULT

DataPath = '/Users/kate/PycharmProjects/Segnet.new/data/'


def create_class_weight(labels_dict,mu=0.15):
    total = sum(labels_dict.values())
    keys = labels_dict.keys()
    class_weight = dict()

    for key in keys:
        score = math.log(mu*float(total)/float(labels_dict[key]))
        class_weight[key] = score if score > 1.0 else 1.0

    return class_weight


def create_labels_dict():

    labels_dict = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    files = os.listdir(DataPath + 'trainmask')

    for file in files:
        print(file)
        img = cv2.imread(DataPath + 'trainmask/' + file)

        for x in range(img.shape[0]):
            for y in range(img.shape[1]):

                index = img[x][y][0]
                labels_dict[str(index)] += 1
    return labels_dict


def compute_class_weight(class_weight, classes, y):

    weight = np.ones(classes.shape[0], dtype=np.float64, order='C')
    if not isinstance(class_weight, dict):
            raise ValueError("class_weight must be dict, 'balanced', or None,"
                             " got: %r" % class_weight)
    for c in class_weight:
            i = np.searchsorted(classes, c)
            if i >= len(classes) or classes[i] != c:
                raise ValueError("Class label {} not present.".format(c))
            else:
                weight[i] = class_weight[c]

    return weight


if __name__ == '__main__':

    labels_dict = create_labels_dict()
    print(labels_dict)
