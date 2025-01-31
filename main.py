import cv2
import numpy as np
import math
import time
from pushover import init, Client
import datetime


api_token = 'aji8tvfc48p6dfqjdb64p4srsbao1h'
user_key = 'uwrxxjcxid32gdh3qg4rg9apdm1eeu'
init(api_token)
cap = cv2.VideoCapture("alan_npc.MOV")

count = 0
count1 = 0
slope = 0
slope1 = 100
minArea = 120 * 100
radianToDegree = 57.324
minimumLengthOfLine = 150.0
minAngle = 18
maxAngle = 72
list_falls = []
count_fall = 0
firstFrame = None
sent = False
time.sleep(1)
current_datetime = datetime.datetime.now()
current_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


# Function definition for frame conversion
def convertFrame(frame):
    screen_width = 720  # Adjust the width of your screen resolution
    screen_height = 600  # Adjust the height of your screen resolution

    scale_width = screen_width / frame.shape[1]
    scale_height = screen_height / frame.shape[0]
    scale = min(scale_width, scale_height)

    window_width = int(frame.shape[1] * scale)
    window_height = int(frame.shape[0] * scale)

    frame = cv2.resize(frame, (window_width, window_height), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)

    return frame, gray

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter('output.mp4', fourcc, 30.0, (720, 600))

# Create a Pushover client
pushover_client = Client(user_key)

fall_detected = False
fall_detected_start_time = 0
fall_detected_duration = 2.0  # Display time for fall detected text (in seconds)
message = 'Our computer vision system has detected on ' + current_time + ' that your grandpa might need help! Be sure to check on them! (This could be a false alarm) '
while True:
    ret, frame = cap.read()
    if frame is None:
        break
    frame, gray = convertFrame(frame)

    # Comparison Frame
    if firstFrame is None:
        time.sleep(1.0)
        _, frame = cap.read()
        frame, gray = convertFrame(frame)
        firstFrame = gray
        continue

    # Frame difference between current and comparison frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    # Thresholding
    thresh1 = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
    # Dilation of Pixels
    thresh = cv2.dilate(thresh1, None, iterations=15)

    # Finding the Region of Interest with changes
    contour, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for con in contour:

        if len(con) >= 5 and cv2.contourArea(con) > minArea:
            ellipse = cv2.fitEllipse(con)
            cv2.ellipse(frame, ellipse, (255, 255, 0), 5)

            # Co-ordinates of extreme points
            extTop = tuple(con[con[:, :, 1].argmin()][0])
            extBot = tuple(con[con[:, :, 1].argmax()][0])
            extLeft = tuple(con[con[:, :, 0].argmin()][0])
            extRight = tuple(con[con[:, :, 0].argmax()][0])

            line1 = math.sqrt((extTop[0] - extBot[0]) * (extTop[0] - extBot[0]) + (extTop[1] - extBot[1]) * (
                    extTop[1] - extBot[1]))
            midPoint = [extTop[0] - int((extTop[0] - extBot[0]) / 2),
                        extTop[1] - int((extTop[1] - extBot[1]) / 2)]
            if line1 > minimumLengthOfLine:
                if extTop[0] != extBot[0]:
                    slope = abs(extTop[1] - extBot[1]) / (extTop[0] - extBot[0])

            else:
                if extRight[0] != extLeft[0]:
                    slope = abs(extRight[1] - extLeft[1]) / (extRight[0] - extLeft[0])

            # Angle in Radians with perpendicular
            originalAngleP = np.arctan((slope1 - slope) / (1 + slope1 * slope))
            # Angle with Horizontal
            originalAngleH = np.arctan(slope)
            # Angle in degrees
            originalAngleH = originalAngleH * radianToDegree
            originalAngleP = originalAngleP * radianToDegree

            if (abs(originalAngleP) > minAngle and abs(originalAngleH) < maxAngle and abs(
                    originalAngleP) + abs(originalAngleH) > 89 and abs(
                    originalAngleP) + abs(originalAngleH) < 91):
                count += 1
                if count > 18:
                    count_fall += 1
                    list_falls.append((time.time()))
                    if count_fall > 1:
                        if list_falls[len(list_falls) - 1] - list_falls[len(list_falls) - 2] < 0.5:
                            fall_detected = True
                            fall_detected_start_time = time.time()
                        else:
                            continue
                    count = 0

    # Display "Fall detected" text if fall is detected
    if fall_detected:
        cv2.putText(frame, "Fall detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if time.time() - fall_detected_start_time >= fall_detected_duration:
            fall_detected = False
        if sent == False:
            pushover_client.send_message(message, title='Medical Emergency', attachment='image.jpg')
            sent = True
            print('Notification sent successfully!')


    # Save the modified frame with text overlay to the output video
    output.write(frame)

    cv2.imshow('Frame', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
output.release()
cv2.waitKey(1)
cv2.destroyAllWindows()
