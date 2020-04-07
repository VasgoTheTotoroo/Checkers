import tkinter
import random
import time
import numpy
import numba
from numba import jit

#################################################################################
#
#  Parametres du jeu

canvas = None   # zone de dessin

#Grille[0][0] désigne la case en haut à gauche
#Grille[2][0] désigne la case en haut à droite
#Grille[0][2] désigne la case en bas à gauche


Grille = numpy.zeros((10,10))  # attention les lignes représentent les colonnes de la grille
           
Scores = [0,0]   # score du joueur 1 (Humain) et 2 (IA)

#################################################################################

# gestion du joueur humain et de l'IA

WIDTH = 1000
humain="blanc"
temps=0.2
simulation=False
nbparties=2
nbcoupsavance=1

def NouvellePartie():
    for i in range(0,10):
        for j in range(0,10):
            Grille[i][j]=0
    for i in range(0,4,2):
        for j in range(0,9,2):
            Grille[j+1][i]=2
            Grille[j][i+1]=2
            Grille[8-j][9-i]=1
            Grille[7-j][8-i]=1
    
NouvellePartie()

def Normalistation(Liste):
    b=0
    l=[]
    for i in range(len(Liste)-1,-1,-1):
        if Liste[i]==[]:
            b=b+1
        else:
            break
    for e in range(len(Liste)-b):
        l.append(Liste[e])
    
    return l

def Path(Liste):
    Liste=Normalistation(Liste)
        
    Final=[]
    Intermediaire=[]
    i=0
    a=0
    
    while i<len(Liste):
        if Liste[i]!= []:
            Intermediaire.append(Liste[i])
            a=i+1
        else:
            Final.append(Intermediaire)
            c=1
            a=i+1
            for j in range(i+1,len(Liste)):
                if Liste[j]==[]:
                    c=c+1
                else:
                    a=j
                    break
            Intermediaire=Intermediaire[0:-c]
        i=a
    
    if Intermediaire:
        Final.append(Intermediaire)
    return Final

def MangerDame(x,y,k,Liste,Manger):
    
    #Joueur IA
    if k==4:
    
        #haut gauche
        for i in range(1,9):
            if x-i>0 and y-i>0:
                if Grille[x-i][y-i]==2 or Grille[x-i][y-i]==4 or ((Grille[x-i][y-i]==1 or Grille[x-i][y-i]==3) and (Grille[x-i-1][y-i-1]==1 or Grille[x-i-1][y-i-1]==3)):
                    break
                if (Grille[x-i][y-i]==1 or Grille[x-i][y-i]==3) and Grille[x-i-1][y-1-i]==0:
                    for j in range(1,10-i):
                        if x-i-j<0 or y-j-i<0:
                            break
                        if Grille[x-i-j][y-i-j]==0:
                            AncienPion=Grille[x-i][y-i]
                            Grille[x-i][y-i]=2
                            Manger.append((x-i,y-i))
                            Grille[x-i-j][y-j-i]=4
                            Liste.append((x-i-j,y-j-i))
                            MangerDame(x-i-j,y-j-i,k,Liste,Manger)
                            Grille[x-i][y-i]=AncienPion
                            Grille[x-i-j][y-j-i]=0
                            Liste.append([])
                            Manger.append([])
                        else:
                            break
                    break
            else:
                break
                
        #haut droit
        for i in range(1,9):
            if x+i<9 and y-i>0:
                if Grille[x+i][y-i]==2 or Grille[x+i][y-i]==4 or ((Grille[x+i][y-i]==1 or Grille[x+i][y-i]==3) and (Grille[x+i+1][y-i-1]==1 or Grille[x+i+1][y-i-1]==3)):
                    break
                if (Grille[x+i][y-i]==1 or Grille[x+i][y-i]==3) and Grille[x+i+1][y-1-i]==0:
                    for j in range(1,10-i):
                        if x+i+j>9 or y-j-i<0:
                            break
                        if Grille[x+i+j][y-j-i]==0:
                            AncienPion=Grille[x+i][y-i]
                            Grille[x+i][y-i]=2
                            Manger.append((x+i,y-i))
                            Liste.append((x+i+j,y-j-i))
                            Grille[x+i+j][y-j-i]=4
                            MangerDame(x+i+j,y-j-i,k,Liste,Manger)
                            Grille[x+i][y-i]=AncienPion
                            Grille[x+i+j][y-j-i]=0
                            Liste.append([])
                            Manger.append([])
                        else:
                            break
                    break
            else:
                break
                
        #bas gauche
        for i in range(1,9):
            if x-i>0 and y+i<9:
                if Grille[x-i][y+i]==2 or Grille[x-i][y+i]==4 or ((Grille[x-i][y+i]==1 or Grille[x-i][y+i]==3) and (Grille[x-i-1][y+i+1]==1 or Grille[x-i-1][y+i+1]==3)):
                    break
                if (Grille[x-i][y+i]==1 or Grille[x-i][y+i]==3) and Grille[x-i-1][y+1+i]==0:
                    for j in range(1,10-i):
                        if x-i-j<0 or y+j+i>9:
                            break
                        if Grille[x-i-j][y+j+i]==0:
                            AncienPion=Grille[x-i][y+i]
                            Grille[x-i][y+i]=2
                            Liste.append((x-i-j,y+j+i))
                            Manger.append((x-i,y+i))
                            Grille[x-i-j][y+j+i]=4
                            MangerDame(x-i-j,y+j+i,k,Liste,Manger)
                            Grille[x-i][y+i]=AncienPion
                            Grille[x-i-j][y+j+i]=0
                            Liste.append([])
                            Manger.append([])
                        else:
                            break
                    break
            else:
                break
                
        #bas droit
        for i in range(1,9):
            if x+i<9 and y+i<9:
                if Grille[x+i][y+i]==2 or Grille[x+i][y+i]==4 or ((Grille[x+i][y+i]==1 or Grille[x+i][y+i]==3) and (Grille[x+i+1][y+i+1]==1 or Grille[x+i+1][y+i+1]==3)):
                    break
                if (Grille[x+i][y+i]==1 or Grille[x+i][y+i]==3) and Grille[x+i+1][y+1+i]==0:
                    for j in range(1,10-i):
                        if x+i+j>9 or y+j+i>9:
                            break
                        if Grille[x+i+j][y+j+i]==0:
                            AncienPion=Grille[x+i][y+i]
                            Grille[x+i][y+i]=2
                            Liste.append((x+i+j,y+j+i))
                            Manger.append((x+i,y+i))
                            Grille[x+i+j][y+j+i]=4
                            MangerDame(x+i+j,y+j+i,k,Liste,Manger)
                            Grille[x+i][y+i]=AncienPion
                            Grille[x+i+j][y+j+i]=0
                            Liste.append([])
                            Manger.append([])
                        else:
                            break
                    break
            else:
                break
                    
    if k==3:
                  
        #haut gauche
        for i in range(1,9):
            if x-i>0 and y-i>0:
                if Grille[x-i][y-i]==1 or Grille[x-i][y-i]==3 or ((Grille[x-i][y-i]==2 or Grille[x-i][y-i]==4) and (Grille[x-i-1][y-i-1]==2 or Grille[x-i-1][y-i-1]==4)):
                    break
                if (Grille[x-i][y-i]==2 or Grille[x-i][y-i]==4) and Grille[x-i-1][y-1-i]==0:
                    for j in range(1,10-i):
                        if x-i-j<0 or y-j-i<0:
                            break
                        if Grille[x-i-j][y-i-j]==0:
                            AncienPion=Grille[x-i][y-i]
                            Grille[x-i][y-i]=1
                            Manger.append((x-i,y-i))
                            Grille[x-i-j][y-j-i]=3
                            Liste.append((x-i-j,y-j-i))
                            MangerDame(x-i-j,y-j-i,k,Liste,Manger)
                            Grille[x-i][y-i]=AncienPion
                            Grille[x-i-j][y-j-i]=0
                            Liste.append([])
                            Manger.append([])
                        else:
                            break
                    break
            else:
                break
                
        #haut droit
        for i in range(1,9):
            if x+i<9 and y-i>0:
                if Grille[x+i][y-i]==1 or Grille[x+i][y-i]==3 or ((Grille[x+i][y-i]==2 or Grille[x+i][y-i]==4) and (Grille[x+i+1][y-i-1]==2 or Grille[x+i+1][y-i-1]==4)):
                    break
                if (Grille[x+i][y-i]==2 or Grille[x+i][y-i]==4) and Grille[x+i+1][y-1-i]==0:
                    for j in range(1,10-i):
                        if x+i+j>9 or y-j-i<0:
                            break
                        if Grille[x+i+j][y-j-i]==0:
                            AncienPion=Grille[x+i][y-i]
                            Grille[x+i][y-i]=1
                            Manger.append((x+i,y-i))
                            Liste.append((x+i+j,y-j-i))
                            Grille[x+i+j][y-j-i]=3
                            MangerDame(x+i+j,y-j-i,k,Liste,Manger)
                            Grille[x+i][y-i]=AncienPion
                            Grille[x+i+j][y-j-i]=0
                            Liste.append([])
                            Manger.append([])
                        else:
                            break
                    break
            else:
                break
                
        #bas gauche
        for i in range(1,9):
            if x-i>0 and y+i<9:
                if Grille[x-i][y+i]==1 or Grille[x-i][y+i]==3 or ((Grille[x-i][y+i]==2 or Grille[x-i][y+i]==4) and (Grille[x-i-1][y+i+1]==2 or Grille[x-i-1][y+i+1]==4)):
                    break
                if (Grille[x-i][y+i]==2 or Grille[x-i][y+i]==4) and Grille[x-i-1][y+1+i]==0:
                    for j in range(1,10-i):
                        if x-i-j<0 or y+j+i>9:
                            break
                        if Grille[x-i-j][y+j+i]==0:
                            AncienPion=Grille[x-i][y+i]
                            Grille[x-i][y+i]=1
                            Liste.append((x-i-j,y+j+i))
                            Manger.append((x-i,y+i))
                            Grille[x-i-j][y+j+i]=3
                            MangerDame(x-i-j,y+j+i,k,Liste,Manger)
                            Grille[x-i][y+i]=AncienPion
                            Grille[x-i-j][y+j+i]=0
                            Liste.append([])
                            Manger.append([])
                        else:
                            break
                    break
            else:
                break
                
        #bas droit
        for i in range(1,9):
            if x+i<9 and y+i<9:
                if Grille[x+i][y+i]==1 or Grille[x+i][y+i]==3 or ((Grille[x+i][y+i]==2 or Grille[x+i][y+i]==4) and (Grille[x+i+1][y+i+1]==2 or Grille[x+i+1][y+i+1]==4)):
                    break
                if (Grille[x+i][y+i]==2 or Grille[x+i][y+i]==4) and Grille[x+i+1][y+1+i]==0:
                    for j in range(1,10-i):
                        if x+i+j>9 or y+j+i>9:
                            break
                        if Grille[x+i+j][y+j+i]==0:
                            AncienPion=Grille[x+i][y+i]
                            Grille[x+i][y+i]=1
                            Liste.append((x+i+j,y+j+i))
                            Manger.append((x+i,y+i))
                            Grille[x+i+j][y+j+i]=3
                            MangerDame(x+i+j,y+j+i,k,Liste,Manger)
                            Grille[x+i][y+i]=AncienPion
                            Grille[x+i+j][y+j+i]=0
                            Liste.append([])
                            Manger.append([])
                        else:
                            break
                    break
            else:
                break

def MangerPion(x,y,k,Liste,Manger):
    
    #Joueur IA
    if k==2:
    
        #HautDroite
        if x<8 and y>1:
            if (Grille[x+1][y-1]==1 or Grille[x+1][y-1]==3) and Grille[x+2][y-2]==0:
                AncienPion=Grille[x+1][y-1]
                Grille[x+1][y-1]=0
                Manger.append((x+1,y-1))
                Grille[x+2][y-2]=2
                Liste.append((x+2,y-2))
                MangerPion(x+2,y-2,2,Liste,Manger)
                Grille[x+1][y-1]=AncienPion
                Grille[x+2][y-2]=0
                Liste.append([])
                Manger.append([])
           
        #haut gauche
        if x>1 and y>1:
            if (Grille[x-1][y-1]==1 or Grille[x-1][y-1]==3) and Grille[x-2][y-2]==0:
                AncienPion=Grille[x-1][y-1]
                Grille[x-1][y-1]=0
                Manger.append((x-1,y-1))
                Grille[x-2][y-2]=2
                Liste.append((x-2,y-2))
                MangerPion(x-2,y-2,2,Liste,Manger)
                Grille[x-1][y-1]=AncienPion
                Grille[x-2][y-2]=0
                Liste.append([])
                Manger.append([])
            
        #Bas Gauche
        if x>1 and y<8:
            if (Grille[x-1][y+1]==1 or Grille[x-1][y+1]==3) and Grille[x-2][y+2]==0:
                AncienPion=Grille[x-1][y+1]
                Grille[x-1][y+1]=0
                Manger.append((x-1,y+1))
                if y+2==9:
                    Grille[x-2][y+2]=4
                    Liste.append((x-2,y+2))
                    Grille[x-1][y+1]=AncienPion
                    Grille[x-2][y+2]=0
                    Liste.append([])
                    Manger.append([])
                else:
                    Grille[x-2][y+2]=2
                    Liste.append((x-2,y+2))
                    MangerPion(x-2,y+2,2,Liste,Manger)
                    Grille[x-1][y+1]=AncienPion
                    Grille[x-2][y+2]=0
                    Liste.append([])
                    Manger.append([])
        
        #bas Droite
        if x<8 and y<8:
            if (Grille[x+1][y+1]==1 or Grille[x+1][y+1]==3) and Grille[x+2][y+2]==0:
                AncienPion=Grille[x+1][y+1]
                Grille[x+1][y+1]=0
                Manger.append((x+1,y+1))
                if y+2==9:
                    Grille[x+2][y+2]=4
                    Liste.append((x+2,y+2))
                    Grille[x+1][y+1]=AncienPion
                    Grille[x+2][y+2]=0
                    Liste.append([])
                    Manger.append([])
                else:
                    Grille[x+2][y+2]=2
                    Liste.append((x+2,y+2))
                    MangerPion(x+2,y+2,2,Liste,Manger)
                    Grille[x+1][y+1]=AncienPion
                    Grille[x+2][y+2]=0
                    Liste.append([])
                    Manger.append([])
                
    if k==1:
    
        #HautDroite
        if x<8 and y>1:
            if (Grille[x+1][y-1]==2 or Grille[x+1][y-1]==4) and Grille[x+2][y-2]==0:
                AncienPion=Grille[x+1][y-1]
                Grille[x+1][y-1]=0
                Manger.append((x+1,y-1))
                if y-2==0:
                    Grille[x+2][y-2]=3
                    Liste.append((x+2,y-2))
                    Grille[x+1][y-1]=AncienPion
                    Grille[x+2][y-2]=0
                    Liste.append([])
                    Manger.append([])
                else:
                    Grille[x+2][y-2]=1
                    Liste.append((x+2,y-2))
                    MangerPion(x+2,y-2,1,Liste,Manger)
                    Grille[x+1][y-1]=AncienPion
                    Grille[x+2][y-2]=0
                    Liste.append([])
                    Manger.append([])
           
        #haut gauche
        if x>1 and y>1:
            if (Grille[x-1][y-1]==2 or Grille[x-1][y-1]==4) and Grille[x-2][y-2]==0:
                AncienPion=Grille[x-1][y-1]
                Grille[x-1][y-1]=0
                Manger.append((x-1,y-1))
                if y-2==0:
                    Grille[x-2][y-2]=3
                    Liste.append((x-2,y-2))
                    Grille[x-1][y-1]=AncienPion
                    Grille[x-2][y-2]=0
                    Liste.append([])
                    Manger.append([])
                else:
                    Grille[x-2][y-2]=1
                    Liste.append((x-2,y-2))
                    MangerPion(x-2,y-2,1,Liste,Manger)
                    Grille[x-1][y-1]=AncienPion
                    Grille[x-2][y-2]=0
                    Liste.append([])
                    Manger.append([])
            
        #Bas Gauche
        if x>1 and y<8:
            if (Grille[x-1][y+1]==2 or Grille[x-1][y+1]==4) and Grille[x-2][y+2]==0:
                AncienPion=Grille[x-1][y+1]
                Grille[x-1][y+1]=0
                Manger.append((x-1,y+1))
                Grille[x-2][y+2]=1
                Liste.append((x-2,y+2))
                MangerPion(x-2,y+2,1,Liste,Manger)
                Grille[x-1][y+1]=AncienPion
                Grille[x-2][y+2]=0
                Liste.append([])
                Manger.append([])
        
        #bas Droite
        if x<8 and y<8:
            if (Grille[x+1][y+1]==2 or Grille[x+1][y+1]==4) and Grille[x+2][y+2]==0:
                AncienPion=Grille[x+1][y+1]
                Grille[x+1][y+1]=0
                Manger.append((x+1,y+1))
                Grille[x+2][y+2]=1
                Liste.append((x+2,y+2))
                MangerPion(x+2,y+2,1,Liste,Manger)
                Grille[x+1][y+1]=AncienPion
                Grille[x+2][y+2]=0
                Liste.append([])
                Manger.append([])

def DisponiblePion(x,y,k):
    Liste = []
    Manger= []

    #Joueur IA
    if k==2:

        MangerPion(x,y,2,Liste,Manger)
        Liste=Path(Liste)
        Manger=Path(Manger)
        
        if Manger:        
            return Liste,Manger
    
        #coups sans bouffer juste en avançant
        if x>0 and x<9:
            if Grille[x+1][y+1]==0:
                Liste.append([(x+1,y+1)])
            if Grille[x-1][y+1]==0:
                Liste.append([(x-1,y+1)])
        elif x==0:
            if Grille[x+1][y+1]==0:
                Liste.append([(x+1,y+1)])
        elif x==9:
            if Grille[x-1][y+1]==0:
                Liste.append([(x-1,y+1)])

    #Joueur HUMAIN
    if k==1:
        
        MangerPion(x,y,1,Liste,Manger)
        Liste=Path(Liste)
        Manger=Path(Manger)
        
        if Manger:        
            return Liste,Manger

        #coups sans bouffer juste en avançant
        if x>0 and x<9:
            if Grille[x+1][y-1]==0:
                Liste.append([(x+1,y-1)])
            if Grille[x-1][y-1]==0:
                Liste.append([(x-1,y-1)])
        elif x==0:
            if Grille[x+1][y-1]==0:
                Liste.append([(x+1,y-1)])
        elif x==9:
            if Grille[x-1][y-1]==0:
                Liste.append([(x-1,y-1)])

    return Liste,Manger
    
def DisponibleDame(x,y,k):
    Liste = []
    Manger= []
    
    if k==4:
        
        MangerDame(x,y,4,Liste,Manger)
        Liste=Path(Liste)
        Manger=Path(Manger)
                            
        if Manger:        
            return Liste,Manger
            
    if k==3:
        
        MangerDame(x,y,3,Liste,Manger)
        Liste=Path(Liste)
        Manger=Path(Manger)
                            
        if Manger:
            return Liste,Manger

    #coups sans bouffer juste en avançant
    
    #haut gauche
    for i in range(1,10):
        if x-i>-1 and y-i>-1:
            if Grille[x-i][y-i]==0:
                Liste.append([(x-i,y-i)])
            else:
                break
        else:
            break
                
    #haut droit
    for i in range(1,10):
        if x+i<10 and y-i>-1:
            if Grille[x+i][y-i]==0:
                Liste.append([(x+i,y-i)])
            else:
                break
        else:
            break
                
    #bas gauche
    for i in range(1,10):
        if x-i>-1 and y+i<10:
            if Grille[x-i][y+i]==0:
                Liste.append([(x-i,y+i)])
            else:
                break
        else:
            break
                
    #bas droit
    for i in range(1,10):
        if x+i<10 and y+i<10:
            if Grille[x+i][y+i]==0:
                Liste.append([(x+i,y+i)])
            else:
                break
        else:
            break
                
    return Liste,Manger
  
def PionsRestant(k):
    Liste = []
    for i in range(10):
        for j in range(10):
            if Grille[i][j]==k:
                Liste.append((i,j))
    return Liste
    
def DisponiblePionJoue(k):
    Liste = []
    ListeMange=[]
    for p in PionsRestant(k):
        if DisponiblePion(p[0],p[1],k)[0]!=[]:
            Liste.append(p)
            if DisponiblePion(p[0],p[1],k)[1]:
                    ListeMange.append(p)
                        
    if ListeMange:
        return ListeMange,True
    return Liste,False
    
def DisponibleDameJoue(k):
    Liste = []
    ListeMange=[]
    for p in PionsRestant(k):
        if DisponibleDame(p[0],p[1],k)[0]!=[]:
            Liste.append(p)
            if DisponibleDame(p[0],p[1],k)[1]:
                    ListeMange.append(p)
                        
    if ListeMange:
        return ListeMange,True
    return Liste,False

if humain=="blanc":
    print("\nvous pouvez jouez les pions : \n"+str(DisponiblePionJoue(1)[0])+"\n")
elif humain=="noir":
    print("\nvous pouvez jouez les pions : \n"+str(DisponiblePionJoue(2)[0])+"\n")
        
def IAHasard(couleur):
    if couleur=="blanc":
        cd=3
        cp=1
    elif couleur=="noir":
        cd=4
        cp=2
        
    P=DisponiblePionJoue(cp)[0]
    D=DisponibleDameJoue(cd)[0]
    pma=DisponiblePionJoue(cp)[1]
    dma=DisponibleDameJoue(cd)[1]
    d=False
    
    if (pma and dma) or (not pma and not dma):
        if P and D:
            r=random.randrange(len(P))
            pion=P[r]
            R=random.randrange(len(D))
            dame=D[R]
            q=random.randrange(2)
            if q==0:
                pionjoue=pion
            else:
                pionjoue=dame
                d=True
        elif D and not P:
            R=random.randrange(len(D))
            pionjoue=D[R]
            d=True
        elif P and not D:
            r=random.randrange(len(P))
            pionjoue=P[r]
        else:
            print("-----------ERREUR IA HASARD----------")
    elif pma and not dma:
        r=random.randrange(len(P))
        pionjoue=P[r]
    elif dma and not pma:
        R=random.randrange(len(D))
        pionjoue=D[R]
        d=True
    else:
        print("-----------ERREUR IA HASARD----------")
        
    if d:
        coups=DisponibleDame(pionjoue[0],pionjoue[1],cd)[0]
        manger=DisponibleDame(pionjoue[0],pionjoue[1],cd)[1]
        Q=random.randrange(len(coups))
        coups=coups[Q]
        if manger:
            manger=manger[Q]
        if not simulation:
            Joue(pionjoue,coups,True,manger,couleur)
        else:
            JoueVite(pionjoue,coups,True,manger,couleur)
        return
    else:
        coups=DisponiblePion(pionjoue[0],pionjoue[1],cp)[0]
        manger=DisponiblePion(pionjoue[0],pionjoue[1],cp)[1]
        Q=random.randrange(len(coups))
        coups=coups[Q]
        if manger:
            manger=manger[Q]
        if not simulation:
            Joue(pionjoue,coups,False,manger,couleur)
        else:
            JoueVite(pionjoue,coups,False,manger,couleur)
        return
        return

def partieFinie():
    if aGagne(1) or aGagne(2):
        return True
    if (not DisponiblePionJoue(1)[0] and not DisponibleDameJoue(3)[0]) or (not DisponiblePionJoue(2)[0] and not DisponibleDameJoue(4)[0]) or (len(DisponibleDameJoue(4)[0])==1 and len(DisponibleDameJoue(3)[0])==1 and len(DisponiblePionJoue(1)[0])==0 and len(DisponiblePionJoue(2)[0])==0):
        return True
    return False
    
def evalPions(k):
    score=0
    #125
    if Grille[5][0]==k:
        score=score+125
    if Grille[4][9]==k:
        score=score+125
    #100
    if Grille[3][0]==k:
        score=score+100
    if Grille[7][0]==k:
        score=score+100
    if Grille[2][9]==k:
        score=score+100
    if Grille[6][9]==k:
        score=score+100
    #80
    if Grille[1][0]==k:
        score=score+80
    if Grille[8][9]==k:
        score=score+80
    #75
    if Grille[9][0]==k:
        score=score+75
    if Grille[0][9]==k:
        score=score+75
    #70
    if Grille[2][1]==k:
        score=score+70
    if Grille[4][1]==k:
        score=score+70
    if Grille[6][1]==k:
        score=score+70
    if Grille[8][1]==k:
        score=score+70
    if Grille[1][8]==k:
        score=score+70
    if Grille[3][8]==k:
        score=score+70
    if Grille[5][8]==k:
        score=score+70
    if Grille[7][8]==k:
        score=score+70
    #50
    if Grille[0][1]==k:
        score=score+50
    if Grille[9][8]==k:
        score=score+50
    #40
    if Grille[0][7]==k:
        score=score+40
    if Grille[9][2]==k:
        score=score+40
    #25
    if Grille[1][2]==k:
        score=score+25
    if Grille[0][3]==k:
        score=score+25
    if Grille[8][3]==k:
        score=score+25
    if Grille[9][4]==k:
        score=score+25
    if Grille[1][4]==k:
        score=score+25
    if Grille[0][5]==k:
        score=score+25
    if Grille[8][5]==k:
        score=score+25
    if Grille[9][6]==k:
        score=score+25
    if Grille[1][6]==k:
        score=score+25
    if Grille[8][7]==k:
        score=score+25
    #20
    if Grille[3][2]==k:
        score=score+20
    if Grille[7][2]==k:
        score=score+20
    if Grille[5][2]==k:
        score=score+20
    if Grille[2][7]==k:
        score=score+20
    if Grille[6][7]==k:
        score=score+20
    if Grille[4][7]==k:
        score=score+20
    #10
    for i in range(2,6,2):
        for j in range(3,5,2):
            if Grille[i][j]==k:
                score=score+10
            if Grille[i+1][j+1]==k:
                score=score+10
                
    return score
    
def evalPions2(k):
    if k==1:
        pe=2
    elif k==2:
        pe=1
    return 120*len(DisponiblePionJoue(k)[0])-150*len(DisponiblePionJoue(pe)[0])
    
def evalDames(k):
    score=0
    
    if k==3:
        pe=2
        de=4
    elif k==4:
        pe=1
        de=3
    
    for d in DisponibleDameJoue(k)[0]:
        if DisponibleDameJoue(k)[1]:
            m=DisponibleDame(d[0],d[1],k)[1]
            manger=[]
            for r in m:
                manger.append(len(r))
            score=score+100*max(manger)
            
        for pionE in DisponiblePionJoue(pe)[0]:
            if DisponiblePion(pionE[0],pionE[1],pe)[1]:
                for chemin in DisponiblePion(pionE[0],pionE[1],pe)[1]:
                    if d in chemin:
                        score=score-1000
        for dameE in DisponibleDameJoue(pe)[0]:
            if DisponibleDame(dameE[0],dameE[1],de)[1]:
                for chemin in DisponibleDame(dameE[0],dameE[1],de)[1]:
                    if d in chemin:
                        score=score-1000
    return score
    
def nbDames(k):
    if k==3:
        de=4
    elif k==4:
        de=3
        
    return 250*len(DisponibleDameJoue(k)[0])-300*len(DisponibleDameJoue(de)[0])
    
def eval(couleur):
    if couleur=="blanc":
        p=1
        d=3
        pe=2
    elif couleur=="noir":
        p=2
        d=4
        pe=1
        
    if aGagne(p):
        return 100000
    if aGagne(pe):
        return -100000
    if partieFinie(): #seulement les cas d'égalité car on gère les wins juste en haut !
        return 0
        
    return nbDames(d)+evalPions(p)-evalPions(pe)+evalDames(d)
    
def IAMinMax(couleur,profondeur):
    res=MinMax(couleur,profondeur)
    
    if not simulation:
        Joue(res[1],res[2][0],res[3],res[2][1],couleur)
    else:
        JoueVite(res[1],res[2][0],res[3],res[2][1],couleur)

def MinMax(couleur,profondeur):
    if couleur=="blanc":
        p=1
        d=3
        comp="noir"
    elif couleur=="noir":
        p=2
        d=4
        comp="blanc"

    if profondeur==0 or partieFinie():
        return [eval(couleur)]
        
    ScoresFinaux=[]
    P=DisponiblePionJoue(p)[0]
    D=DisponibleDameJoue(d)[0]
    P1=DisponiblePionJoue(p)[1]
    D1=DisponibleDameJoue(d)[1]
    
    if P and (P1 or (not P1 and not D1)):
        for pion in P:
            dispo=DisponiblePion(pion[0],pion[1],p)
            scores=[]
            coups=dispo[0]
            manger=dispo[1]
            for i in range(len(coups)):
                mem=[]
                if manger:
                    for mange in manger[i]:
                        mem.append(Grille[mange[0]][mange[1]])
                    JoueVite(pion,coups[i],False,manger[i],couleur)
                else:
                    JoueVite(pion,coups[i],False,manger,couleur)
                score=Simule(comp,profondeur-1)[0]
                scores.append(score)
                if manger:
                    Annule(pion,coups[i],False,manger[i],couleur,mem)
                else:
                    Annule(pion,coups[i],False,manger,couleur,mem)
            if manger:
                ScoresFinaux.append([max(scores),[dispo[0][scores.index(max(scores))],dispo[1][scores.index(max(scores))]],pion])
            else:
                ScoresFinaux.append([max(scores),[dispo[0][scores.index(max(scores))],dispo[1]],pion])
                
    inter=[]
    for f in ScoresFinaux:
        inter.append(f[0])
        
    ScoresFinaux2=[]
    
    if D and (D1 or (not D1 and not P1)):
        for pion in D:
            dispo=DisponibleDame(pion[0],pion[1],d)
            scores=[]
            coups=dispo[0]
            manger=dispo[1]
            for i in range(len(coups)):
                mem=[]
                if manger:
                    for mange in manger[i]:
                        mem.append(Grille[mange[0]][mange[1]])
                    JoueVite(pion,coups[i],True,manger[i],couleur)
                else:
                    JoueVite(pion,coups[i],True,manger,couleur)
                score=Simule(comp,profondeur-1)[0]
                scores.append(score)
                if manger:
                    Annule(pion,coups[i],True,manger[i],couleur,mem)
                else:
                    Annule(pion,coups[i],True,manger,couleur,mem)
            if manger:
                ScoresFinaux2.append([max(scores),[dispo[0][scores.index(max(scores))],dispo[1][scores.index(max(scores))]],pion])
            else:
                ScoresFinaux2.append([max(scores),[dispo[0][scores.index(max(scores))],dispo[1]],pion])

    inter2=[]
    for f in ScoresFinaux2:
        inter2.append(f[0])
        
    if inter and inter2:
        Fin=[max(inter),max(inter2)]
        if Fin.index(max(Fin))==0:
            return [max(inter),ScoresFinaux[inter.index(max(inter))][2],ScoresFinaux[inter.index(max(inter))][1],False]
        return [max(inter2),ScoresFinaux2[inter2.index(max(inter2))][2],ScoresFinaux2[inter2.index(max(inter2))][1],True]
    elif inter and not inter2:
        return [max(inter),ScoresFinaux[inter.index(max(inter))][2],ScoresFinaux[inter.index(max(inter))][1],False]
    elif inter2 and not inter:
        return [max(inter2),ScoresFinaux2[inter2.index(max(inter2))][2],ScoresFinaux2[inter2.index(max(inter2))][1],True]
        
def Simule(couleur,profondeur):
    if couleur=="blanc":
        p=1
        d=3
        comp="noir"
    elif couleur=="noir":
        p=2
        d=4
        comp="blanc"

    if profondeur==0 or partieFinie():
        return [eval(comp)]
        
    ScoresFinaux=[]
    P=DisponiblePionJoue(p)[0]
    D=DisponibleDameJoue(d)[0]
    P1=DisponiblePionJoue(p)[1]
    D1=DisponibleDameJoue(d)[1]
    
    if P and (P1 or (not P1 and not D1)):
        for pion in P:
            dispo=DisponiblePion(pion[0],pion[1],p)
            scores=[]
            coups=dispo[0]
            manger=dispo[1]
            for i in range(len(coups)):
                mem=[]
                if manger:
                    for mange in manger[i]:
                        mem.append(Grille[mange[0]][mange[1]])
                    JoueVite(pion,coups[i],False,manger[i],couleur)
                else:
                    JoueVite(pion,coups[i],False,manger,couleur)
                score=MinMax(comp,profondeur-1)[0]
                scores.append(score)
                if manger:
                    Annule(pion,coups[i],False,manger[i],couleur,mem)
                else:
                    Annule(pion,coups[i],False,manger,couleur,mem)
            if manger:
                ScoresFinaux.append([min(scores),[dispo[0][scores.index(min(scores))],dispo[1][scores.index(min(scores))]],pion])
            else:
                ScoresFinaux.append([min(scores),[dispo[0][scores.index(min(scores))],dispo[1]],pion])
                
    inter=[]
    for f in ScoresFinaux:
        inter.append(f[0])
        
    ScoresFinaux2=[]
    
    if D and (D1 or (not D1 and not P1)):
        for pion in D:
            dispo=DisponibleDame(pion[0],pion[1],d)
            scores=[]
            coups=dispo[0]
            manger=dispo[1]
            for i in range(len(coups)):
                mem=[]
                if manger:
                    for mange in manger[i]:
                        mem.append(Grille[mange[0]][mange[1]])
                    JoueVite(pion,coups[i],True,manger[i],couleur)
                else:
                    JoueVite(pion,coups[i],True,manger,couleur)
                score=MinMax(comp,profondeur-1)[0]
                scores.append(score)
                if manger:
                    Annule(pion,coups[i],True,manger[i],couleur,mem)
                else:
                    Annule(pion,coups[i],True,manger,couleur,mem)
            if manger:
                ScoresFinaux2.append([min(scores),[dispo[0][scores.index(min(scores))],dispo[1][scores.index(min(scores))]],pion])
            else:
                ScoresFinaux2.append([min(scores),[dispo[0][scores.index(min(scores))],dispo[1]],pion])

    inter2=[]
    for f in ScoresFinaux2:
        inter2.append(f[0])
        
    if inter and inter2:
        Fin=[min(inter),min(inter2)]
        if Fin.index(min(Fin))==0:
            return [min(inter),ScoresFinaux[inter.index(min(inter))][2],ScoresFinaux[inter.index(min(inter))][1],False]
        return [min(inter2),ScoresFinaux2[inter2.index(min(inter2))][2],ScoresFinaux2[inter2.index(min(inter2))][1],True]
    elif inter and not inter2:
        return [min(inter),ScoresFinaux[inter.index(min(inter))][2],ScoresFinaux[inter.index(min(inter))][1],False]
    elif inter2 and not inter:
        return [min(inter2),ScoresFinaux2[inter2.index(min(inter2))][2],ScoresFinaux2[inter2.index(min(inter2))][1],True]

def aGagne(k): #Un joueur gagne si il ne reste plus de pions à l'adversaire
    if k==1:
        if not PionsRestant(2) and not PionsRestant(4):
            return True
        else:
            return False
    else:
        if not PionsRestant(1) and not PionsRestant(3):
            return True
        else:
            return False
         
def JoueVite(pion,coups,Dame,manger,couleur):
    if couleur=="noir":
        for i in range(len(coups)):
            Grille[pion[0]][pion[1]]=0
            if Dame:
                Grille[coups[i][0]][coups[i][1]]=4
            else:
                if coups[i][1]==9:
                    Grille[coups[i][0]][coups[i][1]]=4
                else:
                    Grille[coups[i][0]][coups[i][1]]=2
            if manger:
                Grille[manger[i][0]][manger[i][1]]=0
            pion=coups[i]  
        
    elif couleur=="blanc":
        for i in range(len(coups)):
            Grille[pion[0]][pion[1]]=0
            if Dame:
                Grille[coups[i][0]][coups[i][1]]=3
            else:
                if coups[i][1]==0:
                    Grille[coups[i][0]][coups[i][1]]=3
                else:
                    Grille[coups[i][0]][coups[i][1]]=1
            if manger:
                Grille[manger[i][0]][manger[i][1]]=0
            pion=coups[i]
         
def Joue(pion,coups,Dame,manger,couleur):
    if couleur=="noir":
        time.sleep(temps)
        Affiche()
        
        for i in range(len(coups)):
            Grille[pion[0]][pion[1]]=0
            if Dame:
                Grille[coups[i][0]][coups[i][1]]=4
            else:
                if coups[i][1]==9:
                    Grille[coups[i][0]][coups[i][1]]=4
                else:
                    Grille[coups[i][0]][coups[i][1]]=2
            if manger:
                Grille[manger[i][0]][manger[i][1]]=0
            time.sleep(temps)
            Affiche()
            pion=coups[i]  
        
    elif couleur=="blanc":
        time.sleep(temps)
        Affiche()
        
        for i in range(len(coups)):
            Grille[pion[0]][pion[1]]=0
            if Dame:
                Grille[coups[i][0]][coups[i][1]]=3
            else:
                if coups[i][1]==0:
                    Grille[coups[i][0]][coups[i][1]]=3
                else:
                    Grille[coups[i][0]][coups[i][1]]=1
            if manger:
                Grille[manger[i][0]][manger[i][1]]=0
            time.sleep(temps)
            Affiche()
            pion=coups[i]
            
def Annule(pion,coups,Dame,manger,couleur,memoire_manger):
    if couleur=="noir":
        cp=2
        cd=4
    elif couleur=="blanc":
        cp=1
        cd=3
        
    if Dame:
        Grille[pion[0]][pion[1]]=cd
    else:
        Grille[pion[0]][pion[1]]=cp
        
    for i in range(len(coups)):
        Grille[coups[i][0]][coups[i][1]]=0
        if manger:
            Grille[manger[i][0]][manger[i][1]]=memoire_manger[i]
            
def Play():
    
    # Tour du joueur blanc
    if humain!="blanc":
        Tstart=time.time()
        #IA
        IAHasard("blanc")
        T=time.time()-Tstart
        #IAMinMax("blanc",2*nbcoupsavance)
        print("Le joueur blanc a mit "+str(T)+" secondes pour jouer.\n")
    
    if aGagne(1):
        Scores[0]+=1
        NouvellePartie()
        return
    if partieFinie():
        NouvellePartie()
        return
        
    #Tour du joueur noir
    
    if humain!="noir":
        Tstart=time.time()
        #IA
        IAMinMax("noir",1+2*nbcoupsavance)
        T=time.time()-Tstart
        print("Le joueur noir a mit "+str(T)+" secondes pour jouer.\n")
    
    if aGagne(2):
        Scores[1]+=1
        NouvellePartie()
        return
    if partieFinie():
        NouvellePartie()
        return
    
    if humain=="blanc":
        cp=1
        cd=3
    elif humain=="noir":
        cp=2
        cd=4
    if humain!="":
        print("------------------------------")
        if DisponiblePionJoue(cp)[0] and (DisponiblePionJoue(cp)[1] or (not DisponiblePionJoue(cp)[1] and not DisponibleDameJoue(cd)[1])):
            print("vous pouvez jouez les pions : \n"+str(DisponiblePionJoue(cp)[0])+"\n")
        if DisponibleDameJoue(cd)[0] and (DisponibleDameJoue(cd)[1] or (not DisponibleDameJoue(cd)[1] and not DisponiblePionJoue(cp)[1])):
            print("vous pouvez jouez les dames : \n"+str(DisponibleDameJoue(cd)[0])+"\n")

################################################################################
#    
# Dessine la grille de jeu

def Affiche(PartieGagnee = False):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
        
        for i in range(0,WIDTH,int(WIDTH/5)):
            for j in range(0,WIDTH,int(WIDTH/5)):
                canvas.create_rectangle(i,j,i+int(WIDTH/10),j+int(WIDTH/10),fill="#C8AD7F")
                canvas.create_rectangle(i+int(WIDTH/10),j+int(WIDTH/10),i+int(WIDTH/5),j+int(WIDTH/5),fill="#C8AD7F")
                
        canvas.create_rectangle(0,WIDTH,WIDTH,WIDTH+int(WIDTH/10),fill="white")
        
        
        for i in range(11):
            for j in range(11):
                canvas.create_line(j*int(WIDTH/10),0,j*int(WIDTH/10),WIDTH,fill="black", width="1" )
                canvas.create_line(0,i*int(WIDTH/10),WIDTH,i*int(WIDTH/10),fill="black", width="1" )
            
        for x in range(10):
            for y in range(10):
                xc = x * int(WIDTH/10)
                yc = y * int(WIDTH/10)
                if ( Grille[x][y] == 1):
                    canvas.create_oval(xc+int(WIDTH/100),yc+int(WIDTH/100),xc+int(WIDTH*(9/100)),yc+int(WIDTH*(9/100)),fill="#FEFEE2", width=str(WIDTH/200) )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+int(WIDTH/100),yc+int(WIDTH/100),xc+int(WIDTH*(9/100)),yc+int(WIDTH*(9/100)),fill="#2F1E0E", width=str(WIDTH/200) )
                if ( Grille[x][y] == 3):
                    canvas.create_oval(xc+int(WIDTH/100),yc+int(WIDTH/100),xc+int(WIDTH*(9/100)),yc+int(WIDTH*(9/100)),fill="#FEFEE2", width=str(WIDTH/200) )
                    canvas.create_text(xc+int(WIDTH/20),yc+int(WIDTH/20),font=('Arial',int(WIDTH*(4/100))),text="Q",fill='black')
                if ( Grille[x][y] == 4):
                    canvas.create_oval(xc+int(WIDTH/100),yc+int(WIDTH/100),xc+int(WIDTH*(9/100)),yc+int(WIDTH*(9/100)),fill="#2F1E0E", width=str(WIDTH/200) )
                    canvas.create_text(xc+int(WIDTH/20),yc+int(WIDTH/20),font=('Arial',int(WIDTH*(4/100))),text="Q",fill='white')
        
        msg = 'SCORES : ' + str(Scores[0]) + '-' + str(Scores[1])
        fillcoul = 'black'
        canvas.create_text(int(WIDTH/2),WIDTH+int(WIDTH*(6/100)), font=('Mistral', int(WIDTH*(9/100))), text = msg, fill=fillcoul)
        
    
        canvas.update()   #force la mise a jour de la zone de dessin
        
  
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def PositionJoue(x,y,k):
    final=[]
    if k==1:
        for e in DisponiblePion(x,y,1)[0]:
            final.append(e[-1])
    elif k==3:
        for e in DisponibleDame(x,y,3)[0]:
            final.append(e[-1])
    elif k==2:
        for e in DisponiblePion(x,y,2)[0]:
            final.append(e[-1])
    elif k==4:
        for e in DisponibleDame(x,y,4)[0]:
            final.append(e[-1])
    return final

def PionJoue(event,x,y,Dame):
    x2 = event.x // int(WIDTH/10)  # convertit une coordonée pixel écran en coord grille de jeu
    y2 = event.y // int(WIDTH/10)
    
    if humain=="noir":
        cd=4
        cp=2
    else:
        cd=3
        cp=1
    
    window.bind("<Button-1>", PionSelection)
    
    if ((x2<0) or (x2>9) or (y2<0) or (y2>9)): #tester si la position pour ce pion est valide
        print("vous ne pouvez pas joué à cette position !\n")
        return
        
    #vérifier que la position ou veut jouer le jouer est valide
    if not Dame:
        if ((x2,y2) not in PositionJoue(x,y,cp)):
            print("vous ne pouvez pas joué à cette position avec le pion !\n")
            return
    else:
        if ((x2,y2) not in PositionJoue(x,y,cd)):
            print("vous ne pouvez pas joué à cette position avec la dame !\n")
            return

    if not Dame:
        idx=PositionJoue(x,y,cp).index((x2,y2))
        chemin=DisponiblePion(x,y,cp)[0][idx]
        manger=DisponiblePion(x,y,cp)[1]
        if manger:
            manger=manger[idx]
        Joue((x,y),chemin,Dame,manger,humain)
    else:
        idx=PositionJoue(x,y,cd).index((x2,y2))
        chemin=DisponibleDame(x,y,cd)[0][idx]
        manger=DisponibleDame(x,y,cd)[1]
        if manger:
            manger=manger[idx]
        Joue((x,y),chemin,Dame,manger,humain)
                
    Play()  # gestion du joueur humain et de l'IA
    Affiche()
    
def PionSelection(event):
    if humain!="":
        if humain=="noir":
            cd=4
            cp=2
        else:
            cd=3
            cp=1
            
        Dame=False
        x = event.x // int(WIDTH/10)  # convertit une coordonée pixel écran en coord grille de jeu
        y = event.y // int(WIDTH/10)
        
        if ((x<0) or (x>9) or (y<0) or (y>9)): #tester si il a séléctionné un pion valide
            print("vous n'avez pas séléctionné de pion !\n")
            return
        if (x,y) in DisponiblePionJoue(cp)[0] and (DisponiblePionJoue(cp)[1] or (not DisponiblePionJoue(cp)[1] and not DisponibleDameJoue(cd)[1])):
            if Grille[x][y]==cp:
                print("vous avez choisi de jouer le pion ("+str(x)+","+str(y)+")\n")
                if DisponiblePion(x,y,cp)[1]:
                    if DisponiblePion(x,y,cp)[1][0]:
                        print("vous pouvez manger les pions :\n"+str(DisponiblePion(x,y,cp)[1])+"\n")
        elif (x,y) in DisponibleDameJoue(cd)[0] and (DisponibleDameJoue(cd)[1] or (not DisponibleDameJoue(cd)[1] and not DisponiblePionJoue(cp)[1])):
            Dame=True
            print("vous avez choisi de jouer la dame ("+str(x)+","+str(y)+")\n")
            if DisponibleDame(x,y,cd)[1]:
                if DisponibleDame(x,y,cd)[1][0]:
                    print("vous pouvez manger les pions :\n"+str(DisponibleDame(x,y,3)[1])+"\n")
        else:
            print("le pion que vous avez choisi ne peut pas bouger !\n")
            return
    
        if Dame:
            print("Avec cette dame, vous pouvez jouer les positions :\n"+str(PositionJoue(x,y,cd))+"\n")
        else:
            print("Avec ce pion, vous pouvez jouer les positions :\n"+str(PositionJoue(x,y,cp))+"\n")
    
        def intermediaire(event,x=x,y=y,Dame=Dame):
            return PionJoue(event,x,y,Dame)
        window.bind("<Button-1>", intermediaire)
    else:
        if simulation:
            while(nbparties>Scores[0]+Scores[1]):
                Play()
            Affiche()
            print("\n----------------------SIMULATION FINI---------------------\n")
        else:
            while(True):
                Play()
            Affiche()

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

# fenetre
window = tkinter.Tk()
window.geometry(str(WIDTH)+"x"+str(int(WIDTH+(WIDTH/10))))
window.title('Dames')
window.protocol("WM_DELETE_WINDOW", lambda : window.destroy())
window.bind("<Button-1>", PionSelection)

#zone de dessin
HEIGHT = WIDTH+int(WIDTH/5)
canvas = tkinter.Canvas(window, width=WIDTH , height=HEIGHT, bg="#4E3D28")
canvas.place(x=0,y=0)
Affiche()
if humain=="noir":
    Play()
 
# active la fenetre 
window.mainloop()