import cv2
import time
import numpy as np

cap = cv2.VideoCapture(1)
time.sleep(1)


def draw_boxes_around_shapes(my_contours,img):
    for each_contour in my_contours:
        print("Size of contour:", cv2.contourArea(each_contour))
        x,y,w,h = cv2.boundingRect(each_contour)
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),2)

    


while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gaus = cv2.GaussianBlur(hsv, (15,15), 0)
    blurred = cv2.medianBlur(hsv, 15)
    kernel = np.ones((5,5),np.uint8)


    # For blue colors
    lower_blue = np.array([110,150,70])
    upper_blue = np.array([130,255,255])
    mask = cv2.inRange(blurred, lower_blue, upper_blue)

    # For red colors
    # lower_red1 = np.array([0,10,80])
    # upper_red1 = np.array([10,255,255])

    # lower_red2 = np.array([170,100,100])
    # upper_red2 = np.array([180,255,255])

    # mask1 = cv2.inRange(blurred, lower_red1, upper_red1)
    # mask2 = cv2.inRange(blurred, lower_red2, upper_red2)
    # mask = mask1 + mask2



    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE,kernel)

    _, contours, _ = cv2.findContours(closing, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
    # Fills areas with contours that have an Area greater than 800
    list_of_good_contours = [c for c in contours if cv2.contourArea(c) > 800]
    

    mask_inv = cv2.bitwise_not(closing)

    # Not necessary, but makes a really cool hsv overlay
    bg = cv2.bitwise_and(frame,frame,mask=mask_inv)
    fg = cv2.bitwise_and(hsv,hsv,mask=closing)
    dst = cv2.add(fg, bg)

    # cv2.drawContours(dst,contours,-1, (0,0,255), 2)

    if len(areas) != 0:
        draw_boxes_around_shapes(list_of_good_contours, dst)
        print("Number of contours detected:",len(list_of_good_contours))
    else:
        print("No contours detected")

    cv2.imshow('default', dst)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
