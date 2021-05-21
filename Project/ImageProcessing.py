import cv2
import numpy as np


# Renvoie le vecteur déplacement de la pupille entre 2 images
def getPupilVector(lastPos, currentPos):
    return [lastPos[0] - currentPos[0], lastPos[1] - currentPos[1]]


# Renvoie la position de la pupille par rapport à la glande lacrimale
def getPupilPosition(image):
    # Extraction de l'imagette de l'oeil supérieur droit détecté
    eye_color = extractEyesPicture(image)
    # Condition de détection
    if eye_color is None:
        print("Eye_color is None")
        return [0, 0]

    # Passage en noir et blanc pour la réduction d'information et une meilleure détection
    gray = cv2.cvtColor(eye_color, cv2.COLOR_BGR2GRAY)

    ## Détection de cercle dans l'imagette de l'oeil par la méthode de Hough
    #circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

    # Condition de détection d'un cercle
    #if circles is None:
    #    print("No hough circles detected")
    #    showImage(gray, "error")
    #    return [0, 0]

    # Récupération de la taille de l'image
    rows, cols = gray.shape
    # Application d'un flou gaussien
    gray_blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    # Seuillage
    _, threshold = cv2.threshold(gray_blurred, 80, 255, cv2.THRESH_BINARY_INV)
    # Recherche des contours de l'oeil
    contours = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Conditions de détection de l'oeil
    if contours is None:
        print("No eye contour detected")
        return [0, 0]
    if len(contours) == 0:
        print("No eye contour detected")
        return [0, 0]

    # Récupération des coordonnées de la pupille
    (x, y, w, h) = cv2.boundingRect(contours[0])

    return [x + int(w / 2), y + int(h / 2)]


# Extrait une imagette de l'oeil supérieur droit
def extractEyesPicture(image):
    # Méthode des ondelettes de Haar pour la détection des yeux
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Définiton de l'image du visage en couleur
    roi_color, w, h = extractFacesPicture(image);
    # Condition de détection du visage
    if roi_color is None:
        print("roi_color is None")
        return None
    # Passage en noir et blanc pour la réduction d'information et une meilleure détection
    gray = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY)
    # Détection des yeux
    eyes = eye_cascade.detectMultiScale(gray)

    # Définition de l'image extraite
    extracted = None
    # Bouclage sur les yeux détectés
    for (ex, ey, ew, eh) in eyes:
        # Condition de détection de l'oeil supérieur droit
        if ex < w / 2 - 50 and ey < h / 2 + 50:
            extracted = roi_color[ey:ey + eh, ex:ex + ew]

    return extracted


# Extrait une image englobant le visage de l'utilisateur
def extractFacesPicture(image):
    # Méthode des ondelettes de Haar pour la détection de visage
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Passage en noir et blanc pour la réduction d'information et une meilleure détection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Détection des visages
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # Conditions de détection du visage
    if faces is None:
        print("No face detected")
        return None, None, None
    if len(faces) == 0:
        print("No face detected")
        return None, None, None
    # Extraction des données sur l'image du premier visage détecté
    (x, y, w, h) = faces[0]
    # Extraction du 1er visage détecté sur l'image en couleur
    extracted = image[y:y + h, x:x + w]
    return extracted, w, h


# Renvoie une image cv2 de la caméra
def getCameraView(cameraSlot=0):
    cap = cv2.VideoCapture(cameraSlot, cv2.CAP_DSHOW)
    _, frame = cap.read()
    return frame


# Permet d'afficher à l'écran une image (utile pour le debug)
def showImage(image, imageName="noName"):
    cv2.imshow(imageName, image)