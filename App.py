import os
import pyttsx3
import json
import threading
import numpy as np
import tensorflow as tf
from picamera import PiCamera
from picamera.array import PiRGBArray
from utilities import *
import settings

print("\n",'\033[1m',"Launching an application for object recognition and voice notifications",'\033[0m')

if settings.check_for_internet:
    connected = isConnected()
else:
    connected = False
    print("Checking for internet connection is turned off")

if settings.tts_toggle:
    print("Text-to-speech is turned ON")
else:
    print("Text-to-speech is turned OFF")

if settings.print_tts:
    print("Printing Text-to-speech is turned ON")
else:
    print("Printing Text-to-speech is turned OFF")
    
width = settings.width
height = settings.height

model_name = settings.model
current_dir = os.getcwd()
path_graph = os.path.join(current_dir, model_name, settings.graph)

labels=read_labels(os.path.join(model_name, settings.labels))

num_classes = settings.num_classes

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.compat.v2.io.gfile.GFile(path_graph, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    print("Initializing Tensorflow")
    sess = tf.compat.v1.Session(graph=detection_graph)

image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

fps = 1
frequency = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

print("Launching Pi Camera")
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(width, height))
rawCapture.truncate(0)



run_once = 0
settings.isSpeaking = False
    
print("Starting the detection")

for frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    t1 = cv2.getTickCount()

    frame = np.copy(frame1.array)
    frame.setflags(write=1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_expanded = np.expand_dims(frame_rgb, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})

    if run_once == 0:
        print("\nPress 'Space' to exit the app\n")
        run_once = 1

    coords = []
    names = []
    s_boxes = boxes[scores > 0.5]

    for s in s_boxes:
        coords.append(s)
    obj_number = len(coords)

    for j in range(int(num)):
        names.append(labels[classes[0][j]])

    draw_bounding_box(frame, names, coords, scores, obj_number, width, height)
    if settings.tts_toggle and settings.isSpeaking==False:
        x = threading.Thread(target=tts, daemon=True, args=(coords, obj_number, names, connected))
        x.start()
        
    if settings.print_fps:
        cv2.putText(frame, "fps: {0:.2f}".format(fps), (30, 50), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Detection App', frame)

    t2 = cv2.getTickCount()
    fps = 1 / ((t2 - t1) / frequency)

    if cv2.waitKey(1) == ord(' '):
        break
    
    rawCapture.truncate(0)
print("\nExiting the app...\n")
camera.close()

cv2.destroyAllWindows()
