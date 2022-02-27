import sys
width = 1376 # resolution of the Camera 
height = 768
num_classes = 90 # number of classes to detect

check_for_internet = True # Online - using gTTS as TTS, Offline - using Pyttsx3
tts_toggle = True         # Text-to-speech toggle
print_tts = True          # Print TTS message in the console
print_fps = True          # Print frames per second in the top left corner of frame

choose = 1 #  1 - COCO;  2 - RUBIKS CUBE;  3 - MASKS; 4 - CATS and DOGS

model = 'SSD_MobileNet' #Model directory name




if len(sys.argv)==1:
    param=choose
else:
    param=int(sys.argv[1])

if param==1:
    graph = 'frozen_inference_graph.pb'
    labels = 'mscoco_label_map.pbtxt'
elif param==2:
    graph = 'frozen_inference_graph_cube.pb'
    labels = 'cube.pbtxt'
elif param==3:
    graph = 'frozen_inference_graph_mask.pb'
    labels = 'masks.pbtxt'
elif param==4:
    graph = 'frozen_inference_graph_cats.pb'
    labels = 'cats.pbtxt'
else:
    print("else")
    graph = 'frozen_inference_graph.pb'
    labels = 'mscoco_label_map.pbtxt'
    
isSpeaking = False