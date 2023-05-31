import random
def main(taille=9):
    """
    Fonction principale du programme avec la logique d'exécution'
    """
    # Defini la taille avec colonne et ligne
    ligne = [val for val in range(1,taille)]
    colonne = [val for val in range(65, 65 + taille)]
    
    # Initialiser la grille
    grille = grille(taille)
    grille = statutCaseDepart(grille,taille)
    nbr_case_normale = compteNombreMine(grille)
    case_statut = ""
    jeu_statut = True
    
    while jeu_statut:
        # Affiche à chaque fois la grille
        afficher(grille)
        
        # Demande les coords
        saisieUser = saisie((colonne,ligne))
        # Analyse les coords
        case_statut = recupererCaseStatut(saisieUser)
        # On définit l'etat de victoire ou pas
        jeu_statut = regle(case_statut, grille)
    
    print("Fin du jeu, merci de votre participation !!!")
        
        
    
    
def grille(taille:int):
    """
    Fonction Principale :
        Créer un dictionnaire de cette forme
            { (x,y) : {"type" : "mine/speciale/normale", "drapeau" : True/False, "estVisible" : True/False}, etc...}

    Parameters
    ----------
    taille : int
        taille de la liste.

    Returns 
    -------
    un dictionnaire

    """
    dico = {}

    for x in range(1,taille+1):
        for y in range(1,taille+1):
            dico.update(
                {
                    (x,y) : {"type" : "None", "drapeau" : False, "estVisible" : False}
                })
    
    return dico


def statutCaseDepart(grille:dict):
    """
    Fonction Principale :
        Modifier l'attribut type avec des valeurs telle que mine/speciale/normale
        Avec des nombres de mine,speciales,normale proportionnelle à la taille.
        
        - Probabilité mine : 40 %
        - Probabilité speciale : 10%
        - Probabilité normale 50 % (le reste)

    Parameters
    -------
    nouvelle grille avec le type modifier.

    """
    random.seed() # Générer des nombres de façons aléatoire à CHAQUE fois, pour avoir une structure de donnée unique à chaque fois.
    taille = len(grille)
    # Pour le 0.1, aller voir l'explication fonction test_statutCaseDepart
    nbr_mine = round(0.40 * taille + 0.1)
    nbr_speciale = round(0.10 * taille + 0.1)
    nbr_normale = round(0.50 * taille + 0.1)
    liste_Choix = ["mine","normale","speciale"]

    for key in grille.keys():
        isModified = False
        while not(isModified):
            if len(liste_Choix) > 0:
                randomChoice = random.choice(liste_Choix)
                if randomChoice == "mine" and nbr_mine > 0:
                    grille[key]["type"] = randomChoice
                    nbr_mine -= 1
                    isModified = True
                elif randomChoice == "normale" and nbr_normale > 0:
                    grille[key]["type"] = randomChoice
                    nbr_normale -= 1
                    isModified = True
                elif randomChoice == "speciale" and nbr_speciale > 0:
                    grille[key]["type"] = randomChoice
                    nbr_speciale -= 1
                    isModified = True
            else:
                isModified = True
        
        if nbr_mine == 0 and "mine" in liste_Choix:
            liste_Choix.remove("mine")
        elif nbr_normale == 0 and "normale" in liste_Choix:
            liste_Choix.remove("normale")
        elif nbr_speciale == 0 and "speciale" in liste_Choix:
            liste_Choix.remove("speciale")            

    return grille


def recupererCaseStatut(coords:tuple,grille:dict):
    """
    Fonction qui renvoye le type de la case en char:
        - Case Normale : normale
        - Case Spéciale : speciale
        - Case Mine : mine
    """
    return grille[coords]["estVisible"]

def drapeau(coords:tuple,grille:dict,isFind:bool):
    """
    Fonction Principale :
        Changer le statut 'drapeau' : False à True du dico avec les coords x et y 

    Parameters
    ----------
    coords : tuple
       x,y
    grille : dict
        la grille 
    isFind : bool
        vrai ou faux (visible ou pas)


    Returns 
    -------
    rien car modifie directe

    """
    grille[coords]["drapeau"] = isFind

def afficher():
    pass

def mineAdjacente():
    pass

def decouvrirZone(boolean:bool,grille:dict,coords:tuple):
    grille[coords]["estVisible"] = boolean

def compteNombreMine(grille,dict):
    pass

def saisie(taille:tuple):
    pass

def regle(case_statut:str,grille:dict):
    """
    Fonction qui selon le type de la case va exécuter les fonctions attribuée aux regles et va renvoyer un etat boolean
    """
    
    if case_statut == 'normale':
        decouvrirZone(mode=case_statut)
        return True
    elif case_statut == 'speciale':
        print("Evenement aléatoire !!!")
        decouvrirZone(mode=case_statut)
        actionAleatoire()
        return True
    elif case_statut == 'mine':
        print("BOOM")
        return False
        

def actionAleatoire():
    pass

def ajouterMine():
    pass

def cacherZone():
    pass

def changeMine():
    pass

def LigneMontrer(taille,grille:dict,y): # Ligne x
    """
     Fonction Principale :
        fonction qui MODIFIE une ligne en la rendant visibile (Modifier l'attribut des cases != afficher la grille) selon la position de la case evenement (je rapelle que c'est un événement pas une fonction pour afficher; juste modifier le dico selon les coordonnées.)

    :param grille: taille,grille:dict,x,y
    :return: grille
    """
    for x in range(1,len(taille)+1): # parcours la ligne
                grille[(x,y)]["estVisible"] = True  # modifie le paramètre pour que le statue de la case soit visible
    return grille # renvoye la grille

def ColonneMontrer(taille,grille:dict,x): # Colonne y
    """
     Fonction Principale :
        fonction qui MODIFIE une colonne en la rendant visibile 

    :param grille: taille,grille:dict,x,y
    :return: grille
    """
    for y in range(1,len(taille)+1): # parcours la ligne
                grille[(x,y)]["estVisible"] = True  # modifie le paramètre pour que le statue de la case soit visible
    return grille # renvoye la grille

# TEST

def manage_assert(grille):
    """
    FP : Regroupe les fonction test avec des assert
    But: Permet d'activer ou désactiver les asserts sans tout changer
    """
    assert test_statutCaseDepart(grille=grille) == True
    drapeau((9,9),grille=grille, isFind=True)
    assert  test_drapeau((9,9),grille=grille, isFind=True)

def test_statutCaseDepart(grille:dict):
    """
    Fonction Principale :
        Vérifier le bon comportement de la fcontion statutCaseDepart

    Parameters
    ----------
    grille : dict
        le dictionnaire de la liste


    Returns 
    -------
    une valeur boolean pour le assert

    """
    taille = len(grille)
    mine,spe,normal = 0,0,0
    for valeur in grille.values():
        if valeur["type"] == "mine":
            mine += 1
        elif valeur["type"] == "speciale":
            spe += 1
        elif valeur["type"] == "normale":
            normal += 1
    """
    Remarque : Dans les propabilités des cases, j'ai remarqué un problème dû à l'arrondissement des nombres pour les mettre dans le random qui supporte que des integer (pas des float donc on arrondie)
    Par exemple:
        - taille = 81
        nbr_mine = round(0.40 * taille) --> 32 (sans arrondir : 32.4)
        nbr_speciale = round(0.10 * taille) --> 8 (sans arrondir : 8.1)
        nbr_normale = round(0.50 * taille) --> 40 (sans arrondir : 40.5)

        donc 32 + 8 + 40 sa fait 80 et non 81.
    
    Solution: J'ai rajouté 0.1 ce qui va permettre de choisir celui qui aura la case en plus donc: 
    Exemple:
        nbr_normale = round(0.40 * taille + 0.1) --> (40.5 +0.1 = 40.6 soit arrondie = 41)
    """
    
    nbr_mine = round(0.40 * taille + 0.1)
    nbr_speciale = round(0.10 * taille + 0.1)
    nbr_normale = round(0.50 * taille + 0.1)
    
    if nbr_mine == mine and nbr_normale == normal and nbr_speciale == spe: # Vérifier les proba, si il manque pas des mines par ex 
        return True
    else:
        return False

def test_drapeau(coords:tuple,grille:dict,isFind:bool):
    """
    Fonction Principale :
        Vérifie le changement du statut 'drapeau' : False à True du dico avec les coords x et y 

    Parameters
    ----------
    coords : tuple
       x,y
    grille : dict
        la grille 
    isFind : bool
        vrai ou faux (visible ou pas)


    Returns 
    -------
    rien car modifie directe

    """
    if grille[coords]["drapeau"] == isFind:
        return True
    else:
        return False
