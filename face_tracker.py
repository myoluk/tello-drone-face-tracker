import cv2
import numpy as np
import time
import logging
from djitellopy import Tello

# width and height of the camera 360, 240
w, h = 360, 240

# pid values for smooth moving
pid = [0.35, 0.35, 0]
pError = 0
pError_y = 0

# face limit area
faceLimitArea = [8000, 10000]

# drone take off start value
takeoff = False
land = False

# initialize tello
def init_tello():
    tello = Tello()
    Tello.LOGGER.setLevel(logging.WARNING)
    tello.connect()
    print("Tello battery:", tello.get_battery())
    
    # velocity values
    tello.for_back_velocity = 0
    tello.left_right_velocity = 0
    tello.up_down_velocity = 0
    tello.yaw_velocity = 0
    tello.speed = 0
    
    # Streaming
    tello.streamoff()
    tello.streamon()
    
    return tello


# Get frame on stream
def get_frame(tello, w=w, h=h):
    tello_frame = tello.get_frame_read().frame
    return cv2.resize(tello_frame, (w,h))

# Detecting frontal faces on the given image
def face_detect(img):

    frontal_face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_faces = frontal_face.detectMultiScale(img_gray, 1.2, 8)

    # if there are more than 1 face on the given image
    face_list = []
    face_list_area = []
    
    # detected faces coordinates and sizes
    for (x, y, w, h) in img_faces:
        # draw a rectangle around faces
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        
        # center x, y coordinates
        cx = x + w//2
        cy = y + h//2
        
        # save detected face coordinated and its area
        face_list.append([cx, cy])
        face_list_area.append(w*h)

    # get face that closer on the camera (max area)
    # return given image and face_info (detected face coordinates and size)
    # that closer the camera
    if len(face_list_area) != 0:
        i = face_list_area.index(max(face_list_area))
        return img, [face_list[i], face_list_area[i]]
    else:
        return img, [[0,0],0]

# Tracking face smoothly with pid
def face_track(tello, face_info, w, h, pid, pError, pError_y):
    
    x = face_info[0][0]
    y = face_info[0][1]
    area = face_info[1]
    forw_backw = 0
    
    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -60, 60))

    error_y = h//(12/5) - y
    speed_y = pid[0]*error_y + pid[1]*(error_y - pError_y)
    speed_y = int(np.clip(speed_y, -60, 60))
    
    # set speeds to moving
    if x != 0:
        tello.yaw_velocity = speed
    else:
        speed = 0
        tello.yaw_velocity = speed
        error = 0
    
    if y != 0:
        tello.up_down_velocity = speed_y
    else:
        speed_y = 0
        tello.up_down_velocity = speed_y
        error_y = 0

    # Controlling the area size and moving forward, backward
    if area > faceLimitArea[0] and area < faceLimitArea[1]:
        forw_backw = 0
    elif area > faceLimitArea[1]:
        forw_backw = -10
    elif area < faceLimitArea[0] and area > 100:
        forw_backw = 10

    # send adjusted forward backward with adjusted speed
    tello.send_rc_control(0, forw_backw, speed_y, speed)
    return error, error_y


# initialize tello
tello = init_tello()

while True:

    # take off tello
    if takeoff == 0:
        try:
            tello.takeoff()
            tello.move_up(100)
            takeoff = True
            land = True
            time.sleep(2.2)
        except:
            pass
    
    # Press 'Q' to land
    if cv2.waitKey(1) & 0xFF == ord('q'):
        if land:
            try:
                tello.streamoff()
                tello.land()
            except:
                pass    
        break    
    

    # Stream on and get frame
    img = get_frame(tello, w, h)

    # Detect face on the frame
    img, face_info = face_detect(img)

    # Track face smoothly
    # Get current error for pid as pError (previous error)
    pError, pError_y = face_track(tello, face_info, w, h, pid, pError, pError_y)

    # Show frame
    img = cv2.putText(img, str(tello.get_battery()), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,100,250), 1, cv2.LINE_AA)
    img = cv2.putText(img, str('pError:'+str(pError)), (0,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,100,0), 1, cv2.LINE_AA)
    img = cv2.putText(img, str('pError_y:'+str(pError_y)), (0,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,100,0), 1, cv2.LINE_AA)
    img = cv2.putText(img, str('Area:'+str(face_info[1])), (0,120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,100,0), 1, cv2.LINE_AA)
    cv2.imshow("Image", img)


# Close all opened image windows
tello.streamoff()
cv2.destroyAllWindows()
