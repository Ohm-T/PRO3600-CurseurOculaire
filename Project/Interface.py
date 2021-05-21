import tkinter as tk
from RoundButton import *

# Effectue les actions liées au bouton
def buttonClickEvent():
    return


# Affiche les boutons utilisateurs (exit & étalonnage)
def displayButtons(cs):
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
    etan = tk.Button(fenetre, text='étannolage', command=cs.displayCalibratingPoints)
    etan.pack()
    quit = tk.Button(fenetre, text='quitter', command=fenetre.quit)
    quit.pack()
    fenetre.mainloop()
    fenetre.destroy()
    return