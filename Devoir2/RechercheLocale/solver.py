'''
Zakaria Babahadji (2028025)
NGOUNOU TCHAWE Armel (2238017)
'''
from uflp import UFLP
from typing import List, Tuple
import random


def solve(problem: UFLP) -> Tuple[List[int], List[int]]:
    objecitf=[]
    alpha=500
    #Restarts 500 fois
    for i in range (alpha):
        #Solution initiale
        best_stations,best_satellites,best_cost=generate_init_solution(problem)
        done = True
        time=10000
        while done and time>0:
            done = False
            #Hill climbing Algorithm
            for station_index in range(problem.n_main_station) :
                new_stations,new_satellite=get_neighbor(problem,best_stations, station_index)
                new_cost=problem.calcultate_cost(new_stations,new_satellite)
                if new_cost < best_cost:
                    done = True
                    best_stations = new_stations
                    best_satellites = new_satellite
                    best_cost = new_cost
                    time-=1
        objecitf.append((best_stations,best_satellites,best_cost))      
        #objectif, minimiser le coût autant que possible 
        best_stations,best_satellites,_=min(objecitf, key=lambda x: x[2])
    return best_stations, best_satellites

def generate_init_solution(problem:UFLP):

    main_stations_state = [random.choice([0, 1]) for _ in range(problem.n_main_station)]
    #Contrainte sur le fait qu'au moins une station principale doit être ouvert
    if(sum(main_stations_state) == 0):
        main_stations_state[random.randint(0, problem.n_main_station - 1)] = 1
    #Indexer les stations principales qui sont ouvertes
    index_main_stations_opened = [i for i, x in enumerate(main_stations_state) if x == 1]
    #hypothèse sur la base du coût d'ouverture minimum
    min_cost_open=[(problem.get_opening_cost(val),val) for val in index_main_stations_opened]
    _,choix=min_cost_open[min_cost_open.index(min(min_cost_open))]

    init_satellites = [choix for _ in range(problem.n_satellite_station)]
    init_stations = main_stations_state
    init_cost = problem.calcultate_cost(init_stations, init_satellites)
    
    return init_stations,init_satellites,init_cost

def get_neighbor(problem:UFLP, stations:List[int],index:int):
    #Fonction de voisinnage se basant sur l'ouverture des satelites avec les couts d'association les plus faibles
    neighbor_stations = stations.copy()
    neighbor_stations[index] = 1 - neighbor_stations[index]  
    neighbor_satellite = []
    for satelitte in range(problem.n_satellite_station):
        costs = [problem.get_association_cost(main_station, satelitte) if neighbor_stations[main_station] == 1 else 10000000 for main_station in range(problem.n_main_station)]
        min_cost_main_station = costs.index(min(costs))
        neighbor_satellite.append(min_cost_main_station)
    return neighbor_stations,neighbor_satellite