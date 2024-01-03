import cv2 as cv
import numpy as np
import random as rng

rng.seed(99999)

IMAGE_PATH = r'input11.jpeg'
THRESH_MINI = 100
THRESH_MAX_VAL = 255
MIN_SIZE = 1000


def connected_comp_analysis(image):
    image = image.astype('uint8')

    nb_components, output, stats, centroids = cv.connectedComponentsWithStats(
        image, connectivity=8)

    sizes = stats[1:, -1]
    x, y, width, height = stats[1:, 0], stats[1:,
                                              1], stats[1:, 2], stats[1:, 3]

    nb_components = nb_components - 1

    min_size = MIN_SIZE

    img2 = np.zeros((output.shape))
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            img2[output == i + 1] = 255
            print("X : ", x[i])
            print("Y : ", y[i])
            print("Width : ", width[i])
            print("Height : ", height[i])
            print("Area : ", sizes[i])
            print()

    return img2.astype('uint8')


def filling(im_th):
    im_floodfill = im_th.copy()
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv.floodFill(im_floodfill, mask, (0, 0), 255)
    im_floodfill_inv = cv.bitwise_not(im_floodfill)
    im_out = im_th | im_floodfill_inv
    return [im_floodfill, im_floodfill_inv]


def draw_bounding_boxes(threshold, given_img):

    canny_output = cv.Canny(given_img, threshold, threshold * 2)
    contours, hierarchy = cv.findContours(
        canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    drawing = np.zeros(
        (canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

    contour_color = (0, 0, 255)

    for i, c in enumerate(contours):
        boundRect = cv.boundingRect(c)

        cv.rectangle(drawing, (int(boundRect[0]), int(boundRect[1])),
                     (int(boundRect[0] + boundRect[2]), int(boundRect[1] + boundRect[3])), contour_color, 2)

    cv.imshow('Contours', drawing)


normal_image = cv.imread(IMAGE_PATH)

src = cv.imread(IMAGE_PATH, cv.IMREAD_GRAYSCALE)
cv.imshow("orig", src)

src_gray = cv.blur(src, (3, 3))
th, im_th = cv.threshold(src_gray, THRESH_MINI,
                         THRESH_MAX_VAL, cv.THRESH_BINARY_INV)
cv.imshow("gray", im_th)


im_th = connected_comp_analysis(im_th, normal_image)
cv.imshow('Character Removal', im_th)

im_floodfill, im_floodfill_inv = filling(im_th)
cv.imshow("Floodfilled Image", im_floodfill)
cv.imshow("Inverted Floodfilled Image", im_floodfill_inv)

draw_bounding_boxes(100, im_floodfill_inv)

cv.waitKey()
