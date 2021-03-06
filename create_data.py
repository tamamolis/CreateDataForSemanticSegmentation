import os
import cv2
import numpy as np
import shutil

# синий, зелёный, жёлтый, белый, бирюзовый, magenta, красный
# legend_list = [[0, 0, 255], [0, 255, 0], [255, 255, 0], [255, 255, 255], [0, 255, 255], [255, 0, 255], [255, 0, 0]]
# синий, зелёный, белый, красный

legend_list = [[0, 0, 255], [0, 255, 0], [255, 255, 255], [255, 0, 0]]


def only_name_txt(root, pathmask, dir):

    f = open(root + str(dir) + '.txt', 'w')
    m = len([name for name in os.listdir(pathmask) if os.path.isfile(os.path.join(pathmask, name))])

    print(m)

    list_mask = []

    for name in os.listdir(pathmask):
        list_mask.append(str(name))

    for i in range(m):
        f.write(str(list_mask[i]) + '\n')


def black_and_white(out_dir, save_dir):
    color_pictures = out_dir
    files = os.listdir(color_pictures)
    print(out_dir)
    i = 0

    for file in files:
        i += 1
        print(save_dir + file)

        img = cv2.imread(color_pictures + file, cv2.IMREAD_UNCHANGED)
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


def euclidean_metric(inp):
    total = 100000
    index = -1

    for legend in legend_list:
        new_total = np.linalg.norm(np.array(legend) - inp)
        if new_total < total:
            total = new_total
            index = legend_list.index(legend)
    return index


def algoritm(path, path_save, path_mask, path_save_mask):
    files = os.listdir(path)
    for file in files:
        name, format = file.split(".", 1)

        print(path_mask + name + "." + format)
        img = cv2.imread(path + name + "." + format, cv2.IMREAD_UNCHANGED)
        img_seg = cv2.imread(path_mask + name + "." + format, cv2.IMREAD_UNCHANGED)
        print(img_seg)

        windowSize = [416, 608]
        # stepSize = 750 # было 50, потом 200
        # stepSize = np.random.randint(700, 800)

        for y in range(0, img.shape[0], np.random.randint(500, 800)):
            for x in range(0, img.shape[1], np.random.randint(500, 800)):
                try:
                    crop_img = img[y:y + windowSize[0], x:x + windowSize[1]]
                    crop_img_seg = img_seg[y:y + windowSize[0], x:x + windowSize[1]]
                    print('try!')
                    l = len(str(file))
                    name = file[:l-4]
                    print('save: ', path_save + name + str(y) + str(x) + '.png')
                    cv2.imwrite(path_save + name + str(y) + str(x) + '.png', crop_img)
                    cv2.imwrite(path_save_mask + name + str(y) + str(x) + '.png', crop_img_seg)
                except:
                    IndexError
    return 0


def delete_img(path):
    files = os.listdir(path)
    for file in files:
        img = cv2.imread(path + file, cv2.IMREAD_UNCHANGED)
        print(np.shape(img))
        # print(np.shape(img)[0], np.shape(img)[1], np.shape(img)[2])
        if np.shape(img)[0] != 416:
            os.remove(path + file)
        elif np.shape(img)[1] != 608:
            os.remove(path + file)


def check(path_mask, file):
    img = cv2.imread(path_mask + file, cv2.IMREAD_UNCHANGED)
    h, w, z = np.shape(img)
    flag = 0
    for i in range(h):
        for j in range(w):
            if img[i][j][0] == 0 & img[i][j][1] == 0 & img[i][j][2] == 0:
                flag += 1
        if flag >= 75:
            return True
        else:
            return False


def delete_color(path):

    list_of_names = []
    path_mask = path + 'mask/'
    files = os.listdir(path_mask)
    files.sort()
    for file in files:
        print(file)
        if check(path_mask, file):
            list_of_names.append(file)
            print('mask: ', path_mask + file)
            os.remove(path_mask + file)

    path_img = path + 'img/'
    files = os.listdir(path_img)
    files.sort()
    i = 0
    for file in files:
        for img in list_of_names:
            if file == img:
                print('img: ', path_img + file)
                os.remove(path_img + file)
                break;
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


def make_txt(root, path, pathmask, dir):

    f = open(root + str(dir) + '.txt', 'w')
    n = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    m = len([name for name in os.listdir(pathmask) if os.path.isfile(os.path.join(pathmask, name))])

    print(n, m)

    list_path = []
    list_mask = []

    for name in os.listdir(path):
        list_path.append('/make_data/' + str(path) + str(name))

    for name in os.listdir(pathmask):
        list_mask.append('/make_data/' + str(pathmask) + str(name))

    for i in range(n):
        f.write(str(list_path[i]) + ' ' + str(list_mask[i]) + '\n')


def histogram_equalize(im, path):
    print(im)
    img = cv2.imread(path + im, cv2.IMREAD_UNCHANGED)
    # print(img)
    b, g, r = cv2.split(img)
    red = cv2.equalizeHist(r)
    green = cv2.equalizeHist(g)
    blue = cv2.equalizeHist(b)
    return cv2.merge((blue, green, red))


def hist_all_pictures_in_folder(path):
    files = os.listdir(path)
    i = 0
    for file in files:
        img = histogram_equalize(file, path)
        cv2.imwrite(path + str(i) + '.png', img)
        i += 1

# TODO:  80 к 20 на train и test
# TODO:  затем train 80 к 20
# TODO:  Хельсинки, картинки 2, 3, 4, 9 -- train, test -- 7
# TODO:  ls -l | grep ^- | wc -l


if __name__ == '__main__':

    os.system("find /Users/kate/PycharmProjects/make_data -name '.DS_Store' -delete")

    path = "4_CHANNELS_DATA/img/"
    moveto = '4_CHANNELS_DATA/train/'
    n = 1214
    move_pictures(path, moveto, n)

    path = "4_CHANNELS_DATA/mask/"
    moveto = '4_CHANNELS_DATA/trainmask/'
    n = 1214
    move_pictures(path, moveto, n)

    path = "4_CHANNELS_DATA/img/"
    moveto = '4_CHANNELS_DATA/val/'
    n = 303
    move_pictures(path, moveto, n)

    path = "4_CHANNELS_DATA/mask/"
    moveto = '4_CHANNELS_DATA/valmask/'
    n = 1214
    move_pictures(path, moveto, n)