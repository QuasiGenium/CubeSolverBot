import cv2
import os
from kubfu import get_colors, new_rombs, edit_points_of_square
from math import sqrt

def make_contours(im, save_name):
    all_colors = []
    image = cv2.imread(im)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresholded = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]

    # Поиск контуров на изображении
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)
        cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)
        cv2.drawContours(image, [approx], -1, (0, 0, 255), 2)
        for i in range(9):
            all_colors.append(get_colors(im, new_rombs(edit_points_of_square(approx))[i]))

        cv2.drawContours(image, list(new_rombs(edit_points_of_square(approx))), -1, (0, 0, 255), 2)
        save_path = os.path.join("buffer", save_name)
        cv2.imwrite(save_path, image)
        return all_colors
    else:
        return None


def colors_into_code(s):
    c_table = {4: 'y', 13: 'r', 22: 'b', 31: 'w', 40: 'o', 49: 'g'}
    output = [0] * 54
    nos = []
    prol = []
    centers = []
    for _ in s:
        nos.extend(_)
    allg = list(enumerate(nos))
    for i in range(54):
        if i % 9 == 4:
            centers.append(allg[i])
        else:
            prol.append(allg[i])
    for i in centers:
        output[i[0]] = c_table[i[0]]
        d = lambda x: sqrt((i[1][0] - x[1][0])**2 + (i[1][1] - x[1][1])**2 + (i[1][2] - x[1][2])**2)
        prol.sort(key=d)
        for j in range(8):
            output[prol[j][0]] = c_table[i[0]]
        for j in range(8):
            prol.pop(0)
    for i in range(6):
        for j in range(3):
            output[j + i * 9], output[j + i * 9 + 6] = output[j + i * 9 + 6], output[j + i * 9]

    return output