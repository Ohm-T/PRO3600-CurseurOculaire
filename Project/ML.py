import matplotlib.pyplot as mp
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Source en partie : https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
import pyautogui


def solve(eyeX_, eyeY_, mouseX_, mouseY_):
    # Construction des matrice échantillon :
    # échantillons d'entrée : eyeX, eyeY
    XX = []
    XY = []
    # échantillons de sortie : mouseX, mouseY
    YX = []
    YY = []
    for i in range(0, len(eyeX_)):
        XX.append([1, eyeX_[i]])
        XY.append([1, eyeY_[i]])
        YX.append(mouseX_[i])
        YY.append(mouseY_[i])

    # Transformation matricielle puis transposition pour coller à la formule de l'équation normale
    XX = np.array(XX)

    XY = np.array(XY)

    YX = np.array(YX)
    YY = np.array(YY)

    print("XX : \n", XX)
    print("\nYX : \n", YX)

    # Détermination des paramètres optimales pour les régressions
    invertMatrixX = np.linalg.inv( (XX.transpose()).dot(XX) )
    invertMatrixY = np.linalg.inv( (XY.transpose()).dot(XY) )

    thetaX_ = np.matmul(invertMatrixX, ((XX.transpose()).dot(YX)))
    thetaY_ = np.matmul(invertMatrixY, ((XY.transpose()).dot(YY)))

    # Enregistrement des vecteurs optimisés
    return thetaX_, thetaY_


print("running")
vecEyeX = []
vecEyeY = []
vecCurX = []
vecCurY = []
simpleVecEyeX = []
simpleVecEyeY = []

cEyeX = 0
cEyeY = 0

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    img = frame
    img_eye = None
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        img = cv2.circle(img, (int(x + w / 2), int(y + h / 2)), min(int(w / 2), int(h / 2)), (255, 90, 200), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            if ex < w / 2 - 50 and ey < h / 2 + 50:
                img_eye = roi_gray[ey:ey + eh, ex:ex + ew]
                roi_eye = roi_color[ey:ey + eh, ex:ex + ew]
                # cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                cv2.circle(roi_color, (int(ex + ew / 2), int(ey + eh / 2)), min(int(ew / 2), int(eh / 2)),
                           (250, 150, 110), 2)
                cEyeX = int(ex + ew / 2)
                cEyeY = int(ey + eh / 2)

    if img_eye is not None:

        circles = cv2.HoughCircles(img_eye, cv2.HOUGH_GRADIENT, 1.2, 100)

        # if circles is not None:
        #    # convert the (x, y) coordinates and radius of the circles to integers
        #    circles = np.round(circles[0, :]).astype("int")
        #    # loop over the (x, y) coordinates and radius of the circles
        #    for (x, y, r) in circles:
        #        # draw the circle in the output image, then draw a rectangle
        #        # corresponding to the center of the circle
        #        print("cirlce")
        #        cv2.circle(roi_eye, (x, y), r, (0, 255, 0), 4)
        #        rows, cols = img_eye.shape
        #        cv2.line(roi_eye, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
        #        cv2.line(roi_eye, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
        #        cv2.rectangle(roi_eye, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        # show the output image
        rows, cols = img_eye.shape
        gray_roi = cv2.GaussianBlur(img_eye, (7, 7), 0)
        _, threshold = cv2.threshold(gray_roi,90, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow("thresh", threshold)
        contours,hier = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            # cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
            # cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.circle(roi_eye, (x + int(w / 2), y + int(h / 2)), int(w / 2), (255, 0, 0), 2)
            cv2.line(roi_eye, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
            cv2.line(roi_eye, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)

            mouseX, mouseY = pyautogui.position()
            eyeX, eyeY = x + int(w / 2), y + int(h / 2)

            if eyeX == 0 or eyeY == 0:
                break
            print(eyeX, mouseX, eyeY, mouseY)

            simpleVecEyeX.append(eyeX)
            simpleVecEyeY.append(eyeY)
            vecEyeX.append([eyeX, eyeX**2])
            vecEyeY.append([eyeY, eyeY**2])
            vecCurX.append(mouseX)
            vecCurY.append(mouseY)

            break

        cv2.imshow("Eye", roi_eye)
    # Display the resulting frame
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):

        fig, axs = plt.subplots(2, 2)
        axs[0, 0].plot(simpleVecEyeX, vecCurX, 'ro')
        axs[0, 0].set_title('mouseX / EyeX')
        axs[0, 1].plot(simpleVecEyeY, vecCurY, 'bo')
        axs[0, 1].set_title('mouseY / EyeY')

        axs[1, 0].plot(simpleVecEyeX, vecCurX, 'ro')
        axs[1, 1].plot(simpleVecEyeY, vecCurY, 'bo')

        minX = simpleVecEyeX[0]
        maxX = simpleVecEyeX[0]
        for i in simpleVecEyeX:
            if minX > i:
                minX = i
            if maxX < i:
                maxX = i
        x = np.linspace(minX, maxX, 400)

        modelX = LinearRegression().fit(np.array(simpleVecEyeX).reshape(-1, 1), np.array(vecCurX))
        modelY = LinearRegression().fit(np.array(simpleVecEyeY).reshape(-1, 1), np.array(vecCurY))
        print("modelX I: ", modelX.intercept_, "\nmodelX S: ", modelX.coef_[0])

        y1 = modelX.intercept_ + modelX.coef_[0] * x
        y2 = modelY.intercept_ + modelY.coef_[0] * x

        thetaX, thetaY = solve(simpleVecEyeX, simpleVecEyeY, vecCurX, vecCurY)
        print("thetaX : \n", thetaX, "\nthetaY : ", thetaY)

        By1 = thetaX[0] + thetaX[1]*x
        By2 = thetaY[0] + thetaY[1]*x

        axs[0, 0].plot(x, y1)
        axs[0, 1].plot(x, y2)
        axs[0, 0].plot(x, By1)
        axs[0, 1].plot(x, By2)

        plt.show()
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
