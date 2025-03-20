import cv2
import numpy as np

camera_stream = cv2.VideoCapture(0)

averager = []
average = 0
capacity = 5

font = cv2.FONT_HERSHEY_SIMPLEX
org = (70, 70)
fontScale = 1
color = (0, 0, 255)
thickness = 2

while True:
    image = cv2.flip(camera_stream.read()[1], 1)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    gray_blurred = cv2.blur(gray, (3, 3))  
    detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, 1, 20, param1 = 52,
                                        param2 = 28, minRadius = 1, maxRadius = 30)
    
    if detected_circles is not None:
        d = detected_circles[0]
        circle_count = detected_circles[0]
        d = np.uint16(np.around(detected_circles))
            
        for pt in d[0, :]: 
            a, b, r = pt[0], pt[1], pt[2]
            for gol in range(r):
                cv2.circle(image, (a, b), gol, (0, 0, 255), 3)
        if average > 6:
            average = 0
            averager.clear()
        if len(averager) < capacity:
            averager.append(len(circle_count))
        elif len(averager) >= capacity:
            average = 0
            for iii in range(len(averager)):
                average += averager[iii]
            average /= len(averager)
            average = round(average)
            averager.clear()
            
        cv2.putText(image, str(average), org, font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.rectangle(image, (60, 40), (100, 80), color, thickness)
        cv2.imshow("Detected Circle", image)
        
    else:
        image = cv2.putText(image, '-', (68, 69), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
        cv2.rectangle(image, (60, 40), (100, 80), color, thickness)
        cv2.imshow("Detected Circle", image)
        
    cv2.waitKey(1)
    
