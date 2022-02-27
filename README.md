# ObjectToSpeech
#### An application for recognizing objects in real time and describing their name and location in the frame by voice


![Detection App_screenshot2_03 12 2021](https://user-images.githubusercontent.com/73905822/155888748-e1a8aa8d-29cd-4323-bec4-50638a2289cc.png)

#### Exemplary messages printed by the application:


```
I see a person at the top right corner.
I see 2 objects: a chair at the bottom and a person at left.
I see 3 objects: a keyboard at right, a tv at top and a cup at the bottom left corner.
```

#### Hardware used in the project:
- Raspberry Pi 4
- Pi Camera v2

#### Models used for the object detection:
- MobileNet SSD v2 Lite
- MobileNet SSD v1

#### Object datasets used for training:
- Common Objects in Context (COCO)
- Custom dataset with Rubics Cubes
- Custom dataset with people wearing face masks
- Custom dataset with pictures of dogs and cats

#### Text to speech libraries:
- gTTs (when connection to the Internet is established)
- pyttsx3 (when being offline)

#### The Application creates the sentences based on the golden ratio division of the frame:
![ratiosframecropped](https://user-images.githubusercontent.com/73905822/155889425-2d37acc1-e5a2-4016-bd6d-a953be9342a4.png)

To install required packages run the following command:

`pip3 install -r requirements.txt`

Finally to launch the application run:

`python3 App.py`


