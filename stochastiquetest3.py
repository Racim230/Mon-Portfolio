import numpy as np
from scipy.optimize import linprog

# 1. Entrée des données
def lire_donnees():
    n = int(input("Entrer la cardinalité de E (nombre d'états) : "))  # Nombre d'états
    delta = [int(input(f"Nombre de décisions pour l'état {i + 1} : ")) for i in range(n)]  # Nombre de décisions pour chaque état

    tableau = []
    for i in range(n):
        for j in range(delta[i]):
            print(f"Entrer les données pour l'état {i + 1}, décision {j + 1} :")
            from fractions import Fraction
            p_ij = list(map(lambda x: float(Fraction(x)), input("Probabilités (séparées par des espaces) : ").split()))
            c_ij = list(map(float, input("Coûts (séparés par des espaces) : ").split()))  # Accepter plusieurs coûts séparés par un espace
            a_i = float(input("Valeur a_i : "))
            tableau.append((i + 1, j + 1, p_ij, c_ij, a_i))  # Ajouter les données pour cet état et décision
    return n, delta, tableau


# 2. Demander à l'utilisateur s'il s'agit d'un problème de maximisation ou minimisation
def choisir_type_probleme():
    choix = input("Est-ce un problème de maximisation (m) ou minimisation (mi) ? : ").strip().lower()
    if choix == 'm':
        return 'maximisation'
    elif choix == 'mi':
        return 'minimisation'
    else:
        print("Choix non valide, veuillez entrer 'm' ou 'mi'.")
        return choisir_type_probleme()

# 3. Génération d'une politique initiale arbitraire
def politique_initiale(delta):
    return [1 for _ in delta]  # Initialisation : on prend toujours la première décision

# 4. Conversion en programme linéaire
def construire_programme_lineaire(n, delta, tableau, politique):
    A = []  # Matrice des contraintes
    b = []  # Second membre
    c = []  # Vecteur des coûts

    for i, j, p_ij, c_ij, a_i in tableau:
        if j == politique[i - 1]:  # On ne considère que les décisions de la politique courante
            A.append(p_ij)
            b.append(a_i)
            c.extend(c_ij)  # Ajouter les coûts à c (au lieu de les ajouter ligne par ligne)

    # Convertir A et b en matrices numpy pour linprog
    A = np.array(A)
    b = np.array(b)
    c = np.array(c)

    return A, b, c

# 5. Résolution du PL
def resoudre_pl(A, b, c, type_probleme):
    c = np.array(c)  # S'assurer que c est un tableau numpy
    if c.ndim != 1:
        print(f"Avertissement : c n'est pas 1D, on l'aplatit.")
        c = c.flatten()  # Aplatir en un tableau 1D si nécessaire
    
    if type_probleme == 'maximisation':
        c = -c  # Maximisation implique de prendre le négatif du vecteur de coûts pour linprog
    res = linprog(c, A_eq=A, b_eq=b, method="simplex")
    return res.x, res.fun

# 6. Mise à jour de la politique
def mise_a_jour_politique(tableau, n, delta, x):
    nouvelle_politique = []
    for i in range(n):
        max_val = -float('inf')
        meilleur_decision = 1
        for j in range(delta[i]):
            # Calcul de la valeur totale pour chaque décision
            val = sum(x[k] * p_ij[k] for k, p_ij in enumerate(tableau) if tableau[k][0] == i + 1 and tableau[k][1] == j + 1)
            if val > max_val:
                max_val = val
                meilleur_decision = j + 1
        nouvelle_politique.append(meilleur_decision)
    return nouvelle_politique

# Boucle principale
def algorithme_stochastique():
    n, delta, tableau = lire_donnees()
    type_probleme = choisir_type_probleme()
    politique = politique_initiale(delta)
    
    while True:
        A, b, c = construire_programme_lineaire(n, delta, tableau, politique)
        x, g = resoudre_pl(A, b, c, type_probleme)
        print(f"Valeur de G : {g}")
        
        nouvelle_politique = mise_a_jour_politique(tableau, n, delta, x)
        if nouvelle_politique == politique:
            print("Politique optimale trouvée :", politique)
            break
        politique = nouvelle_politique

# Lancer l'algorithme
algorithme_stochastique()
