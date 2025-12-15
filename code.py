import time
import os
from typing import Set, Tuple, Iterator

#  Types 
Cellule = Tuple[int, int]
Monde = Set[Cellule]

# Fonctions Pures 

def obtenir_voisins(cellule: Cellule) -> Iterator[Cellule]:
    x, y = cellule
    decalages = [(-1, -1), (-1, 0), (-1, 1),
                 ( 0, -1),          ( 0, 1),
                 ( 1, -1), ( 1, 0), ( 1, 1)]
    return ((x + dx, y + dy) for dx, dy in decalages)

def nb_voisins_vivants(cellule: Cellule, monde: Monde) -> int:
    return sum(1 for v in obtenir_voisins(cellule) if v in monde)

def doit_vivre(cellule: Cellule, monde: Monde) -> bool:
    vivants = nb_voisins_vivants(cellule, monde)
    if cellule in monde:
        return vivants == 2 or vivants == 3
    return vivants == 3

def obtenir_candidats(monde: Monde) -> Set[Cellule]:
    candidats = set(monde)
    for cellule in monde:
        candidats.update(obtenir_voisins(cellule))
    return candidats

def generation_suivante(monde: Monde) -> Monde:
    candidats = obtenir_candidats(monde)
    return {c for c in candidats if doit_vivre(c, monde)}

#  Fonctions d'Affichage 

def formater_monde(monde: Monde) -> str:
    if not monde:
        return "Le monde est vide."
    
    xs = [x for x, y in monde]
    ys = [y for x, y in monde]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    lignes = []
    lignes.append(f"Population : {len(monde)}")
    
    for y in range(min_y - 1, max_y + 2):
        ligne = ""
        for x in range(min_x - 1, max_x + 2):
            ligne += " O " if (x, y) in monde else " . "
        lignes.append(ligne)
    
    return "\n".join(lignes)

def nettoyer_ecran():
    os.system('cls' if os.name == 'nt' else 'clear')

#  Tests Fonctionnels 

def executer_test(nom_test: str, condition: bool):
    if condition:
        print(f"[SUCCÈS] {nom_test}")
    else:
        print(f"[ÉCHEC]  {nom_test} - La logique est incorrecte.")

def lancer_les_tests():
    print("--- Démarrage des tests unitaires ---")

    # Test 1 : Une cellule seule meurt (sous-population)
    monde_seul = {(0, 0)}
    executer_test(
        "Cellule isolée meurt", 
        generation_suivante(monde_seul) == set()
    )

    # Test 2 : Le bloc (structure stable) reste identique
    bloc = {(0, 0), (0, 1), (1, 0), (1, 1)}
    executer_test(
        "Le bloc reste stable", 
        generation_suivante(bloc) == bloc
    )

    # Test 3 : Le clignotant (oscillateur) change d'état
    ligne = {(0, -1), (0, 0), (0, 1)}
    colonne = {(-1, 0), (0, 0), (1, 0)}
    executer_test(
        "Le clignotant oscille (étape 1)", 
        generation_suivante(ligne) == colonne
    )
    executer_test(
        "Le clignotant revient (étape 2)", 
        generation_suivante(colonne) == ligne
    )
    
    print("--- Fin des tests ---\n")
    time.sleep(2)

# --- Boucle Principale ---

def demarrer_simulation():
    lancer_les_tests()

    # Initialisation : Un "Planeur" (Glider)
    monde = {
        (0, 1), (1, 2), (2, 0), (2, 1), (2, 2)
    }

    try:
        while True:
            nettoyer_ecran()
            print(formater_monde(monde))
            monde = generation_suivante(monde)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nSimulation arrêtée par l'utilisateur.")

if __name__ == "__main__":
    demarrer_simulation()