import pyautogui
import ImageProcessing
import numpy as np
import Interface
from RoundButton import RoundButton
import tkinter as tk


class CursorScaling:

    # Constructeur de CursorScaling
    def __init__(self):
        # Donne le dernier vecteur position de l'oeil calculé
        self.lastPupilPosition = [0, 0]

        # Donne l'approximation calculée lors de l'échellonnage
        self.approximation = []

        # Liste des positions des points d'échelonnage sur l'écran
        self.buttonsLocations = [[0, 0], [0, 30], [0, 60]]

        # Liste des position de la pupille
        # enregistrés lors de l'échelonnage avec les positions des points cibles
        self.registeredApproximations = []

        # Booléan indiquant si l'on est en mode étalonnage ou non
        self.isScaling = False

    # Applique la position au curseur vis-à-vis du vecteur
    # déplacement de la pupille
    def setCursorPosition(self, vector):
        pyautogui.moveTo(vector[0], vector[1])

    # Constitue l'hypothèse de régression
    # sur l'écran étalonné les valeurs étalons
    # et optimisée
    # theta défini le vecteur de paramétrisation
    # x défini le vecteur d'entrer nouvelle
    def hypothesis(self, theta, x):
        # On définie le vecteur sortie supposé
        y = 0

        # On construit y = sum(theta_i*x_i)
        for i in range(0, len(x)):
            y = theta[i] * x[i]
        return y

    # Enregistre le point d'étalonnage en utilisation
    # la dernière position de la pupille
    def pointClickEvent(self):
        # On récupère les coordonnées du curseur
        mouseX, mouseY = pyautogui.position()

        # On récupère les coordonnées de la pupille
        [eyeX, eyeY] = ImageProcessing.getPupilPosition(ImageProcessing.getCameraView())
        print("Position de l'oeil : " + str(eyeX) + ", " + str(eyeY))
        # On enregistre la réalisation d'étalonnage en prévision de la régression
        self.registeredApproximations.append([mouseX, mouseY, eyeX, eyeY])

        # Condition définissant que tous les boutons ont été cliqués
        if len(self.registeredApproximations) == len(self.buttonsLocations):

            # Construction des matrice échantillon :
            # échantillons d'entrée : eyeX, eyeY
            X = []
            # échantillons de sortie : mouseX, mouseY
            YX = []
            YY = []
            for i in range(0, len(self.registeredApproximations)):
                X.append([1, self.registeredApproximations[i][2], self.registeredApproximations[i][3]])
                YX.append(self.registeredApproximations[i][0])
                YY.append(self.registeredApproximations[i][1])

            # Transformation matricielle puis transposition pour coller à la formule de l'équation normale
            X = np.array(X)
            X.transpose()
            YX = np.array(YX)
            YX.transpose()
            YY = np.array(YY)
            YY.transpose()

            # Détermination des paramètres optimales pour les régressions
            invertMatrix = np.invert(np.dot(X.transpose(), X))
            thetaX = np.dot(np.dot(invertMatrix, X.transpose()), YX)
            thetaY = np.dot(np.dot(invertMatrix, X.transpose()), YY)

            # Enregistrement des vecteurs optimisés
            self.approximation = [thetaX, thetaY]

            # Une fois les opérations effectuées, on affiche les boutons de contrôle :
            Interface.displayButtons(self)
            # On désactive le mode étalonnage
            self.isScaling = False

    # Liste les positions des boutons étalons et initialise buttonsLocations
    def setPosition(self, xmax, ymax):
        side_width = 3
        diam = 100
        ray = diam // 2
        xmilieu = xmax // 2
        ymilieu = ymax // 2
        self.buttonsLocations = [[0, 0], [0, ymilieu - ray], [0, ymax - diam], [xmilieu - ray, 0],
                                 [xmilieu - ray, ymilieu - ray],
                                 [xmilieu - ray, ymax - diam], [xmax - diam, 0], [xmax - diam, ymilieu - ray],
                                 [xmax - diam, ymax - diam]]

    # Affiche les points d'étalonnage à l'écran
    def displayCalibratingPoints(self):
        # Appel d'une fenêtre tk
        fenetre = tk.Tk()
        # Mode fullscreen
        fenetre.attributes('-fullscreen', True)
        # Echap permet de quitter l'interface
        fenetre.bind('<Escape>', lambda e: fenetre.destroy())
        # Récupération des informations de l'écran
        width = fenetre.winfo_screenwidth()
        height = fenetre.winfo_screenheight()
        # création de la fenêtre
        canvas = tk.Canvas(fenetre, width=width, height=height, bg='black')
        canvas.pack()
        # initialisation des positions des boutons étalons
        self.setPosition(width, height)
        # Placement des boutons
        for i in range(len(self.buttonsLocations)):
            button_i = RoundButton(fenetre, 100, 100, 50, 0, 'red', "black", command=self.pointClickEvent)
            button_i.place(x=self.buttonsLocations[i][0], y=self.buttonsLocations[i][1])
            # Ajout du bouton à la boucle tk
            button_i.pack

        # Lancement du scheduler tk
        fenetre.mainloop()
        # Destruction de la fenêtre
        fenetre.destroy()

    # Lance le mode étalonnage
    def launchCalibrating(self):
        # On montre au programme qu'il est en mode étalonnage
        self.isScaling = True
        # On reset les anciennes données de régression
        self.registeredApproximations.clear()
        # On affiche les boutons étalons
        self.displayCalibratingPoints()