import math
from uflp import UFLP
from typing import List, Tuple
import random
import itertools
import numpy as np


def solve(problem: UFLP) -> Tuple[List[int], List[int]]:
    
    objecitf=[]
    temp = 100
    cooling_rate = 0.99

    #solution initiale
    best_stations,best_satellites,best_cost=generat_init_solution(problem)
    objecitf.append((best_stations,best_satellites, best_cost))
    for i in range(5000):
        new_sation, new_sattelite,new_cost = local_search(problem, best_stations, temp, cooling_rate,best_cost)
        if new_cost < best_cost:
            if problem.solution_checker(new_sation,new_sattelite):
                best_cost = new_cost
                best_stations = new_sation
                best_satellites = new_sattelite
                objecitf.append((best_stations,best_satellites, best_cost))

        else:
            b_stations,satellite,best_cost=generat_init_solution(problem)
            if problem.solution_checker(b_stations,satellite):
                if (b_stations,satellite, best_cost) not in objecitf:
                    objecitf.append((b_stations,satellite, best_cost))
    #objectif
    best_stations,best_satellites,_=min(objecitf, key=lambda x: x[2])
    return list(best_stations), best_satellites

def generat_init_solution(problem:UFLP):

    main_stations_state = [random.choice([0, 1]) for _ in range(problem.n_main_station)]
    #contrainte sur le fait qu'au moins une station principale doit être ouvert
    if(sum(main_stations_state) == 0):
        main_stations_state[random.randint(0, problem.n_main_station - 1)] = 1
    #indexer les stations principales qui sont ouvertes
    index_main_stations_opened = [i for i, x in enumerate(main_stations_state) if x == 1]

    best_satellites = [random.choice(index_main_stations_opened) for _ in range(problem.n_satellite_station)]

    best_stations = main_stations_state
    cost = problem.calcultate_cost(best_stations, best_satellites)

    return best_stations,best_satellites,cost


def local_search(problem: UFLP, stations, temp, cooling_rate,best_cost):
    
    neighbor_main,neighbor_sattelite = neighbor(problem, stations)
    best_stations = stations
    best_satellites = []
    for permutation in neighbor_main:
        for index,satelite in enumerate(permutation):
            new_cost = problem.calcultate_cost(permutation, neighbor_sattelite[index])
            delta_cost = new_cost - best_cost
            if delta_cost < 0:
                best_stations = permutation
                best_satellites = neighbor_sattelite[index]
                best_cost = new_cost
            elif random.random()< math.exp(-delta_cost / temp):
                best_stations = permutation
                best_satellites = neighbor_sattelite[index]
                best_cost = new_cost
                temp *= cooling_rate
    return best_stations, best_satellites,best_cost

def neighbor(problem: UFLP,stations):
    unique_permutations = set()
    satellite_combinations = []
  
    for station_permutation in itertools.permutations(stations, problem.n_satellite_station):
        if station_permutation not in unique_permutations:
            unique_permutations.add(tuple(station_permutation))
        for perm in unique_permutations:
            index = [i for i, x in enumerate(perm) if x == 1]
            #index_open_cost=index[np.argmin([problem.get_opening_cost(index[j])for j in range(len(index))])]       
            satellite_combinations.append([random.choices(index) for _ in range(problem.n_satellite_station)])

    return list(unique_permutations), satellite_combinations

