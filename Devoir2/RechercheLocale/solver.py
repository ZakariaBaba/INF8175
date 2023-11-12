'''
Zakaria Babahadji (2028025)
NGOUNOU TCHAWE Armel (2238017)
'''
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
    for i in range(1000):
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
