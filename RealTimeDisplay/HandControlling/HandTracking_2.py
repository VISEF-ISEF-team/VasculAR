# Import the required modules
import cv2
import numpy as np
import pyautogui

# Define the hand gesture parameters
GESTURE_THRESHOLD = 10 # The minimum number of frames to recognize a gesture
GESTURE_HOLD = 5 # The number of frames to hold a gesture action
GESTURE_DRAG = 0 # The gesture code for drag action
GESTURE_CLICK = 2 # The gesture code for click action

# Define the colors for drawing
COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)

# Define the region of interest for hand detection
ROI_X = 100
ROI_Y = 100
ROI_WIDTH = 300
ROI_HEIGHT = 300

# Create a window to display the camera feed
cv2.namedWindow('Hand Gesture Mouse Control')

# Capture the camera feed
cap = cv2.VideoCapture(0)

# Initialize the background subtractor
back_sub = cv2.createBackgroundSubtractorMOG2()

# Initialize the gesture variables
gesture = None # The current gesture
gesture_count = 0 # The current gesture count
gesture_action = False # The current gesture action

# Main loop
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Extract the region of interest from the frame
    roi = frame[ROI_Y:ROI_Y+ROI_HEIGHT, ROI_X:ROI_X+ROI_WIDTH]

    # Apply the background subtractor to get the foreground mask
    mask = back_sub.apply(roi)

    # Apply some morphological operations to remove noise and fill holes
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, None)

    # Find the contours in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If there are no contours, skip the rest of the loop
    if len(contours) == 0:
        continue

    # Find the largest contour by area
    max_area = 0
    max_contour = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_contour = cnt

    # Draw the convex hull around the largest contour
    hull = cv2.convexHull(max_contour)
    cv2.drawContours(roi, [hull], -1, COLOR_GREEN, 2)

    # Find the convexity defects in the largest contour
    hull_indices = cv2.convexHull(max_contour, returnPoints=False)
    defects = cv2.convexityDefects(max_contour, hull_indices)

    # Count the number of fingers by counting the number of defects plus one
    fingers = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(max_contour[s][0])
        end = tuple(max_contour[e][0])
        far = tuple(max_contour[f][0])
        angle = np.arctan2(start[1] - far[1], start[0] - far[0]) - np.arctan2(end[1] - far[1], end[0] - far[0])
        if angle < np.pi / 2:
            fingers += 1
            cv2.circle(roi, far, 4, COLOR_RED, -1)
    
    fingers += 1

    # Display the number of fingers on the frame
    cv2.putText(frame, 'Fingers: {}'.format(fingers), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, COLOR_BLUE, 3)

    # Update the gesture variables based on the number of fingers
    if gesture == fingers:
        gesture_count += 1
        if gesture_count >= GESTURE_THRESHOLD:
            gesture_action = True 
            if gesture == GESTURE_DRAG:
                pyautogui.mouseDown()
            elif gesture == GESTURE_CLICK:
                pyautogui.click()
            else:
                pyautogui.mouseUp()
            gesture_count -= GESTURE_HOLD 
    else:
        gesture_action = False 
        pyautogui.mouseUp()
        gesture_count = 0
    
    gesture = fingers

    # Get the centroid of the largest contour
    moments = cv2.moments(max_contour)
    cx = int(moments['m10'] / moments['m00'])
    cy = int(moments['m01'] / moments['m00'])

    # Draw a circle at the centroid
    cv2.circle(roi, (cx, cy), 4, COLOR_BLUE, -1)

    # Map the centroid coordinates to the screen coordinates
    screen_x = np.interp(cx, [0, ROI_WIDTH], [0, pyautogui.size()[0]])
    screen_y = np.interp(cy, [0, ROI_HEIGHT], [0, pyautogui.size()[1]])

    # Move the mouse pointer to the screen coordinates
    pyautogui.moveTo(screen_x, screen_y)

    # Draw a rectangle around the region of interest
    cv2.rectangle(frame, (ROI_X, ROI_Y), (ROI_X+ROI_WIDTH, ROI_Y+ROI_HEIGHT), COLOR_BLUE, 2)

    # Display the frame
    cv2.imshow('Hand Gesture Mouse Control', frame)

    # Exit if the user presses ESC
    key = cv2.waitKey(10) & 0xFF
    if key == 27:
        break

# Release the camera and destroy the windows
cap.release()
cv2.destroyAllWindows()
