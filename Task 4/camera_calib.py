import cv2 as cv
import numpy as np
import glob

CHESS_BOARD_DIM = (9, 6)

SQUARE_SIZE = 23  # mm


criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

obj_3D = np.zeros((CHESS_BOARD_DIM[0] * CHESS_BOARD_DIM[1], 3), np.float32)
obj_3D[:, :2] = np.mgrid[0 : CHESS_BOARD_DIM[0], 0 : CHESS_BOARD_DIM[1]].T.reshape(
    -1, 2
)

# hmm
obj_3D *= SQUARE_SIZE
print(obj_3D)

# Arrays to store object points and image points from all the images.
obj_points_3D = []  # 3d point in real world space
img_points_2D = []  # 2d points in image plane.

images = glob.glob("calib_images/*.png")
gray = np.array([])
for file in images:
    img = cv.imread(file)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, CHESS_BOARD_DIM)
    if ret == True:
        obj_points_3D.append(obj_3D)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        img_points_2D.append(corners2)

        img = cv.drawChessboardCorners(img, CHESS_BOARD_DIM, corners2, ret)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
    obj_points_3D, img_points_2D, gray.shape[::-1], None, None
)
print("calibrated")

# saving calibration data
np.savez(
    "calib_data",
    camMatrix=mtx,
    distCoef=dist,
    rVector=rvecs,
    tVector=tvecs,
)
