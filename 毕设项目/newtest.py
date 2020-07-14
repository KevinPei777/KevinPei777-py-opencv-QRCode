import cv2
import numpy as np

img = cv2.imread('test.png')
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

# 图片灰度化
gary = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, gray = cv2.threshold(gary, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
img, contours, hierachy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
tmp = np.squeeze(hierachy)
rec = []

def compute_1(contours, i, j):
    '''最外面的轮廓和子轮廓的比例'''
    area1 = cv2.contourArea(contours[i])
    area2 = cv2.contourArea(contours[j])
    if area2 == 0:
        return False
    ratio = area1 * 1.0 / area2
    if abs(ratio - 49.0 / 25):
        return True
    return False


def compute_2(contours, i, j):
    '''子轮廓和子子轮廓的比例'''
    area1 = cv2.contourArea(contours[i])
    area2 = cv2.contourArea(contours[j])
    if area2 == 0:
        return False
    ratio = area1 * 1.0 / area2
    if abs(ratio - 25.0 / 9):
        return True
    return False


def compute_center(contours, i):
    '''计算轮廓中心点'''
    M = cv2.moments(contours[i])
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    return cx, cy


def detect_contours(vec):
    '''判断这个轮廓和它的子轮廓以及子子轮廓的中心的间距是否足够小'''
    distance_1 = np.sqrt((vec[0] - vec[2]) ** 2 + (vec[1] - vec[3]) ** 2)
    distance_2 = np.sqrt((vec[0] - vec[4]) ** 2 + (vec[1] - vec[5]) ** 2)
    distance_3 = np.sqrt((vec[2] - vec[4]) ** 2 + (vec[3] - vec[5]) ** 2)
    if sum((distance_1, distance_2, distance_3)) / 3 < 3:
        return True
    return False


for i in range(len(tmp)):
    child = tmp[i][2]
    child_child = tmp[child][2]
    if child != -1 and tmp[child][2] != -1:
        if compute_1(contours, i, child) and compute_2(contours, child, child_child):
            cx1, cy1 = compute_center(contours, i)
            cx2, cy2 = compute_center(contours, child)
            cx3, cy3 = compute_center(contours, child_child)
            if detect_contours([cx1, cy1, cx2, cy2, cx3, cy3]):
                rec.append([cx1, cy1, cx2, cy2, cx3, cy3, i, child, child_child])  # for i in range(len(hierachy)):
print(len(rec))
# for i in rec:
#     img_dc = img.copy()
#     cv2.drawContours(img_dc, contours, i, (0, 255, 0), 3)
#     cv2.imshow('Image', img_dc)
#     cv2.waitKey(0)
img_fc, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

hierarchy = hierarchy[0]
found = []
for i in range(len(contours)):
    k = i
    c = 0
    while hierarchy[k][2] != -1:
        k = hierarchy[k][2]
        c = c + 1
    if c >= 5:
        found.append(i)

for i in found:
    img_dc = img.copy()
    cv2.drawContours(img_dc, contours, i, (0, 255, 0), 3)
    cv2.imshow("Image", img_dc)
    cv2.waitKey(0)