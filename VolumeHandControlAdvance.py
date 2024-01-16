import cv2
import HandTrackingModule as htm
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#####################################
wCam, hCam = 640, 480
#####################################

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detection_confidence=0.7, max_hands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        # Get the coordinates of thumb and index finger
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # Draw a line connecting thumb and index finger
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Calculate the length of the line (distance between thumb and index finger)
        length = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)

        # Hand range is between 50 and 300, map the length to the volume range
        volumeRange = length - 50
        if volumeRange < 0:
            volumeRange = 0
        if volumeRange > 300:
            volumeRange = 300

        # Map the volume range to the system volume range (0 to -65.25 dB)
        volume.SetMasterVolumeLevelScalar(volumeRange / 300, None)

        # Display the volume bar on the screen
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(150 + (volumeRange / 300) * 250)), (85, 400), (0, 255, 0), cv2.FILLED)

    # Display the image
    cv2.imshow("Img", img)
    cv2.waitKey(1)



