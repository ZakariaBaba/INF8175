from uflp import UFLP
from typing import List, Tuple
import random


def solve(problem: UFLP) -> Tuple[List[int], List[int]]:
    """
    Votre implementation, doit resoudre le probleme via recherche locale.

    Args:
        problem (UFLP): L'instance du probleme à résoudre

    Returns:
        Tuple[List[int], List[int]]: 
        La premiere valeur est une liste représentant les stations principales ouvertes au format [0, 1, 0] qui indique que seule la station 1 est ouverte
        La seconde valeur est une liste représentant les associations des stations satellites au format [1 , 4] qui indique que la premiere station est associée à la station pricipale d'indice 1 et la deuxieme à celle d'indice 4
    """
    "Fonction de Voisinage : N(s): S->2^S"
    "Fonction de validite : L(N(s), s) : 2S × S → 2S"
    "Fonction de selection : Q(L(N(s), s), s) : 2S × S → S"
    "Fonction de cout : f : S → R"
    "Fonction de recherche locale : s0 ∈ S, s ∈ S, s0 ← s"
    
    #Solution initiale
    main_stations_opened = [random.choice([0, 1]) for _ in range(problem.n_main_station)]
    satellite_station_association = [0 for _ in range(problem.n_satellite_station)]

    best_stations = main_stations_opened
    best_association = satellite_station_association
    best_cost = problem.calcultate_cost(best_stations, best_association) 

    for _ in range(100000):
        neighbor_main,neighbor_sattelite = neighbor(problem, best_stations, best_association)
        if neighbor_main is None or neighbor_sattelite is None:
            continue

        neighbor_cost = evaluate(problem,neighbor_main, neighbor_sattelite)
        if neighbor_cost < best_cost:
            best_stations = neighbor_main
            best_association = neighbor_sattelite
            best_cost = neighbor_cost

    for association in best_association:
        if best_stations[association] == 0:
            best_stations[association] = 1
    return best_stations, best_association

def neighbor(problem: UFLP, current_main_stations_opened: List[int], current_satellite_assignments:List[int]) -> Tuple [List[int],List[int]]:
    
    i = random.randint(0, problem.n_main_station - 1)
    j = random.randint(0, problem.n_main_station - 1)
    new_main_station1 = random.randint(0, problem.n_main_station - 1)
    new_main_station2 = random.randint(0, problem.n_main_station - 1)

    current_main_stations_opened[i] = 1
    current_main_stations_opened[j] = 0
    current_satellite_assignments[new_main_station1] = j
    current_satellite_assignments[new_main_station2] = i
    
    return current_main_stations_opened,current_satellite_assignments

def evaluate(problem: UFLP, current_main_stations_opened: List[int], current_satellite_assignments:List[int]):
    cost = 0
    for index,main_station in enumerate(current_main_stations_opened):
        if main_station == 1:
            cost+=problem.get_opening_cost(index)
            for index_satellite,satellite_station in enumerate(current_satellite_assignments):
                if satellite_station == index:
                    cost+=problem.get_association_cost(index,index_satellite)
    return cost
