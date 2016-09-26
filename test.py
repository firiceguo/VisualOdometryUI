import cv2
import numpy as np

img = cv2.imread("./data/perspectiveimg.jpg", 0)
w = img.shape[1]
h = img.shape[0]
img_points = []
# pattern_size = (7, 7)

# found, corners = cv2.findChessboardCorners(img, pattern_size)
# if found:
#     term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
#     cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)
#     img_points.append(corners.reshape(-1, 2))
# if not found:
#     print("corners not found")

print(img_points)
src = [[186, 361], [449, 361],
       [133, 466], [508, 466]]
src = np.array(src, np.float32)
dst = np.array([[w // 2 - 100, h - 200], [w // 2 + 100, h - 200], [w // 2 - 100, h], [w // 2 + 100, h]], np.float32)
# dst = np.array([[0, 0], [300, 0], [0, 300], [300, 300]], np.float32)
ret = cv2.getPerspectiveTransform(src, dst)
pic = cv2.warpPerspective(img, ret, (w, h))
cv2.imwrite('./output/out.jpg', pic)
