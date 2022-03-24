import cv2
import numpy as np
from datetime import datetime
import os
import time
class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']
class_counts = [0, 0, 0, 0, 0]
label_index = 0

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
root_folder = "data"
set_folder = "set-"+current_time
os.makedirs(os.path.join(root_folder,set_folder))
for label in class_labels:
    os.makedirs(os.path.join(root_folder,set_folder,label))


def gstreamer_pipeline(
        sensor_id = 0,
        capture_width = 1920,
        capture_height = 1080,
        display_width = 960,
        display_height = 540,
        framerate = 30,
        flip_method = 0,
    ):
    return ("nvarguscamerasrc sensor-id=%d !"
            "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                sensor_id,
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )

capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

while True:
    _, frame = capture.read()
    pressed_key = cv2.waitKey(1) & 0xFF
    if pressed_key == ord('q'):
        break
    elif pressed_key == ord('n'):
        label_index=(label_index+1)%5
        print("n")
    elif pressed_key == ord('c'):
        img_path = os.path.join(root_folder,set_folder, class_labels[label_index], str(class_counts[label_index])+".png")
        cv2.imwrite(img_path, frame)
        class_counts[label_index]+=1
        curr=time.time()
        print("c")
          
    cv2.putText(frame, class_labels[label_index]+ "#"+str(class_counts[label_index])+ " next is "+class_labels[(label_index+1)%5], (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
    cv2.imshow('Emotion :3', frame)
    
capture.release()
cv2.destroyAllWindows()
