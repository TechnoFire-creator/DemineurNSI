import random
import math

    
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
                    (x,y) : {"type" : "None", "drapeau" : False, "estVisible" : False, "nbr_mine" : 0}
                })
    
    return dico


def statutCaseDepart(grille:dict):
    """
    Fonction Principale :
        Modifier l'attribut type avec des valeurs telle que mine/speciale/normale
        Avec des nombres de mine,speciales,normale proportionnelle à la taille.
        
        - Probabilité mine : 40%
        - Probabilité speciale : 5%
        - Probabilité normale 50% (le reste)

        Puis mettre les MineAdjacentes
    Parameters
    -------
    nouvelle grille avec le type modifier.

    """
    random.seed() # Générer des nombres de façons aléatoire à CHAQUE fois, pour avoir une structure de donnée unique à chaque fois.
    taille = len(grille)
    # Pour le 0.1, aller voir l'explication fonction test_statutCaseDepart
    nbr_mine = round(0.45 * taille + 0.1)
    nbr_speciale = round(0.05 * taille + 0.1)
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
    return (grille[coords]["type"],grille[coords]["estVisible"])

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

def afficher(grille:dict,taille):
    """Fonction Principale :
        Fonction qui affiche les données de la grille selon le type de case etc...
        
        :param grille:dict
        :return grille
    """
    abscisse = "    " + "".join( str(val)+" " for val in range(1,taille+1))
    print(abscisse)
    print("    " + "- "*(taille))
    for x in range(1,taille+1):
        print(str(x) + " | ",end="")
        for y in range(1,taille+1):
            case = grille[(x,y)]
            if case["drapeau"] == False:
                if case["estVisible"]:
                    print(case["nbr_mine"], end="")
                else:
                    print(" ", end="")
            else:
                print("?",end="")
            
            print(" ",end="")
        print("")

def MineAdjacente(grille:dict,coords):
    """Fonction Principale :
        fonction qui indique le nombre de mine adjacente
        
        :param grille(dict),taille
        :return  nbrMineAdjacent
    """
    nbr_mine = 0
    x = coords[0]
    y = coords[1]
    
    liste_case_within = [(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1),(x-1,y-1)]
    
    for coord in liste_case_within:
        if grille.get(coord, "-1") != "-1" and grille[coord]["type"] == "mine":
            nbr_mine += 1
    
    return nbr_mine


def decouvrirZone(boolean:bool,grille:dict,coords:tuple):
    grille[coords]["estVisible"] = boolean


def saisie(taille:int):
    """
    FP : fonction qui récpére les données de l'utilisateur et la vérifie
    
    parametre;
        -taille : int

    Returns
    -------
    tuple(x,y)

    """
    
    drapeau = -1
    case = ()
    
    isCheck = True
    while isCheck:
        commands = input("demineur :  ")
        if commands[0]=="c" and len(commands) == 3:
            if 48 <=  ord(commands[1]) <= ord(str(taille))and 48 <=  ord(commands[2]) <= ord(str(taille)):
                case = (int(commands[2]),int(commands[1]))
        elif commands[0]=="d" and len(commands) == 3:
            if 48 <=  ord(commands[1]) <= ord(str(taille))and 48 <=  ord(commands[2]) <= ord(str(taille)):
                drapeau = (int(commands[2]),int(commands[1]))
        elif commands[0]=="e" and len(commands) == 1:
            isCheck = False
        else:
            print("Erreur de syntaxe \nExemple : \nc11 pour creuser une case en x=1 et y=1 \nd11 pour poser un drapeau en x=1 et y=1\ne : exit")
        
    return {"case":case,"drapeau":drapeau}

def regle(case_statut:tuple,grille:dict, case_decouverte:int,coords:tuple,drapeauSaisie,taille:int):
    """
    Fonction qui selon le type de la case va exécuter les fonctions attribuée aux regles et va renvoyer un etat boolean
    """
    
    if drapeauSaisie != -1:
        drapeau(drapeauSaisie, grille, True)
        if len(case_statut) != 0:
            if case_statut[1] == True and case_statut[0] != "mine":
                print("Erreur, déjà visible")
                return(True, case_decouverte)
            elif case_statut[0] == 'normale':
                casseAllie(grille, taille, coords)
                return (True, case_decouverte+1)
            elif case_statut[0] == 'speciale':
                print("Evenement aléatoire !!!")
                casseAllie(grille, taille, coords)
                actionAleatoire(coords,taille,grille)
                return (True, case_decouverte+1)
            elif case_statut[0] == 'mine':
                print("BOOM")
                return (False,case_decouverte)
        else:
            return (True, case_decouverte)
    else:
        if len(case_statut) != 0:
            if case_statut[1] == True and case_statut[0] != "mine":
                print("Erreur, déjà visible")
                return(True, case_decouverte)
            if case_statut[0] == 'normale':
                casseAllie(grille, taille, coords)
                return (True, case_decouverte+1)
            elif case_statut[0] == 'speciale':
                print("Evenement aléatoire !!!")
                casseAllie(grille, taille, coords)
                actionAleatoire(coords,taille,grille)
                return (True, case_decouverte+1)
            elif case_statut[0] == 'mine':
                print("----[BOOM]----")
                return (False,case_decouverte,grille)
        else:
            return (True, case_decouverte)

def actionAleatoire(coords:tuple,taille:int,grille:dict):
    """
    FP: Choisir de façons aléatoire et équitable (1/5) de tomber sur l'un des 5 événement/actions customiser.

    Parameters
    ----------
    coords : tuple
        DESCRIPTION.

    Returns
    -------
    None.

    """
    x = coords[0]
    y = coords[1]
    nombreAle = random.randint(1,5)
    if nombreAle == 1:
        fatality(grille,taille)
        print("Retours à la case departs !")
    if nombreAle == 2:
        cacherZone(coords,grille)
        print("Zone cachée !")
    if nombreAle == 3:
        montrerColonne(taille,grille,y)
        print("Colonne découverte !")
    if nombreAle == 4:
        montrerLigne(taille,grille,x)
        print("Ligne Découverte")
    if nombreAle == 5:
        montrerDiagonal(taille,grille)
        print("Diagonal Découverte")
    
        
        
        
def montrerDiagonal(taille:int,grille:dict):
    """
    FP: fonction qui montre les cases des diagonales

    Returns
    -------
    None.

    """
    x = 1
    y = 1
    for _ in range(0,taille): # parcours la diagonale droite
        grille[(x,y)]["estVisible"] = True
        x += 1
        y += 1
    
    x = taille
    y = 1
    for _ in range(0,taille): # parcours la diagonale gauche
        grille[(x,y)]["estVisible"] = True
        x -= 1
        y += 1
    
def cacherZone(coords:tuple,grille:dict):
    """
    FP : cache les cases aux alentours 
    
    :params:
        - coords:tuple
        - grille:dict
    
    return None
    """
    x = coords[0]
    y = coords[1]
    liste_case_within = [(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x,y)]
    for coord in liste_case_within:
        if grille.get(coord, "-1") != "-1":
            grille[coord]["estVisible"] = False
        
def fatality(demineur:dict,taille:int):
    """
    Fonction Principale : fonction qui changes toute

    :param grille,coords
    :return grille
    """
    demineur.clear()
    demineur.update(grille(taille))
    demineur = statutCaseDepart(demineur)  #redéfinit le statut des cases
    demineur = mineAdjacenteDepart(demineur,taille)   #appelle la fonction pour mettre à jour les cases adjacente 

def montrerColonne(taille,grille:dict,y): # Ligne x
    """
     Fonction Principale :
        fonction qui MODIFIE une ligne en la rendant visibile (Modifier l'attribut des cases != afficher la grille) selon la position de la case evenement (je rapelle que c'est un événement pas une fonction pour afficher; juste modifier le dico selon les coordonnées.)

    :param grille: taille,grille:dict,x,y
    :return:
    """
    for x in range(1,taille+1): # parcours la ligne
        grille[(x,y)]["estVisible"] = True  # modifie le paramètre pour que le statue de la case soit visible

def montrerLigne(taille,grille:dict,x): # Colonne y
    """
     Fonction Principale :
        fonction qui MODIFIE une colonne en la rendant visibile 

    :param grille: taille,grille:dict,x,y
    :return: grille
    """
    for y in range(1,taille+1): # parcours la ligne
        grille[(x,y)]["estVisible"] = True  # modifie le paramètre pour que le statue de la case soit visible

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

def mineAdjacenteDepart(grille:dict,taille:int):
    """
    FP : Générer toutes les stats sur nbr_mine pour toutes les mines

    param:
    -grille:dict
    -taille:int

    return: grille
    """
    for x in range(1,taille+1):
        for y in range(1,taille+1):
            if grille[(x,y)]["type"] != "mine":
                grille[(x,y)]["nbr_mine"] = MineAdjacente(grille,coords=(x,y))        
            else:
                grille[(x,y)]["nbr_mine"] = "M"
    return grille

def casseAllie(grille:dict,taille:int,coords:tuple):
    """
    FP : Si la case où l'on a creusé ne contient aucune mine dans son voisinage (une case nbr_mine = 0), 
    alors le jeu creuse automatiquement sur toutes les cases autour d'elle, ce qui permet de dégager les grands espaces (toute les cases autours) libres d'un seul coup. Plus facile pour le joueur
    

    Parameters
    ----------
    grille : dict
        DESCRIPTION.
    taille : int
        DESCRIPTION.
    coords : tuple
        DESCRIPTION.

    Returns
    -------
    grille.

    """
    liste_cases_allie = [coords]
    if grille[coords]["nbr_mine"] == 0:
        x = coords[0]
        y = coords[1]
        liste_case_within = [(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1),(x-1,y-1)]
        for coord in liste_case_within:
            if grille.get(coord, "-1") != "-1" and grille[coord]["type"] == "normale" and grille[coord]["nbr_mine"] == 0 and grille[coord]["estVisible"] == False:
                liste_cases_allie.append(coord)
    
    for case in liste_cases_allie:
        decouvrirZone(True,grille,case)
    
    return grille

def main(taille=5):
    """
    Fonction principale du programme avec la logique d'exécution'
    """
    print("Regles : ")
    print("x --> abscisse \ny --> ordonnée \nSymbole M --> mine")
    print("")
    print("----[Debut]----\n")

    # Initialiser la grille
    isCheck = True
    while isCheck:
        reponse = input("Selectionner Mode (facile, moyen, difficile) : ")
        if reponse == "facile":
            taille = 4
            isCheck = False
        elif reponse == "moyen":
            taille = 6
            isCheck = False
        elif reponse == "difficile":
            taille = 9
            isCheck = False
        else:
            print("Erreur syntaxe")
    demineur = grille(taille)
    demineur = statutCaseDepart(demineur)
    # Générer les nbrs
    demineur = mineAdjacenteDepart(grille=demineur,taille=taille)
    # Aider le joueur au debut
    x,y = (random.randint(1, taille),random.randint(1, taille))
    liste_case_within = [(x,y),(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    for coord in liste_case_within:
        if demineur.get(coord, "-1") != "-1":
            demineur[coord]["estVisible"] = True
    
    
    case_decouverte = 0
    case_statut = ""
    jeu_statut = True
    print("Comment interagir ??? \nExemple : \nc11 pour creuser une case en x=1 et y=1 \nd11 pour poser un drapeau en x=1 et y=1\ne : exit")
    print("")
    while jeu_statut:
        # Affiche à chaque fois la grille
        afficher(demineur,taille)
        
        # Demande les coords
        saisieUser = saisie(taille)
        
        # Analyse les coords
        case_statut = ()
        if len(saisieUser["case"]) != 0:    
            case_statut = recupererCaseStatut(saisieUser["case"],demineur)
        # On définit l'etat de victoire ou pas
        data = regle(case_statut, demineur, case_decouverte, saisieUser["case"],saisieUser["drapeau"],taille)
        jeu_statut = data[0]
        case_decouverte = case_decouverte + data[1]
        
        
        if case_decouverte == pow(taille,2) - int(0.40 *  pow(taille,2)): # A refaire
            jeu_statut = False
            print("Vous avez gagnée")
        
        
        
        
    print("Fin du jeu, merci de votre participation !!!")

main(5)
