import cv2
import numpy as np
import os


def overlay_img(path_orig, path_lines, path_save):
    files = os.listdir(path_orig)
    files.sort()

    for file in files:
        name = str(file).split(".")[0]
        print(path_orig + name + '.jpg')
        overlay = cv2.imread(path_orig + name + '.jpg')
        print(path_lines + name + '.png')
        background = cv2.imread(path_lines + name + '.png')

        new_image = cv2.addWeighted(background, 0.7, overlay, 0.8, 0)

        print(path_save, " ", name)
        cv2.imwrite(path_save + name + '.png', new_image)


def sobel(path, path_save):
    files = os.listdir(path)
    files.sort()

    for file in files:
        img = cv2.imread(path + file)
        img = np.sqrt(img)
        print(np.shape(img))

        sobelx = cv2.Sobel(np.float32(img), cv2.CV_64F, 1, 0)
        sobely = cv2.Sobel(np.float32(img), cv2.CV_64F, 0, 1)

        mag, ang = cv2.cartToPolar(sobelx, sobely)

        name = str(file).split(".")[0]

        print(path_save, " ", name)
        cv2.imwrite(path_save + name + '.png', mag)


def treshhold(path, path_save):
    files = os.listdir(path)
    files.sort()

    for file in files:

        img = cv2.imread(path + file)

        # Remember -> OpenCV stores things in BGR order
        lower = np.array([225, 225, 230])
        upper = np.array([240, 240, 240])
        new_img = cv2.inRange(img, lower, upper)

        name = str(file).split(".")[0]

        print(path_save, " ", name)
        cv2.imwrite(path_save + name + '.png', new_img)


def canny(path, path_save):
    files = os.listdir(path)
    files.sort()

    for file in files:
        img = cv2.imread(path + file)
        b_channel, g_channel, r_channel = cv2.split(img)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray_img, 100, 200) # было 175 на 220 и 7
        name = str(file).split(".")[0]

        img_with_edges = cv2.merge((b_channel, g_channel, r_channel, edges))
        print(np.shape(img_with_edges), img_with_edges[0][0])
        cv2.imwrite(path_save + name + '.png', img_with_edges)


def invert(path, path_save):
    files = os.listdir(path)
    files.sort()

    for file in files:
        img = cv2.imread(path + file)
        new_img = cv2.bitwise_not(img)

        name = str(file).split(".")[0]
        print(path_save, " ", name)
        cv2.imwrite(path_save + name + '.png', new_img)

if __name__ == '__main__':

    os.system("find /Users/kate/PycharmProjects/make_data -name '.DS_Store' -delete")

    path = "Airports/!MINEhelsinki/lines/"
    path_save = "Airports/!MINEhelsinki/canny/"
    path_orig = "Airports/!MINEhelsinki/img/"
    canny(path, path_save, path_orig)