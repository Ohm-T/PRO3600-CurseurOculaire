import sched
import time

from CursorScaling import CursorScaling
import ImageProcessing

# Lancement de l'étalonnage au démarrage du programme
scaler = CursorScaling()
scaler.launchCalibrating()


# Définition de la fonction de gestion du curseur
def running():
    # Condition de mise à jour de la position du curseur
    if not scaler.isScaling:
        # On récupère la position de l'oeil
        [eyeX, eyeY] = ImageProcessing.getPupilPosition(ImageProcessing.getCameraView())
        # On en déduit la position prévue du curseur Les index 0,1 références thetaX et thetaY optimisant l'hypothèse
        # de régression et ont été calculés lors de l'étalonnage
        pos = [scaler.hypothesis(scaler.approximation[0], eyeX), scaler.hypothesis(scaler.approximation[1], eyeY)]
        # On déplace le curseur à cette position
        scaler.setCursorPosition(pos)
        # On enregistre le dernier vecteur position de la pupille
        scaler.lastPupilPosition[0], scaler.lastPupilPosition[1] = pos[0], pos[1]


# Création de la boucle scheduler
s = sched.scheduler(time.monotonic, running)
# Lancement du scheduler
s.run()