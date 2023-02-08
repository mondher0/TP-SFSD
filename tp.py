# bismillah
# -*- coding: utf-8 -*-
from pickle import dumps,loads
from sys import getsizeof

global b
global tnom
global tprénom
global tnuminscpt 
global taffiliation
#taille du bloc: un bloc peut contenir au max b enregitrements 
b=2
#taille du champ numéro inscription
tnum=10  
#taille du champ nom
tnom=20
#taille du champ prénom  
tprénom=20 
#taille du champ affiliation
taffiliation=20 
# Tetud  c'est la taille totale d'un enregitrement
Tetud=tnum+tnom+tprénom+taffiliation
# fixer la taille d'un enregitrement 
Tnreg='#'*(Tetud+1)  
global buf
Tbloc=[0,[Tnreg]*b,-1] #
global blocsize
blocsize=getsizeof(dumps(Tbloc))+len(Tnreg)*(b-1)+(b-1)

def resize_chaine(chaine, maxtaille):
    for i in range(len(chaine),maxtaille):
          chaine=chaine+'#' 
    return chaine

def lireBloc(file,i):
    dp=2*getsizeof(dumps(0))+i*blocsize
    file.seek(dp,0);
    buf=file.read(blocsize)
    return (loads(buf))

def ecrireBloc(file,i,bf):
    dp=2*getsizeof(dumps(0))+i*blocsize
    file.seek(dp,0)
    file.write(dumps(bf))
    return


def affecter_entete(file,of,c):
    dp=of*getsizeof(dumps(0))
    file.seek(dp,0)
    file.write(dumps(c))
    return

def entete(file,offset):
    dp=offset*getsizeof(dumps(0))
    file.seek(dp,0)
    c=file.read(getsizeof(dumps(0)))
    return loads(c)


def créer_fichier():
    fn=input('Entrer le nom du fichier à créer: ')
    j=0
    i=0
    n=0
    buf = [0, [Tnreg]*b , -1]
    try:
      f = open(fn,'wb')
    except:
        print("impossible d'ouvrir le fichier en mode d'écriture ")
        return
    f_index = open('fileindex','w')
    f_debordement = open('filedebordement',"wb")
    rep='O'
    while(rep=='O'):
        print("Entrer les information de l'étudiant: ")
        num=input("Enter le numéro d'inscription : ")
        nom=input('Entrer le nom: ')
        prénom=input('Entrer le prénom: ')
        affiliation=input("Entrer l'affiliation: ")
        num=resize_chaine(num,tnum)
        nom=resize_chaine(nom,tnom)
        prénom=resize_chaine(prénom,tprénom)
        affiliation=resize_chaine( affiliation,taffiliation)
        etud=num+nom+prénom+affiliation+'T'
        n=n+1
        if (j<b):
           buf[1][j]=etud #mettre l'enregitrement dans le tableau  
           buf[0] += 1 #augmenter le buf.NB
           j += 1
           lastnum = num
        else: 
            ecrireBloc(f,i,buf)
            f_index.write(lastnum.replace('#',"") + "\n")
            # rénitialiser le tableau d'enregitrement et le Nb
            buf = [1, [Tnreg]*b , -1]
            buf[1][0] = etud
            j = 1
            i += 1
        rep=input('Avez vous un autre élement à entrer O/N: ').upper() 
    ecrireBloc(f,i,buf) 
    f_index.write(num.replace('#',"") + "\n")
    affecter_entete(f,0,n)
    affecter_entete(f,1,i+1)
    affecter_entete(f_debordement,0,0)
    affecter_entete(f_debordement,1,0)
    f.close()
    return 

def afficher_fichier():
      fn=input('Entrer le nom du fichier à afficher: ')
      try :
        f = open(fn,'rb')
      except:
        print("erreur lors de l'ouverture du fichier")
        return
      file_debordement = open('filedebordement',"rb")
      secondcar=entete(f,1)
      print(f'votre fichier contient {secondcar} block \n')
      for i in range (secondcar):
            buf=lireBloc(f,i)
            print(f'Le contenu du block {i+1} est: ' )
            # pour chaque enregitrement dans le tableau 
            for j in range(buf[0]):
                if buf[1][j][-1:] != 'F':
                    print(buf[1][j][:-1].replace('#'," "))# afficher l'enregistrement
            while buf[2] != -1:
                print(f"le contenu du bloc {buf[2]} dans le fichier de débordement est : ")
                buf = lireBloc(file_debordement,buf[2])
                for j in range(buf[0]):
                    if buf[1][j][-1:] != 'F':
                        print(buf[1][j][:-1].replace('#'," "))# afficher l'enregistrement
                  
      return

def recherche():
    file = input('entrez le nom du fichier : ')
    try:
        f = open(file,"rb")
    except:
        print("erreur lors de l'ouverture")
        return
    cle = input('entrez la clé à rechercher : ')
    file_index = open('fileindex',"r")
    file_debordement = open('filedebordement','rb')
    # recherche dichotomique a l'interieur du fichier index:
    l = file_index.readlines()
    v = False
    for i in range(entete(f,1)): # on cherche la clé dans le fichier index
        if l[i][:-1] != 'empty' and l[i][:-1] >= cle:
           v = True
           break
        i += 1
    if not v : # on ne l'a pas trouvé, donc insertion à la fin du premier fichier
        print(-1,-1,False)
        return(-1,-1,False)
    buf = lireBloc(f,i) # on lit le bloc dans lequel devrait se trouver l'enregistrement
    for j in range(buf[0]): # on cherche la clé
        if buf[1][j][:10].replace("#","") == cle  and buf[1][j][-1:] == 'T':
            print(i,j,True)
            return[i,j,True] # on l'a trouvée
        if buf[1][j][:10].replace("#","") > cle  and buf[1][j][-1:] == 'T':
            print(i,j,False)
            return[i,j,False] # on a trouvé sa place
    while buf[2] != -1:
        i1 = buf[2]
        j1 = buf[0]
        buf = lireBloc(file_debordement,buf[2]) # on cherche dans le fichier de débordement
        for j in range(buf[0]):
            if buf[1][j][:10].replace("#","") == cle  and buf[1][j][-1:] == 'T':
                print(i1,j,True,True)
                return[i1,j,True,True]
    print(i1,j1,False,False)
    return[i1,j1,False,False]

def recherche2(f,cle):
    file_index = open('fileindex',"r")
    file_debordement = open('filedebordement','rb')
    # recherche dichotomique a l'interieur du fichier index:
    l = file_index.readlines()
    v = False
    for i in range(entete(f,1)): # on cherche la clé dans le fichier index
        if l[i][:-1] != 'empty' and l[i][:-1] >= cle:
           v = True
           break
        i += 1
    if not v : # on ne l'a pas trouvé, donc insertion à la fin du premier fichier
        return(-1,-1,False)
    buf = lireBloc(f,i) # on lit le bloc dans lequel devrait se trouver l'enregistrement
    for j in range(buf[0]): # on cherche la clé
        if buf[1][j][:10].replace("#","") == cle and buf[1][j][-1:] == 'T':
            return[i,j,True] # on l'a trouvée
        if buf[1][j][:10].replace("#","") > cle and buf[1][j][-1:] == 'T':
            return[i,j,False] # on a trouvé sa place
    while buf[2] != -1:
        i1 = buf[2]
        j1 = buf[0]
        buf = lireBloc(file_debordement,buf[2]) # on cherche dans le fichier de débordement
        for j in range(buf[0]):
            if buf[1][j][:10].replace("#","") == cle  and buf[1][j][-1:] == 'T':
                return[i1,j,True,True]
    return[i1,j1,False,False]

def insertion():
    file = input('entrez le nom du fichier : ')
    try:
        f = open(file,"rb+")
    except:
        print("erreur lors de l'ouverture")
        return
    file_index = open('fileindex','r')
    file_debordement = open("filedebordement",'rb+')
    print("Entrer les information de l'étudiant: ")
    num=input("Enter le numéro d'inscription : ")
    rech = recherche2(f,num)
    if rech[2]:
        print("la clé existe déjà")
        return
    nom=input('Entrer le nom: ')
    prénom=input('Entrer le prénom: ')
    affiliation=input("Entrer l'affiliation: ")
    num=resize_chaine(num,tnum)
    nom=resize_chaine(nom,tnom)
    prénom=resize_chaine(prénom,tprénom)
    affiliation=resize_chaine( affiliation,taffiliation)
    etud=num+nom+prénom+affiliation+'T'   
    if rech[0] == -1 : # insertion fin
        buf = lireBloc(f,entete(f,1)-1)
        if buf[0] == b: # nouveau bloc à la fin
            buf = [1,[Tnreg]*b,-1]
            buf[1][0] = etud
            ecrireBloc(f,entete(f,1),buf)
            affecter_entete(f,1,entete(f,1)+1)
            file_index.close()
            file_index = open('fileindex','a')
            file_index.write(num.replace("#","") + '\n')
            affecter_entete(f,0,entete(f,0)+1)
        else: # on insère à la fin du bloc
            buf[1][buf[0]] = etud
            buf[0] += 1
            ecrireBloc(f,entete(f,1)-1,buf)
            affecter_entete(f,0,entete(f,0)+1)
            l = file_index.readlines()
            l[entete(f,1)-1] = num.replace('#',"") + "\n"
            file_index.close()
            file_index = open('fileindex',"w")
            file_index.writelines(l)
    elif len(rech) == 3: # c'est a dire on doit faire des décalages
        if rech[2] == 0 and rech[0] != 0: # c'est a dire qu'on peut insérer l'element dans le bloc préc
            buf = lireBloc(f,rech[0]-1) # on va dans le bloc précédent
            l = file_index.readlines()
            l[rech[0]-1] = num.replace('#',"") + "\n" # on remplace dans l'index psq mtn c le pls grand num
            file_index.close()
            file_index = open('fileindex',"w")
            file_index.writelines(l)
            if buf[2] == -1: # il n y aucun bloc dans le débordement, on en crée un nv
                buf[2] = entete(file_debordement,1)
                ecrireBloc(f,rech[0]-1,buf) # on mets le pointeur a jour
                buf = [1,[Tnreg]*b,-1]
                buf[1][0] = etud
                ecrireBloc(file_debordement,entete(file_debordement,1),buf)
                affecter_entete(file_debordement,1,entete(file_debordement,1)+1)
                affecter_entete(file_debordement,0,entete(file_debordement,0)+1)
            else:
                while buf[2] != -1: # on cherche le dernier bloc de débordement
                    i = buf[2]
                    buf = lireBloc(file_debordement,buf[2])
                if buf[0] != b: # si le dernier bloc n'est pas plein on rajoute à la fin
                    buf[1][buf[0]] = etud
                    buf[0] += 1
                    ecrireBloc(file_debordement,i,buf)
                    affecter_entete(file_debordement,0,entete(f,0)+1) # on augmente le nb d'enregistrements
                else : # si le dernier bloc est plein, on en crée un nv
                    buf[2] = entete(file_debordement,1)
                    ecrireBloc(file_debordement,i,buf) # le pointeur
                    buf = [1,[Tnreg]*b,-1]
                    buf[1][0] = etud
                    ecrireBloc(file_debordement,entete(file_debordement,1),buf)
                    affecter_entete(file_debordement,1,entete(file_debordement,1)+1)
                    affecter_entete(file_debordement,0,entete(file_debordement,0)+1)
        else: # on va faire des décalages:
            buf = lireBloc(f,rech[0])
            if buf[0] != b: # il y a de la place dans le bloc
                for j in range(buf[0]-1,rech[1],-1):
                    buf[1][j] = buf[1][j-1]
                buf[1][rech[1]] = etud
                ecrireBloc(f,buf[0],buf)
            else:
                a_decaler = buf[1][buf[0]-1]
                for j in range(buf[0]-1,rech[1],-1):
                    buf[1][j] = buf[1][j-1]
                buf[1][rech[1]] = etud
                ecrireBloc(f,rech[0],buf)
                if buf[2] == -1: # il n y aucun bloc dans le débordement, on en crée un nv
                    buf[2] = entete(file_debordement,1) # le pointeur
                    ecrireBloc(f,rech[0],buf)
                    buf = [1,[Tnreg]*b,-1]
                    buf[1][0] = a_decaler
                    ecrireBloc(file_debordement,entete(file_debordement,1),buf)
                    affecter_entete(file_debordement,1,entete(file_debordement,1)+1)
                    affecter_entete(file_debordement,0,entete(file_debordement,0)+1)
                else:
                    while buf[2] != -1: # on cherche le dernier bloc de débordement
                        i = buf[2]
                        buf = lireBloc(file_debordement,buf[2])
                    if buf[0] != b: # si le dernier bloc n'est pas plein on rajoute à la fin
                        buf[1][buf[0]] = a_decaler
                        buf[0] += 1
                        ecrireBloc(file_debordement,i,buf)
                        affecter_entete(file_debordement,0,entete(file_debordement,0)+1) # on augmente le nb d'enregistrements
                    else : # si le dernier bloc est plein, on en crée un nv
                        buf[2] = entete(file_debordement,1)
                        ecrireBloc(file_debordement,i,buf) # le pointeur...
                        buf = [1,[Tnreg]*b,-1]
                        buf[1][0] = a_decaler
                        ecrireBloc(file_debordement,entete(file_debordement,1),buf)
                        affecter_entete(file_debordement,1,entete(file_debordement,1)+1)
                        affecter_entete(file_debordement,0,entete(file_debordement,0)+1)

    elif len(rech) == 4: # insertion dans la zone de débordement
        buf = lireBloc(file_debordement,rech[0])
        if buf[0] == b: # on crée un nv bloc
            buf[2] = entete(file_debordement,1) # le pointeur
            ecrireBloc(file_debordement,rech[0],buf)
            buf = [1,[Tnreg]*b,-1]
            buf[1][0] = etud
            ecrireBloc(file_debordement,entete(file_debordement,1),buf)
            affecter_entete(file_debordement,1,entete(file_debordement,1)+1)
            affecter_entete(file_debordement,0,entete(file_debordement,0)+1)
        else: # il y a encore de la place dans un bloc de débordement
            buf[1][buf[0]] = etud
            buf[0] += 1
            ecrireBloc(file_debordement,rech[0],buf)
            affecter_entete(file_debordement,0,entete(file_debordement,0)+1)
    f.close()
    file_debordement.close()
    file_index.close()


def suppression():
    file = input('entrez le nom du fichier : ')
    try:
        f = open(file,'rb+')
    except:
        print('erreur')
        return
    f_debordement = open("filedebordement","rb+")
    f_index = open('fileindex','r')
    cle = input('entrez la clé à supprimer : ')
    rech = recherche2(f,cle)
    if not rech[2]:
        print("la clé n'existe pas")
        return
    buf = lireBloc(f,rech[0])
    buf[1][rech[1]] = buf[1][rech[1]][:-1] + "F" # on modifie puis on écrit
    ecrireBloc(f,rech[0],buf)
    if len(rech) == 4:
        i = rech[3]
    else:
        i = rech[0]
    l = f_index.readlines()
    max = 'empty'
    if l[i][:-1] ==  buf[1][rech[1]][:10].replace('#',""): # c'est a dire on doit chercher le max pr remplacer dans l'index
        buf = lireBloc(f,i)
        for j in range(buf[0]):
            if (max == "empty" and buf[1][j][-1:] == 'T') or (max != 'empty' and buf[1][j][:10].replace('#',"") > max and buf[1][j][-1:] == 'T') :
                max = buf[1][j][:10].replace('#',"") 
        while buf[2] != -1:
            buf = lireBloc(f_debordement,buf[2])
            for j in range(buf[0]):
                if (max == False and buf[1][j][-1:] == 'T') or (max != 'empty' and buf[1][j][:10].replace('#',"") > max and buf[1][j][-1:] == 'T') :
                    max = buf[1][j][:10].replace('#',"") 
        l[i] = max + "\n"
        f_index.close()
        f_index = open('fileindex','w')
        f_index.writelines(l)

    f_index.close()
    f.close()
    f_debordement.close()




def reorganisation():
    file = input('entrez le nom du fichier que vous voulez réorganiser : ')
    try:
        f = open(file,'rb')
    except:
        print("erreur")
        return
    f_debordement = open('filedebordement','rb')
    nvfile = input('entrez le nom du nouveau fichier : ')
    nvfile = open(nvfile,'wb') # le nom du fichier dans lequel on a réorganisé
    i1 = 0
    j1 = 0
    n = 0
    buf1 = [0, [Tnreg]*b , -1]
    for i in range(entete(f,1)):
        buf = lireBloc(f,i)
        for j in range(buf[0]):
            if buf[1][j][-1:] == 'T':
                if (j1<b):
                    buf1[1][j1] = buf[1][j]  
                    buf1[0] += 1 
                    j1 += 1
                    n += 1
                else:
                    ecrireBloc(nvfile,i1,buf1)
                    buf1 = [1, [Tnreg]*b , -1]
                    buf1[1][0] = buf[1][j]
                    j1 = 1
                    i1 += 1
                    n += 1
        lindex = []
        lbuf = []
        while buf[2] != -1:
            buf = lireBloc(f_debordement,buf[2])
            for j in range(buf[0]):
                if buf[1][j][-1:] == 'T':
                    cle = float(buf[1][j][:10].replace("#",""))
                    lindex.append(cle)
                    lindex.sort()
                    emp = lindex.index(cle)
                    lbuf.insert(emp,buf[1][j])
        for el in lbuf:
            if (j1<b):
                buf1[1][j1] = el 
                buf1[0] += 1 
                j1 += 1
                n += 1
            else:
                ecrireBloc(nvfile,i1,buf1)
                buf1 = [1, [Tnreg]*b , -1]
                buf1[1][0] = el
                j1 = 1
                i1 += 1
                n += 1
    ecrireBloc(nvfile,i1,buf1)
    affecter_entete(nvfile,0,n)
    affecter_entete(nvfile,1,i1+1)
    nvfile.close()
    f.close()


def requete_a_intervalle():
    file = input('entrez le nom du fichier : ')
    try:
        f = open(file,'rb')
    except:
        print("erreur")
        return
    c1 = input('entrez la première valeur : ')
    c2 = input('entrez la deuxième valeur : ')
    c1 = min(c1,c2)
    c2 = max(c1,c2)
    file_index = open('fileindex',"r")
    l = file_index.readlines()
    if c1 > l[entete(f,1)-1][:-1] :
        print('borne min plus grand que le max')
        return
    k = 0    
    for el in l:
        if el[:-1] > c1:
            break
        k += 1
    file_debordement = open('filedebordement','rb')
    for i in range(k,entete(f,1)):
        buf = lireBloc(f,i)
        for j in range(buf[0]):
            if buf[1][j][:10].replace("#","") >= c1 and buf[1][j][:10].replace("#","") <= c2 and buf[1][j][-1:] == 'T':
                print(buf[1][j].replace('#'," "))
            if buf[1][j][:10].replace("#","") > c2 :
                return
        while buf[2] != -1:
            buf = lireBloc(file_debordement,buf[2]) # on cherche dans le fichier de débordement
            for j in range(buf[0]):
                if buf[1][j][:10].replace("#","") >= c1 and buf[1][j][:10].replace("#","") <= c2 and buf[1][j][-1:] == 'T':
                    print(buf[1][j].replace("#"," "))
        
    








                

    

    

def default():
    return "choix invalid"
    
def choix(ch):
    switcher = {
        1: créer_fichier,
        2: afficher_fichier,
        3: recherche,
        4: insertion,
        5: suppression,
        6: reorganisation,
        7: requete_a_intervalle
    }
    return switcher.get(ch, default)()

def main():       
    
    rep='O' 
    while (rep=='O'):
        print("""Entrer votre choix 
                 1: créer_fichier
                 2: afficher_fichier
                 3: recherche
                 4: insertion
                 5: suppression
                 6: reorganisation
                 7: requete_a_intervalle""" )
        ch=int(input())
        choix(ch)
        rep=input('Avez vous une autre opération O/N? ').upper()

main()