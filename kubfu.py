import cv2
import numpy as np

def edit_points_of_square(points):
    right_points = []
    r = [list(i[0]) for i in points]
    r.sort(key=lambda x: x[1])
    if r[0][0] < r[1][0]:
        right_points.append(r[0])
        if r[-1][0] < r[-2][0]:
            right_points.append(r[-1])
            right_points.append(r[-2])
        else:
            right_points.append(r[-2])
            right_points.append(r[-1])
        right_points.append(r[1])
    else:
        right_points.append(r[1])
        if r[-1][0] < r[-2][0]:
            right_points.append(r[-1])
            right_points.append(r[-2])
        else:
            right_points.append(r[-2])
            right_points.append(r[-1])
        right_points.append(r[0])

    return np.array(right_points)


def romb_from_square(points):
    up = (points[2] - points[1]) * 0.5 + points[1]
    down = (points[3] - points[0]) * 0.5 + points[0]
    left = (points[0] - points[1]) * 0.5 + points[1]
    right = (points[3] - points[2]) * 0.5 + points[2]
    return [up, right, down, left]

def new_rombs(points):
    c00 = points[1] + (points[0] - points[1]) * (1/3) + (points[2]-points[1]) * (1/3)
    c01 = points[2] + (points[3] - points[2]) * (1/3) - (points[2]-points[1]) * (1/3)
    c10 = points[0] + (points[3] - points[0]) * (1/3) - (points[0] - points[1]) * (1/3)
    c11 = points[3] - (points[3] - points[2]) * (1/3) - (points[3] - points[0]) * (1/3)

    rombs = [romb_from_square([points[1] + (points[0] - points[1]) * (1/3), points[1],points[1] + (points[2] - points[1]) * (1/3) ,c00]),
             romb_from_square([c00, points[1] + (points[2] - points[1]) * (1/3), points[1] + (points[2] - points[1]) * (2/3), c01]),
             romb_from_square([c01, points[1] + (points[2] - points[1]) * (2/3), points[2], points[2] + (points[3] - points[2]) * (1/3)]),

             romb_from_square([points[1] + (points[0] - points[1]) * (2/3), points[1] + (points[0] - points[1]) * (1/3), c00, c10]),
             romb_from_square([c10, c00, c01, c11]),
             romb_from_square([c11, c01, points[2] + (points[3] - points[2]) * (1/3), points[2] + (points[3] - points[2]) * (2/3)]),

             romb_from_square([points[0], points[1] + (points[0] - points[1]) * (2/3), c10, points[0] + (points[3] - points[0]) * (1/3)]),
             romb_from_square([points[0] + (points[3] - points[0]) * (1/3), c10, c11, points[0] + (points[3] - points[0]) * (2/3)]),
             romb_from_square([points[0] + (points[3] - points[0]) * (2/3), c11, points[2] + (points[3] - points[2]) * (2/3), points[3]])]
    for i in range(9):
        for j in range(4):
            rombs[i][j] = [[int(rombs[i][j][0]), int(rombs[i][j][1])]]
    return np.array(rombs)


def get_colors(image_path, points):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("не загрузил изо")

    pts = np.array(points, dtype=np.int32)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [pts], 255)
    mean_color = cv2.mean(img, mask=mask)[:3]
    return list(np.round(mean_color).astype(int))


