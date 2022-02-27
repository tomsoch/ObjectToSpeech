import cv2
import time
import pyttsx3
from gtts import gTTS
from io import BytesIO
from pygame import mixer
import settings
import requests
import random

def read_labels(path):

    label_id = None
    label_name = None
    labels_dict = {}

    with open(path, "r") as pbtxt:
        for row in pbtxt:
            row.replace(" ", "")
            if row == "item{":
                pass
            elif row == "}":
                pass
            elif "id" in row:
                label_id = int(row.split(":", 1)[1].strip())
            elif "display_name" in row:
                label_name = row.split(":")[-1].replace("\"", " ").strip()
            if label_id is not None and label_name is not None:
                labels_dict[label_id] = label_name
                label_id = None
                label_name = None
    return labels_dict

def isConnected():
    url = "http://www.google.com"
    timeout = 5
    try:
        print("Connecting to the Internet...")
        requests.get(url, timeout=timeout)
        print("Internet connection established")
        return True
    except (requests.ConnectionError, requests.Timeout):
        print("No Internet connection")
    return False

def color_seed(name):
    adder = sum(bytearray(name, "utf-8"))
    random.seed(adder)
    r = random.randint(0, 255)
    random.seed(adder+10)
    g = random.randint(0, 255)
    random.seed(adder+20)
    b = random.randint(0, 255)
    random.seed(adder+40)
    return (r,g,b)
    

def draw_bounding_box(frame, names, coords, scores, obj_number, width, height):
    if len(coords) > 0:
        for j in range(obj_number):
            ymin = int(coords[j][0] * height)
            xmin = int(coords[j][1] * width)
            ymax = int(coords[j][2] * height)
            xmax = int(coords[j][3] * width)
            
            object_name = names[j]
            r,g,b = color_seed(object_name)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (r, g, b), 5)
            label = '%s: %d%%' % (object_name, int(scores[0][j] * 100))
            font_size, bot_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            top_margin = max(ymin, font_size[1] + 10)
            cv2.rectangle(frame, (xmin, top_margin - font_size[1] - 10),
                          (xmin + font_size[0], top_margin + bot_line - 10), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, label, (xmin, top_margin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

def init_engine():
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty('voice', 'english_rp+f2')
    return engine

def tts(coords, obj_number, names, connected):
    if settings.isSpeaking is False and obj_number > 0:
        words = []
        settings.isSpeaking = True
        for j in range(obj_number):
            if j == 0:
                words.append('I see ')
                if obj_number > 1:
                    words.append(str(obj_number) + ' objects: ')
            if (names[j][0]== 'a' or names[j][0]== 'e' or names[j][0]== 'i' or names[j][0]== 'o' or names[j][0]== 'u'):
                words.append('an ')
            else:
                words.append('a ')
            words.append(names[j])
            words.append(' at ')
            ycentre = (coords[j][0] + coords[j][2]) / 2
            xcentre = (coords[j][1] + coords[j][3]) / 2
            tempCoords = []
            if ycentre < 0.382:
                tempCoords.append('the top')
            elif ycentre > 0.618:
                tempCoords.append('the bottom')
            if xcentre < 0.382:
                tempCoords.append('left')
            elif xcentre > 0.618:
                tempCoords.append('right')
            if len(tempCoords) == 2:
                tempCoords.append('corner')
            if (0.382 < xcentre < 0.618) and (0.382 < ycentre < 0.618):
                tempCoords.append('the centre')

            tempCoords = ' '.join(tempCoords)
            words.append(tempCoords)

            if j == obj_number - 2:
                words.append(' and ')
            elif j == obj_number - 1:
                words.append('.')
            else:
                words.append(', ')
        phrase = ''.join(words)
        
        if connected:
            tts = gTTS(text=phrase, lang='en')
            mp3 = BytesIO()
            tts.write_to_fp(mp3)
            mp3.seek(0)
            mixer.init()
            mixer.music.load(mp3)
            mixer.music.play()
            if settings.print_tts:
                print("TTS: ", phrase)
            while True:
                if mixer.music.get_busy() == True:
                    settings.isSpeaking = True
                    time.sleep(0.2)
                else:
                    settings.isSpeaking = False
                    time.sleep(0.2)
                    break
        else:
            try:
                engine = init_engine()
                engine.say(phrase)
                engine.runAndWait()
                if settings.print_tts:
                    print("TTS: ", phrase)
            except:
                time.sleep(0.2)
            time.sleep(0.2)
            settings.isSpeaking = False
