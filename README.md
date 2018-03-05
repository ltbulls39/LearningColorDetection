# LearningColorDetection
## First Project: **Detecting colors and putting boxes around them**
##### Recognizing various colors, first up: blue.
### Step 1: Import necessary libraries
    import cv2
    import numpy as np
### Step 2: Set-up camera for video feed (You can use cv2.imread() for images if you prefer)
    cap = cv2.VideoCapture(1)
    while True:
        _, frame = cap.read()
        
        cv2.imshow('Default', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

