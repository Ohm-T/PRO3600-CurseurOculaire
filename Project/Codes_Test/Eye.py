import numpy as np
import cv2
import autopy


print("running")
vecEyeX = []
vecEyeY = []

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# données écran
Screen_w,Screen_h=autopy.screen.size()
smooth=10
X,Y=0,0
smoothX,smoothY=0,0
marge_x=15
marge_y=20

cap = cv2.VideoCapture(0)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret is False:
        break

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    img = frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        img = cv2.circle(img, (int(x + w / 2), int(y + h / 2)), min(int(w / 2), int(h / 2)), (0,0,200), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            if ex < w / 2 - 50 and ey < h / 2 + 50:
                width_eye=ex
                height_eye=ey
                gray_eye = roi_gray[ey:ey + eh -5, ex:ex + ew-5]
                roi_eye = roi_color[ey:ey + eh, ex:ex + ew]


        rows, cols = gray_eye.shape
        gray_roi = cv2.GaussianBlur(gray_eye, (7, 7), 0)
        _, threshold = cv2.threshold(gray_roi,80, 255, cv2.THRESH_BINARY_INV)
        contours,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            # cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
            cv2.circle(roi_eye, (x + int(w / 2), y + int(h / 2)), int(w / 2), (255, 0, 0), 2)
            cv2.line(roi_eye, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
            cv2.line(roi_eye, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)

            eyeX, eyeY = x + int(w / 2), y + int(h / 2)


            if eyeX == 0 or eyeY == 0:
                break
            print(eyeX,eyeY)
            # print(marge_x,marge_y,width_eye-marge_x,height_eye-marge_y)
            vecEyeX.append(eyeX)
            vecEyeY.append(eyeY)

            #Mouse
            cv2.rectangle(roi_eye,(marge_x,marge_y),(width_eye-marge_x,height_eye-marge_y),(255,0,0),1)
            x = np.interp(eyeX, (marge_x, width_eye-marge_x), (0, Screen_w))
            y = np.interp(eyeY, (marge_y, height_eye-marge_y), (0, Screen_h))

            #Smooth the mouse
            smoothX=X+(x-X)/smooth
            smoothY=Y+(y-Y)/smooth
            X, Y = smoothX, smoothY
            autopy.mouse.move(Screen_w - X, Y)





            break

    cv2.imshow('img', img)
    cv2.imshow("Eye", roi_eye)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()