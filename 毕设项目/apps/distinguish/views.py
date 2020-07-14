from django.shortcuts import render
from django.views.generic import View
from django.http.response import JsonResponse
import base64
import cv2
import copy
import numpy as np
from pyzbar.pyzbar import decode
import re
# Create your views here.


class DistinguishView(View):
    def get(self, request):
        return render(request, 'Distinguish.html', {})


class DistinguishQRCodeViw(View):
    def post(self, request):
        src = request.body.decode('utf-8')
        if src[9:14] != 'image':
            return JsonResponse({"msg": "fail"})
        res = src.find('base64,')
        result_res = src[res + len('base64,'):]
        img = base64.b64decode(result_res)
        nparr = np.fromstring(img, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image, contours, hierachy = detecte(image)
        final_img = find(image, contours, np.squeeze(hierachy))
        if final_img is False:
            return JsonResponse({"msg": "fail"})
        result = decode(final_img)
        final = str(result[0].data)[2:-1]
        message = re.match("^([hH][tT]{2}[pP]://|[hH][tT]{2}[pP][sS]://|[wW]{3}\.)(([A-Za-z0-9-~]+).)+([A-Za-z0-9-~\\/])+$", final)
        if message is not None:
            print(final)
            return JsonResponse({"msg": 'url', "url": final, "text": ''})
        return JsonResponse({"msg": 'text', "url": '', "text": final})


# 提取所有轮廓
def detecte(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
    img, contours, hierachy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return image, contours, hierachy


# 最外面的轮廓和子轮廓的比例
def compute_1(contours, i, j):
    area1 = cv2.contourArea(contours[i])
    area2 = cv2.contourArea(contours[j])
    if area2 == 0:
        return False
    ratio = area1 * 1.0 / area2
    if abs(ratio - 49.0 / 25):
        return True
    return False


# 子轮廓和子子轮廓的比例
def compute_2(contours, i, j):
    area1 = cv2.contourArea(contours[i])
    area2 = cv2.contourArea(contours[j])
    if area2 == 0:
        return False
    ratio = area1 * 1.0 / area2
    if abs(ratio - 25.0 / 9):
        return True
    return False


# 计算轮廓中心点
def compute_center(contours, i):
    M = cv2.moments(contours[i])
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    return cx, cy


# 判断这个轮廓和它的子轮廓以及子子轮廓的中心的间距是否足够小
def detect_contours(vec):
    distance_1 = np.sqrt((vec[0] - vec[2]) ** 2 + (vec[1] - vec[3]) ** 2)
    distance_2 = np.sqrt((vec[0] - vec[4]) ** 2 + (vec[1] - vec[5]) ** 2)
    distance_3 = np.sqrt((vec[2] - vec[4]) ** 2 + (vec[3] - vec[5]) ** 2)
    if sum((distance_1, distance_2, distance_3)) / 3 < 3:
        return True
    return False


# 判断寻找是否有三个点可以围成等腰直角三角形
def juge_angle(rec):
    if len(rec) < 3:
        return -1, -1, -1
    for i in range(len(rec)):
        for j in range(i + 1, len(rec)):
            for k in range(j + 1, len(rec)):
                distance_1 = np.sqrt((rec[i][0] - rec[j][0]) ** 2 + (rec[i][1] - rec[j][1]) ** 2)
                distance_2 = np.sqrt((rec[i][0] - rec[k][0]) ** 2 + (rec[i][1] - rec[k][1]) ** 2)
                distance_3 = np.sqrt((rec[j][0] - rec[k][0]) ** 2 + (rec[j][1] - rec[k][1]) ** 2)
                if abs(distance_1 - distance_2) < 5:
                    if abs(np.sqrt(np.square(distance_1) + np.square(distance_2)) - distance_3) < 5:
                        return i, j, k
                elif abs(distance_1 - distance_3) < 5:
                    if abs(np.sqrt(np.square(distance_1) + np.square(distance_3)) - distance_2) < 5:
                        return i, j, k
                elif abs(distance_2 - distance_3) < 5:
                    if abs(np.sqrt(np.square(distance_2) + np.square(distance_3)) - distance_1) < 5:
                        return i, j, k
    return -1, -1, -1


# 找到符合要求的轮廓
def find(image, contours, hierachy, root=0):
    rec = []
    for i in range(len(hierachy)):
        child = hierachy[i][2]
        child_child = hierachy[child][2]
        if child != -1 and hierachy[child][2] != -1:
            if compute_1(contours, i, child) and compute_2(contours, child, child_child):
                cx1, cy1 = compute_center(contours, i)
                cx2, cy2 = compute_center(contours, child)
                cx3, cy3 = compute_center(contours, child_child)
                if detect_contours([cx1, cy1, cx2, cy2, cx3, cy3]):
                    rec.append([cx1, cy1, cx2, cy2, cx3, cy3, i, child, child_child])
    # 计算得到所有在比例上符合要求的轮廓中心点
    i, j, k = juge_angle(rec)
    if i == -1 or j == -1 or k == -1:
        return False
    ts = np.concatenate((contours[rec[i][6]], contours[rec[j][6]], contours[rec[k][6]]))
    rect = cv2.minAreaRect(ts)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    # print(box)
    x = []
    y = []
    for i in range(4):
        x.append(box[i][1])
        y.append(box[i][0])
    # print(x, y)
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    # print(x_min,x_max,y_min,y_max)
    result = copy.deepcopy(image)
    cv2.drawContours(result, [box], 0, (0, 0, 255), 2)
    cutrect = image[x_min:x_max, y_min:y_max]
    return cutrect
