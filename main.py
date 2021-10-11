import cv2
import mediapipe as mp 
import numpy as np 
import HandTrackingModule as htm 
import time 
import pyautogui as pag
pag.FAILSAFE = False


#################
w, h = 640, 480
frameReduction = 100
smoothening = 7
#################

ptime = 0
plocX, plocY = 0, 0 #previous location of x, y
clocX, clocY = 0, 0 #curr location of x , y 


cap = cv2.VideoCapture(0)
cap.set(3, w)
cap.set(4, h)
detector = htm.handDetector(max_hands= 1)
while True:
    #1. Find hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lm , bbox= detector.findPosition(img)
    #2. Get the tip of index and middle finger 
    if len(lm) != 0:
        x1, y1  = lm[8][1:]
        x2, y2 = lm[12][1:]
        # print(x1, y1, x2, y2)
    #3. Check which finger is up 
        fingers = detector.fingersUp()
        print(fingers)
        cv2.rectangle(img, (frameReduction, frameReduction), (w - frameReduction, h - frameReduction), (255, 0, 0), 2 )

    #4. Only Index Finger : Moving Mode 
        if fingers[1] == 1 and fingers[2] == 0:

    #5. Convert coordinates 
            x3 = np.interp(x1, (frameReduction, w- frameReduction), (0,1366.0))
            y3 = np.interp(y1, (frameReduction, h - frameReduction), (0,768.0))
            
    #6. Smoothen Values 
            clocX = plocX +(x3 - plocX) / smoothening
            clocY = plocY +(y3 - plocY) / smoothening
            

    #7. Move mouse 
            pag.moveTo(1366.0 - clocX,clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0 , 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

    #8. Both Index and middle fingers are UP: Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            #9. Find the distance between fingers
            length, img, lineinfo = detector.findDistance(8, 12, img)
            print(length)
            #10. Click mouse if distance short 
            if length < 40:
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, ( 0 ,255, 0), cv2.FILLED)
                pag.leftClick()


    
    
    #11. Frame Rate 
    ctime = time.time()
    fps = 1/ (ctime - ptime)
    ptime = ctime 
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0, 0), 3)
    #12. Display
    cv2.imshow('Virtual-mouse', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


