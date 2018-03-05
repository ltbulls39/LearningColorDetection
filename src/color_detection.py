import cv2
import time
import numpy as np

cap = cv2.VideoCapture(1)
time.sleep(1)


def draw_boxes_around_shapes(my_contours,img, color):
    number = 1
    if color == 'blue':
        box_shade = (0,255,0)
        col = 'Blue'
    else:
        box_shade = (100,100,255)
        col = 'Pink'

    for each_contour in my_contours:
        print("Size of contour:", cv2.contourArea(each_contour))
        x,y,w,h = cv2.boundingRect(each_contour)
        cv2.rectangle(img, (x,y),(x+w,y+h),box_shade,2)
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(img, col,(x,y -5),font, 2, (255,100,255),2,cv2.LINE_AA)
        cv2.putText(img, str(number), (x+w,y-5),font,2,(0,128,255),2,cv2.LINE_AA)
        number+=1

    


while True:
    _, frame = cap.read()
    

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gaus = cv2.GaussianBlur(hsv, (15,15), 0)
    blurred = cv2.medianBlur(hsv, 15)
    kernel = np.ones((5,5),np.uint8)


    # For blue colors
    lower_blue = np.array([110,150,70])
    upper_blue = np.array([130,255,255])
    blue_mask = cv2.inRange(blurred, lower_blue, upper_blue)

    lower_pink = np.array([145,100,100])
    upper_pink = np.array([175,255,255])
    pink_mask = cv2.inRange(hsv, lower_pink, upper_pink)

    # Smoothes out the masks, gets rid of noise
    pink_opening = cv2.morphologyEx(pink_mask,cv2.MORPH_OPEN, kernel)
    pink_closing = cv2.morphologyEx(pink_opening, cv2.MORPH_CLOSE, kernel)
    _, pink_contours, _ = cv2.findContours(pink_closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    blue_opening = cv2.morphologyEx(blue_mask,cv2.MORPH_OPEN, kernel)
    blue_closing = cv2.morphologyEx(blue_opening, cv2.MORPH_CLOSE,kernel)
    _, blue_contours, _ = cv2.findContours(blue_closing, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
    # Fills areas with contours that have an Area greater than 800
    list_of_good_pink_contours = [c for c in pink_contours if cv2.contourArea(c) > 800]
    list_of_good_blue_contours = [c for c in blue_contours if cv2.contourArea(c) > 800]
    
    pink_mask_inv = cv2.bitwise_not(pink_closing)
    blue_mask_inv = cv2.bitwise_not(blue_closing)

    # Not necessary, but makes a really cool hsv overlay
    bg = cv2.bitwise_and(frame,frame,mask=blue_mask_inv)
    fg = cv2.bitwise_and(hsv,hsv,mask=blue_closing)
    blue_dst = cv2.add(fg, bg)

    bg2 = cv2.bitwise_and(frame,frame,mask=pink_mask_inv)
    fg2 = cv2.bitwise_and(hsv,hsv,mask=pink_closing)
    pink_dst = cv2.add(fg2,bg2)


    # Draws the boxes around pink and/or blue contours if detected
    if len(list_of_good_blue_contours) != 0:
        draw_boxes_around_shapes(list_of_good_blue_contours, frame, 'blue')
        print("Number of blue contours detected:",len(list_of_good_blue_contours))
    else:
        print("No contours detected")
    
    if len(list_of_good_pink_contours) != 0:
        draw_boxes_around_shapes(list_of_good_pink_contours, frame, 'pink')
        print("Numer of pink contours detected", len(list_of_good_pink_contours))
    else:
        print("No contours detected")



    cv2.imshow('default', frame)
    
    # Kills the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
