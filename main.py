import cv2
import time
from send_mail import send_email

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []

while 1:
    status = 0

    check, frame = video.read()
    # Configure the frames to simplify the comparison of images by doing grayscale and gaussian blur
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # cv2.imshow("My video", gray_frame_gau) --> preprocessing feed-- to display gaussian view

    # Capture the first frame
    if first_frame is None:
        first_frame = gray_frame_gau
    # set delta feed  to create difference when an object enters
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # to remove shadow effects and set whites to pure whites to differentiate object from background
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # more processing to set the feed with object and background differentiated.
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # cv2.imshow("My video", dil_frame) --> processed feed to see threshold view(dilated view)

    # to create contours around the object
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # To remove smaller objects-- unintended objects
        if cv2.contourArea(contour) < 5000:
            continue
        # get dimensions around the  object contour
        x, y, w, h = cv2.boundingRect(contour)

        # create  green rectangle around the object
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        # updating status variable if an object is detected(in rectangle)
        if rectangle.any():
            status = 1

    # updating status list based on status
    status_list.append(status)
    status_list = status_list[-2:]

    # Checking the exit of object based on status list and trigger email
    if status_list[0] == 1 and status_list[1] == 0:
        print("send email")

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
