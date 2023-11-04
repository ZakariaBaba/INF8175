import math
from uflp import UFLP
from typing import List, Tuple
import random
import itertools


def solve(problem: UFLP) -> Tuple[List[int], List[int]]:

    temp = 100
    cooling_rate = 0.99
    
    #Solution initiale
    main_stations_opened = [random.choice([0, 1]) for _ in range(problem.n_main_station)]
    if(sum(main_stations_opened) == 0):
        main_stations_opened[random.randint(0, problem.n_main_station - 1)] = 1
    index = [i for i, x in enumerate(main_stations_opened) if x == 1]
    best_satellites = [random.choice(index) for _ in range(problem.n_satellite_station)]
    best_stations = main_stations_opened
    best_cost = problem.calcultate_cost(best_stations, best_satellites)


    for i in range(5000):
        new_sation, new_sattelite = local_search(problem, best_stations, temp, cooling_rate,best_cost)
        new_cost = problem.calcultate_cost(best_stations, best_satellites)
        if new_cost < best_cost:
            best_cost = new_cost
            best_stations = new_sation
            best_satellites = new_sattelite
        i+=1
    return best_stations, best_satellites

def local_search(problem: UFLP, stations, temp, cooling_rate,best_cost):
    
    neighbor_main,neighbor_sattelite = neighbor(problem, stations)
    best_stations = stations
    best_satellites = []
    for permutation in neighbor_main:
        for index,satelite in enumerate(permutation):
            new_cost = problem.calcultate_cost(permutation, neighbor_sattelite[index])
            delta_cost = new_cost - best_cost
          
            if delta_cost < 0  or random.random()< math.exp(-delta_cost / temp) :
                best_stations = permutation
                best_satellites = neighbor_sattelite[index]
                best_cost = new_cost
            # if new_cost < best_cost:
            #     best_cost = new_cost
            #     best_stations = permutation
            #     best_satellites = neighbor_sattelite[index]
        temp *= cooling_rate
    return best_stations, best_satellites

def neighbor(problem: UFLP,stations):
    unique_permutations = set()
    satellite_combinations = []
    # if(len(stations) <=10):
    #     for perm in itertools.permutations(stations, len(stations)):
    #         if perm not in unique_permutations:
    #             unique_permutations.add(perm)
    #     for perm in unique_permutations:
    #         index = [i for i, x in enumerate(perm) if x == 1]
    #         satellite_combinations.append([random.choice(index) for _ in range(problem.n_satellite_station)])
    #     return list(unique_permutations),satellite_combinations
    # else:
    for _ in range(1000):  
        station_permutation = next(itertools.permutations(stations, len(stations)))
        if station_permutation not in unique_permutations:
            unique_permutations.add(tuple(station_permutation))
        for perm in unique_permutations:
            index = [i for i, x in enumerate(perm) if x == 1]
            satellite_combinations.append([random.choice(index) for _ in range(problem.n_satellite_station)])

    return list(unique_permutations), satellite_combinations

