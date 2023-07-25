# Localisation (Task 4) 

This project contains two parts:
- Camera Caliberation
- Pose Estimation using Aruco Tags

## Camera Calibration
This section consists of two files ``capture_calib_images.py`` and ``camera_calib.py`` implemented as per the OpenCV documnetation.

``camera_calib.py`` utilises the images of the 9x6 checkboard captured using ``capture_calib_images.py`` in order to calibrate the camera and find its parameters. These are then saved to the file ``calib_data.npz`` and used in the next section.


Reference:  *[OpenCV documentation for calibration](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)*

## Pose Estimation using Aruco Tags
This part is implemented using ``aruco.py``. 

The marker is first detected using the ArUco library. The camera calibration data and the marker size are then used to figure out the mapping between camera coordinates and real world coordinates, which is further used to measure the distance and orientation of the camera with respect to the marker. 


Reference:  *[OpenCV documentation for pose estimation](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)*
