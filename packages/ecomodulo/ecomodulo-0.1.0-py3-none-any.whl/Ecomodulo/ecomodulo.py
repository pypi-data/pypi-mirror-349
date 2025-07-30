import math      

#fonction de calcul de pourçentage
def pourcentage (valeur, total):
    a = valeur*total/100
    print(a)

# fonction de calcul de CA
def CA (pu , qte):
    a = pu * qte
    print(a)

#fonction de calcul de benefice
def benef(CA, couts):
    a = CA - couts
    print(a)


#fonction de calcul de cout moyen
def cout_moyen(cout_total, qte_produite):
    a = cout_total / qte_produite
    print(a)
