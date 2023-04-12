# Tello Drone Face Tracker

![stars](https://img.shields.io/github/stars/myoluk/tello-drone-face-tracker)
![forks](https://img.shields.io/github/forks/myoluk/tello-drone-face-tracker)
![licence](https://img.shields.io/github/license/myoluk/tello-drone-face-tracker)
![last-commit](https://img.shields.io/github/last-commit/myoluk/tello-drone-face-tracker)

:star: Allows **autonomous** flight by processing the images taken with Tello

:white_check_mark: **OpenCV** Haar feature-based cascade classifiers used for face detection

:white_check_mark: [DJITelloPy](https://pypi.org/project/djitellopy) Python library used for communication with Tello

:white_check_mark: **6 DOF** (Six Degrees of Freedom) maneuverable

:point_right: DJI Tello [official site](https://store.dji.com/shop/tello-series)

![Tello Drone Face Tracker](images/tello-drone-face-tracker.png)

:white_check_mark: [PID](https://en.wikipedia.org/wiki/PID_controller) (proportional–integral–derivative) controller used for stabilization

![PID](images/pid-diagram.png)

:white_check_mark: `pError` controls the x-axis, `pError_y` controls the y-axis

![PID Errors](images/p-error-axis.png)
