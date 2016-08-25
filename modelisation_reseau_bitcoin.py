# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 15:55:27 2016

@author: Raphaël
"""

#Paramètre : nombre de noeuds, distribution des degrés.
#But estimer le nombre de composantes connexe.
#On assimile le réseau bitcoin a un graphe aléatoire.



from random import uniform, randint

def calcule_deg(i,deg,degré):
    r=uniform(0,1)
    k=0
    while r>deg[k]:
        k+=1
    degré[i]=k
    
def select_hasard(l):
    return(l[randint(0,len(l)-1)])
    
def connecte(i,v,voisins,non_voisins,degré):
    voisins[i].append(v)
    voisins[v].append(i)
    degré[i]-=1
    degré[v]-=1
    non_voisins[i].remove(v)
    non_voisins[v].remove(i)
    if degré[v]==0:
        for j in range(len(non_voisins)):
            if v in non_voisins[j]:
                non_voisins[j].remove(v)
    if degré[i]==0:
        for j in range(len(non_voisins)):
            if i in non_voisins[j]:
                non_voisins[j].remove(i)
                
#Cette fonction est utile si on ajoute des noeuds spv, ils ne doivent pas se connecter en dernier au réseau (sinon on construit
                # des paires de noeuds SPV)               
def melange(l,k):
    n=len(l)
    for i in range(k):
        j = randint(0,n-1)
        t = randint(0,n-1)
        s=l[j]
        l[j]=l[t]
        l[t]=s
        
#~Composantes connexes
def composantes_connexes(voisins):
    cc=[[i] for i in range(len(voisins))]
    def cherche(i,l):
        for j in l:
            if i in j:
                return(j)
    for i in range(len(voisins)):
        v=voisins[i]
        for k in v:
            ci=cherche(i,cc)
            ck=cherche(k,cc)
            if ci!=ck:
                cc.remove(ci)
                cc.remove(ck)
                cc.append(ci+ck)
    return(cc)

#simulation de selfish mining, le mineur égoïste est 0 avec 100 voisins.    
def test(k):      
    p=[]
    for u in range(k):          
        i=randint(1,n-1)
        egoiste=0
        l=[i]
        ego=[egoiste]
        r=0
        boo=False
        while len(l)+len(ego)<len(cc[0]):
            if not boo:
                r+=1
                lu=[]
                for u in l:
                    for t in voisins[u]:
                        boo= boo or t==egoiste
                        if not t in l and not t in lu and not t in ego:
                            lu.append(t)
                l=l+lu
            else:
                r+=1
                lu=[]
                lego=[]
                for u in ego:
                    for t in voisins[u]:
                        if not t in l and not t in lego and not t in ego:
                            lego.append(t)
                ego=ego+lego
                for u in l:
                    for t in voisins[u]:
                        if not t in l and not t in lu and not t in ego:
                            lu.append(t)
                l=l+lu
        p.append(len(ego))
    return(p)   
                
#Distribution venant de coinscope.
deg=[0]
p=0
for i in range(1,7):
    p+=1/20
    deg.append(p)
for i in range(7,13):
    p+=0.1
    deg.append(p)
for i in range(100):
    p+=0.001
    deg.append(p)

#Taille du réseau Bitcoin
nf=5000 #nombre de full nodes
ns=0 #nombre de noeuds spv
n=nf+ns

#Liste de voisins
voisins=[[] for i in range(n)]
non_voisins=[[i for i in range(n)] for j in range(n)]

for i in range(n):
    non_voisins[i].remove(i)

#liste des degrés encore à pourvoir
degré=[0 for i in range(n)]

degré[0]=100
for i in range(1,nf):
    calcule_deg(i,deg,degré)
    print(i)
for i in range(nf,n):
    degré[i]=1
    
#melange(degré,n)
degré2=degré.copy()
    
for i in range(n):
    while (not not non_voisins[i]) and degré[i]>0:
        connecte(i,select_hasard(non_voisins[i]),voisins,non_voisins,degré)
    print(i)


vrai_deg=[]
for v in voisins:
    vrai_deg.append(len(v))
    
li=[]
for i in range(len(vrai_deg)):
    if vrai_deg[i]!=degré2[i]:
        li.append(i)
    
m=0
for d in vrai_deg:
    m+=d
m=m/n


    
cc=composantes_connexes(voisins)

test(10)
        
                