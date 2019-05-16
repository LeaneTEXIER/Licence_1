from random import randint
from turtle import*

couleur={'0':'blue','1':'green','2':'red','3':'yellow','4':'orange','5':'purple','6':'brown','7':'hot pink','8':'cyan','9':'salmon'}
couleur_fr1={'b':'0','v':'1','r':'2','j':'3','o':'4','p':'5','m':'6','f':'7','c':'8','s':'9'}
couleur_fr2={'0':'bleu','1':'vert','2':'rouge','3':'jaune','4':'orange','5':'prune','6':'marron','7':'fushia','8':'cyan','9':'saumon'}

h=0
points_ordi=0
points_joueur=0
points_joueur1=0
points_joueur2=0

def instr(nb_coul):
    """Ecrit quelques instructions sur la fenêtre turtle"""
    penup()
    goto(-200,350)
    pendown()
    color('red')
    write("*     *  *******  *******  *******  *******   *******  *     *  *******   *       *  ****     ")
    penup()
    goto(-200,345)
    pendown()
    write("**   **  *      *  *               *     *           *       *  **   **     *       **      *  *   *    ")
    penup()
    goto(-200,340)
    pendown()
    write("* * * *  *      *  *               *     *           *       *  * * * *     *       * *     *  *    *   ")
    penup()
    goto(-200,335)
    pendown()
    write("*  *  *  *******  *******       *     *******   *******  *  *  *     *       *    *  *  *    *  ")
    penup()
    goto(-200,330)
    pendown()
    write("*     *  *       *          *       *     *           * *        *     *     *       *     * *  *    *   ")
    penup()
    goto(-200,325)
    pendown()
    write("*     *  *       *          *       *     *           *   *      *     *     *       *      **  *   *    ")
    penup()
    goto(-200,320)
    pendown()
    write("*     *  *       *  *******       *     *******   *     *    *     *  *******  *       *  ****     ")
    penup()
    goto(-300,300)
    pendown()
    color('black')
    coul=""
    for i in range (nb_coul):
        coul=coul+couleur_fr2[str(i)]+" "
    write("Suivant le nombre de couleurs que vous avez déclarés en paramètre, voici la liste des couleurs disponibles:")
    penup()
    goto(-300,282)
    pendown()
    write(coul)
    penup()
    goto(-300,254)
    pendown()
    write("Il peut y avoir plusieurs fois la même couleur dans la combinaison.\nVous devez rentrer que les premières lettres des couleurs.")
   
def ligne(nb_pions):
    """
    Dessine une ligne de cercle comme base pour le support, avec nb_pions*cercle
    pour la proposition de combinaisons, et nb_pions*cercle pour la correction
    """
    speed(200)
    bgcolor("lightgrey")
    for k in range(2):
        for i in range(nb_pions):
            circle(10)
            penup()
            forward(30)
            pendown()
        penup()
        forward(50)
        pendown()

def support(nb_pions,nb_max_coup,nb_coul):
    """
    Dessine le support du mastermind : les hauteurs des lignes en fonction du nombre de coups maximum autorisés, et
    la longueur des lignes en fonction du nombre de pions souhaités.
    """
    instr(nb_coul)
    penup()
    goto(-320,-260)
    pendown()
    begin_fill()
    fillcolor("PaleGreen1")
    for i in range(2):
        forward((nb_pions)*50+80+20) #nb_pions*(diametre+espace entre cercle)+espace entre combi/correction + 20 de chaque coté du suppport
        left(90)
        forward(nb_max_coup*32)
        left(90)
    end_fill()
    
    penup()
    goto(-300,-250)
    pendown()
    for i in range(1,nb_max_coup+1):
        ligne(nb_pions)
        penup()
        goto(-300,-250+(i*30)) #faire monter les lignes
        pendown()
    penup()
    goto(-300,-240)
    pendown() 

def couleurs_pions(proposition):
    """
    Rempli les trous avec la couleur demandée par le joueur
    """
    for i in proposition:
        dot(22,couleur[i])
        penup()
        forward(30)
        pendown()
           
def couleurs_pions_correct(nb_pions,proposition,combi):
    """
    Rempli les trous de fiches blanches ou noires selon l'evaluation de la combinaison
    pour la phase 1
    """
    global h
    penup()
    forward(50)
    pendown()
    for i in range(nb_pions+1):
        for j in range(nb_pions+1):
            if evalue(proposition,combi)==(i,j):
                for a in range(i):
                    dot(22,'black') 
                    penup()
                    forward(30)
                    pendown()
                for b in range(j):
                    dot(22,'white') 
                    penup()
                    forward(30)
                    pendown()               
    penup()
    goto(-300,-240+(h*30)) #faire monter les lignes
    left(90)
    forward(30)
    right(90)
    pendown()
    h+=1

def couleurs_pions_correct2(nb_pions,bien_place,mal_place):
    """
    Rempli les trous de fiches blanches ou noires selon l'evaluation de la combinaison
    pour la phase 2, 3 et 4
    """
    global h
    penup()
    forward(50)
    pendown()
    for i in range(nb_pions+1):
        for j in range(nb_pions+1):
            if int(bien_place)==i and int(mal_place)==j:
                for a in range(i):
                    dot(21,'black') 
                    penup()
                    forward(30)
                    pendown()
                for b in range(j):
                    dot(21,'white') 
                    penup()
                    forward(30)
                    pendown()               
    penup()
    goto(-300,-240+(h*30)) #faire monter les lignes
    left(90)
    forward(30)
    right(90)
    pendown()
    h+=1
    
def choix_alea(nb_pions,nb_coul):
    """
    int,int->str
    Renvoie la combinaison secrete chiffrée en fonction du nombre de pions et de couleurs
    CU : nb_pions et nb_couleurs sont des entiers avec nb_coul<11
    """
    assert(type(nb_pions)==int),"Le nombre de pions doit être un entier"
    assert(type(nb_coul)==int),"Le nombre de couleurs doit être un entier"
    assert(nb_coul<11),"Le nombre de couleurs doit être <11"
    combi=""
    for i in range(nb_pions):
        combi=combi+str(randint(0,nb_coul-1))
    return combi

def evalue(proposition,combi):
    """
    str,str->tuple
    Renvoie le nombre de pions bien placés et le nombre de pions de la bonne couleur mais mal placés
    CU: proposition et combi doivent être des chaines de meme longueur
    """
    assert (type(proposition)==str),"La proposition doit être une chaine de caractères"
    assert (type(combi)==str),"La combinaison doit être une chaine de caractères"
    bien_place=0
    mal_place=0
    for i in range(len(proposition)):
        if proposition[i]==combi[i]:
            bien_place+=1  
    for j in proposition:
        if j in combi:
            mal_place+=1
            ind1=proposition.index(j)
            ind2=combi.index(j)
            proposition=proposition[:ind1]+proposition[ind1+1:]
            combi=combi[:ind2]+combi[ind2+1:]
    return(bien_place,mal_place-bien_place)

def prop_correct(combi_chiffre,nb_pions):
    """
    str,int-> NoneType
    Verfie si la proposition est correcte.
    CU: La proposition est une chaine de caractères et nb_pions est un entier
    """
    assert (type(combi_chiffre)==str),"La proposition doit être une chaine de caractères"
    assert(type(nb_pions)==int),"Le nombre de pions doit être un entier"
    if len(combi_chiffre)!=nb_pions:
        print('Votre proposition doit être de longueur',nb_pions)
        return False


def phase1(nb_pions,nb_coul,nb_max_coup):
    """
    Fait deviner la combinaison secrète au joueur en un nombre d'essais limités
    """
    global points_ordi
    global points_joueur
    combi=choix_alea(nb_pions,nb_coul)
    combi_devoile="" 
    for i in combi: 
        combi_devoile=combi_devoile+couleur_fr2[i]+" " 
    nb_coup=1
    support(nb_pions,nb_max_coup,nb_coul)
    while(nb_coup<=nb_max_coup):
        proposition=input('Entrez une proposition de combinaison : ')
        combi_chiffre=""
        for i in proposition:
            combi_chiffre=combi_chiffre+couleur_fr1[i] 
        while prop_correct(combi_chiffre,nb_pions)==False:
            proposition=input('Entrez une proposition de combinaison : ')
            combi_chiffre=""
            for i in proposition:
                combi_chiffre=combi_chiffre+couleur_fr1[i]
        couleurs_pions(combi_chiffre)
        if evalue(combi_chiffre,combi)!=(nb_pions,0):
            print(nb_coup,proposition,evalue(combi_chiffre,combi))
            nb_coup+=1
        couleurs_pions_correct(nb_pions,combi_chiffre,combi)
        if evalue(combi_chiffre,combi)==(nb_pions,0):
            points_joueur+=1
            clear()
            return ('Bravo ! Vous avez trouvé la réponse')
    clear()
    points_ordi+=1
    print("Perdu ! Vous avez dépassé votre nombre de coups autorisés\nLa réponse était",combi_devoile) 
        
               
############ Phase 2

def choix_alea2(l):
    """
    Choisi une combinaison au hasard dans la liste de toutes les combibinaisons possibles
    """
    i=randint(0,(len(l)-1))
    return l[i]
            
def combi_possibles(nb_pions,nb_coul):
    """
    Renvoie la liste de toutes les combinaisons possibles
    """
    liste=[]
    fin=str(nb_coul-1)*nb_pions
    for i in range(int(fin)+1):
        if len(str(i))<len(fin):  
            liste.append('0'*(nb_pions-len(str(i)))+str(i))
        else:
            liste.append(str(i))
    for i in liste:
        for x in range(nb_coul,10):
            for i in liste:
                if str(x) in str(i) and i in liste:
                    liste.remove(str(i))  
    return liste

def autres(proposition, liste,bien_place,mal_place):
    """
    Crée une nouvelle liste qui garde seulement les combinaisons possibles après l'évalutation du joueur codeur
    """
    nvl_liste=[]
    for i in liste:
        if evalue(proposition,i)==(bien_place,mal_place):
            nvl_liste.append(i)
    return nvl_liste

def phase2(nb_pions, nb_coul, nb_max_coup):
    """
    Fait chercher la combinaison secrete à l'ordinateur en un nombre de coups limités
    """
    global points_ordi
    global points_joueur
    print("A vous de choisir une combinaison !")
    support(nb_pions,nb_max_coup,nb_coul)
    liste_combi=combi_possibles(nb_pions,nb_coul)
    nb_coup=0
    while (nb_coup<nb_max_coup):
        nb_coup+=1
        proposition=choix_alea2(liste_combi)
        combi_lettre=""
        for i in proposition:
            combi_lettre=combi_lettre+couleur_fr2[i]+" "
        print("L'ordinateur propose :",combi_lettre)
        couleurs_pions(proposition) 
        bien_place=int(input("Nombre de pions bien placés : "))
        mal_place=int(input("Nombre de pions mal placés : "))
        couleurs_pions_correct2(nb_pions,bien_place,mal_place)
        if int(bien_place)==nb_pions and int(mal_place)==0:
            points_ordi+=1
            clear()
            return("L'ordinateur a gagné en",nb_coup,"coups")
        liste_combi=autres(proposition,liste_combi,bien_place,mal_place)
    clear()
    points_joueur+=1
    return("L'ordinateur n'a pas su trouver la réponse en",nb_max_coup,"coups.")

################# Phase 3
    
def phase3(nb_pions, nb_coul, nb_max_coup):
    """
    Fait chercher la combinaison secrete d'un humain (joueur2) à un autre humain (joueur1) en un nombre de coups limités
    """
    global points_joueur1
    global points_joueur2
    support(nb_pions,nb_max_coup,nb_coul)
    nb_coup=0
    while (nb_coup<nb_max_coup):
        proposition=input('Entrez une proposition de combinaison : ')
        nb_coup+=1
        combi_chiffre=""
        for i in proposition:
            combi_chiffre=combi_chiffre+couleur_fr1[i]
        while prop_correct(combi_chiffre,nb_pions)==False:
            proposition=input('Entrez une proposition de combinaison : ')
            combi_chiffre=""
            for i in proposition:
                combi_chiffre=combi_chiffre+couleur_fr1[i]
        couleurs_pions(combi_chiffre)
        bien_place=int(input("Nombre de pions bien placés : "))
        mal_place=int(input("Nombre de pions mal placés : "))
        couleurs_pions_correct2(nb_pions,bien_place,mal_place)
        if int(bien_place)==nb_pions and int(mal_place)==0:
            points_joueur1+=1
            clear()
            return("Le joueur 1 a gagné en",nb_coup,"coups")
    clear()
    points_joueur2+=1
    return("Le joueur 1 n'a pas su trouver la réponse en",nb_max_coup,"coups.")

def phase4(nb_pions, nb_coul, nb_max_coup):
    """
    Fait chercher la combinaison secrete d'un humain (joueur1) à un autre humain (joueur2) en un nombre de coups limités
    """
    global points_joueur1
    global points_joueur2
    support(nb_pions,nb_max_coup,nb_coul)
    nb_coup=0
    while (nb_coup<nb_max_coup):
        proposition=input('Entrez une proposition de combinaison : ')
        nb_coup+=1
        combi_chiffre=""
        for i in proposition:
            combi_chiffre=combi_chiffre+couleur_fr1[i]
        while prop_correct(combi_chiffre,nb_pions)==False:
            proposition=input('Entrez une proposition de combinaison : ')
            combi_chiffre=""
            for i in proposition:
                combi_chiffre=combi_chiffre+couleur_fr1[i]
        couleurs_pions(combi_chiffre)
        bien_place=int(input("Nombre de pions bien placés : "))
        mal_place=int(input("Nombre de pions mal placés : "))
        couleurs_pions_correct2(nb_pions,bien_place,mal_place)
        if int(bien_place)==nb_pions and int(mal_place)==0:
            points_joueur2+=1
            clear()
            return("Le joueur 2 a gagné en",nb_coup,"coups")
    clear()
    points_joueur1+=1
    return("Le joueur 2 n'a pas su trouver la réponse en",nb_max_coup,"coups.")
   

#################JEU

def jouer():
    """
    Fait jouer le jeu au joueur codeur puis au joueur decodeur jusqu'a un nombre de points souhaités
    """
    global h
    global points_joueur1
    global points_joueur2
    global points_ordi
    global points_joueur
    option=int(input("Vous voulez jouer contre un humain ou un ordinateur? (Répondez 1 pour un humain et 2 pour un ordinateur)"))
    if (option==1):
        prenom1=input("Comment s'appelle le joueur 1 ? ")
        prenom2=input("Comment s'appelle le joueur 2 ? ")
        points_gagnants=int(input("En combien de points gagnants voulez-vous jouer ? "))
        commencement=input("Qui commence à découvrir la combinaison ? (Répondez 1 pour le joueur 1 et 2 pour le joueur 2) ")
        while (commencement!="1") and (commencement!="2"): 
            commencement=input("Choix impossible\nQui commence à découvrir la combinaison ? (Répondez 1 pour le joueur 1 et 2 pour le joueur 2) ")
        nb_pions=int(input("Avec combien de pions voulez-vous jouer ? (Nombre compris entre 3 et 5) "))
        while (nb_pions<3 or nb_pions>5):
            nb_pions=int(input("Choix impossible\Avec combien de pions voulez-vous jouer ? (Nombre compris entre 3 et 5) "))
        nb_coul=int(input("Avec combien de couleurs voulez-vous jouer ? (Nombre compris entre 2 et 10) "))
        while (nb_coul<2 or nb_coul>10):
            nb_coul=int(input("Choix impossible\nAvec combien de couleurs voulez-vous jouer ? (Nombre compris entre 2 et 10) "))
        nb_max_coup=int(input("En combien de coups maximum voulez-vous jouer ? (Nombre compris entre 2 et 15) "))
        while (nb_coul<2 or nb_coul>15):
            nb_max_coup=int(input("Choix impossible\nEn combien de coups maximum voulez-vous jouer ? (Nombre compris entre 2 et 15) "))
        if commencement=="1":
            while (points_joueur1!=points_gagnants) and (points_joueur2!=points_gagnants):
                phase3(nb_pions,nb_coul,nb_max_coup)
                h=0
                print (prenom1,":",points_joueur1, "\n",prenom2,":",points_joueur2) 
                if (points_joueur1!=points_gagnants) and (points_joueur2!=points_gagnants):
                    phase4(nb_pions,nb_coul,nb_max_coup)
                    h=0
                    print (prenom1,":",points_joueur1, "\n",prenom2,":",points_joueur2) 
        else:
            while (points_joueur1!=points_gagnants) and (points_joueur2!=points_gagnants):
                phase4(nb_pions,nb_coul,nb_max_coup)
                h=0
                print (prenom1,":",points_joueur1, "\n",prenom2,":",points_joueur2) 
                if (points_joueur1!=points_gagnants) and (points_joueur2!=points_gagnants):
                    phase3(nb_pions,nb_coul,nb_max_coup)
                    h=0
                    print (prenom1,":",points_joueur1, "\n",prenom2,":",points_joueur2) 
        if points_joueur2==points_gagnants:
            (points_joueur1_ann,points_joueur1)=(points_joueur1,0)
            (points_joueur2_ann,points_joueur2)=(points_joueur2,0)
            print (prenom2, "a gagné avec",points_joueur2_ann,"point(s) contre",points_joueur1_ann,"point(s) pour",prenom1," !")
        elif points_joueur1==points_gagnants:
            (points_joueur2_ann,points_joueur2)=(points_joueur2,0)
            (points_joueur1_ann,points_joueur1)=(points_joueur1,0)
            print (prenom1, "a gagné avec",points_joueur1_ann,"point(s) contre",points_joueur2_ann,"point(s) pour",prenom2," !")
    elif (option==2):
        prenom=input("Comment vous appelez-vous ? ")
        points_gagnants=int(input("En combien de points gagnants voulez-vous jouer ? "))
        commencement=input("Qui commence à découvrir la combinaison ? (Répondez 1 pour vous et 2 pour l'ordinateur) ")
        while (commencement!="1") and (commencement!="2"):
            commencement=input("Choix impossible\nQui commence à découvrir la combinaison ? (Répondez 1 pour le joueur 1 et 2 pour le joueur 2) ")
        nb_pions=int(input("Avec combien de pions voulez-vous jouer ? (Nombre compris entre 3 et 5) "))
        while (nb_pions<3 or nb_pions>5):
            nb_pions=int(input("Choix impossible\nAvec combien de pions voulez-vous jouer ? (Nombre compris entre 3 et 5) "))
        nb_coul=int(input("Avec combien de couleurs voulez-vous jouer ? (Nombre compris entre 2 et 10) "))
        while (nb_coul<2 or nb_coul>10):
            nb_coul=int(input("Choix impossible\nAvec combien de couleurs voulez-vous jouer ? (Nombre compris entre 2 et 10) "))
        nb_max_coup=int(input("En combien de coups maximum voulez-vous jouer ? (Nombre compris entre 2 et 15) "))
        while (nb_coul<2 or nb_coul>15):
            nb_max_coup=int(input("Choix impossible\nEn combien de coups maximum voulez-vous jouer ? (Nombre compris entre 2 et 15) "))
        if commencement=="1":
            while (points_ordi!=points_gagnants) and (points_joueur!=points_gagnants):
                phase1(nb_pions,nb_coul,nb_max_coup)
                h=0
                print (prenom,":",points_joueur, "\n ordi :",points_ordi) 
                if (points_ordi!=points_gagnants) and (points_joueur!=points_gagnants):
                    phase2(nb_pions,nb_coul,nb_max_coup)
                    h=0
                    print (prenom,":",points_joueur, "\n ordi :",points_ordi) 
        else:
            while (points_ordi!=points_gagnants) and (points_joueur!=points_gagnants):
                phase2(nb_pions,nb_coul,nb_max_coup)
                h=0
                print (prenom,":",points_joueur, "\n ordi :",points_ordi) 
                if (points_ordi!=points_gagnants) and (points_joueur!=points_gagnants):
                    phase1(nb_pions,nb_coul,nb_max_coup)
                    h=0
                    print (prenom,":",points_joueur, "\n ordi :",points_ordi) 
        if points_ordi==points_gagnants:
            (points_ordi_ann,points_ordi)=(points_ordi,0)
            (points_joueur_ann,points_joueur)=(points_joueur,0)
            print ("L'ordinateur a gagné avec",points_ordi_ann,"point(s) contre",points_joueur_ann,"point(s) pour vous",prenom," !")
        elif points_joueur==points_gagnants:
            (points_ordi_ann,points_ordi)=(points_ordi,0)
            (points_joueur_ann,points_joueur)=(points_joueur,0)
            print ("Vous,",prenom,", avez gagné avec",points_joueur_ann,"point(s) contre",points_ordi_ann,"point(s) pour l'ordinateur !")
    else:
        return ("Choix impossible")

jouer()
