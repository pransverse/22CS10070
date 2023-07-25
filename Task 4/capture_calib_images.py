import cv2 as cv
import glob
import numpy as np

CHESS_BOARD_DIM = (9, 6)

calib_img_dir = "calib_images"
n = 1  # image counter

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def detect_checker_board(img, grayimg, criteria, board_dim):
    ret, corners = cv.findChessboardCorners(grayimg, board_dim)
    if ret == True:
        corners2 = cv.cornerSubPix(
            grayimg, corners, (11, 11), (-1, -1), criteria
        )  # banda used 3x3
        img = cv.drawChessboardCorners(img, board_dim, corners2, ret)

    return img, ret


cap = cv.VideoCapture(0)

while True:
    _, frame = cap.read()
    copyframe = frame.copy()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    img, board_detected = detect_checker_board(frame, gray, criteria, CHESS_BOARD_DIM)

    cv.putText
    (
        frame,
        f"saved img no. {n}",
        (30, 40),
        cv.FONT_HERSHEY_PLAIN,
        1.4,
        (0, 255, 0),
        2,
        cv.LINE_AA,
    )

    cv.imshow("frame", frame)
    cv.imshow("copyframe", copyframe)

    key = cv.waitKey(1)

    # quit
    if key == ord("q"):
        break
    # save
    if key == ord("s") and board_detected:
        cv.imwrite(f"{calib_img_dir}/img{n}.png", copyframe)

        print(f"saved img no. {n}")
        n += 1

cap.release()
cv.destroyAllWindows()

print(f"Total saved images {n}")
