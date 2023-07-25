import cv2 as cv
from cv2 import aruco
import numpy as np


calib_data = np.load("calib_data.npz")

cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

MARKER_SIZE = 5.5  # cm

marker_params = aruco.DetectorParameters()
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, rejects = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=marker_params
    )
    if marker_corners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            marker_corners, MARKER_SIZE, cam_mat, dist_coef
        )

        aruco.drawDetectedMarkers(frame, marker_corners, marker_IDs)
        total_markers = range(0, marker_IDs.size)
        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            # Calculating the distance
            distance = np.sqrt(
                tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
            )
            # print(tuple(corners[0][0].astype("int32")))
            cv.putText(
                frame,
                f"id: {ids[0]} Dist: {round(distance, 2)} \nHeight: {round(tVec[i][0][2])}",
                tuple(corners[i][0].astype("int32")),
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            rmat = cv.Rodrigues(rVec[i])[0]
            position_mat = cv.hconcat((rmat, tVec[i][0]))
            _, _, _, _, _, _, euler_angles = cv.decomposeProjectionMatrix(position_mat)
            euler_angles = euler_angles.astype("int32")
            cv.putText(
                frame,
                f"Roll: {euler_angles[2]} \nPitch: {euler_angles[1]} \nYaw: {euler_angles[0]}",
                tuple(corners[i][2].astype("int32")),
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            # Draw the pose of the marker
            point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)

    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv.destroyAllWindows()
