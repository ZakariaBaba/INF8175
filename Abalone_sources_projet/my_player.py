from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError
import random
import math

class MyPlayer(PlayerAbalone):
    """
    Player class for Abalone game.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "bob", time_limit: float=60*15,*args) -> None:
        """
        Initialize the PlayerAbalone instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type,name,time_limit,*args)


    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Function to implement the logic of the player.

        Args:
            current_state (GameState): Current game state representation
            **kwargs: Additional keyword arguments

        Returns:
            Action: selected feasible action
        """
        #TODO
        # [print(*x) for x in current_state.get_rep().get_grid()] 
        # [print(a,b.__dict__) for a,b in current_state.get_rep().env.items()]         
        _,action = self.max_value(current_state)
        return action
    
    def max_value(self, state: GameState, alpha = -math.inf, beta = math.inf, maxDepth = 0):

        if state.is_done():
            return state.get_player_score(self), None
        elif maxDepth == 3:
            return self.heuristic(state), None
        best_value = -math.inf
        best_action = None
        for action in state.get_possible_actions():
            next_state = action.get_next_game_state()
            v,_ = self.min_value(next_state,alpha,beta,maxDepth+1)
            if v > best_value:
                best_value = v
                best_action = action
                alpha = max(alpha,best_value)
            if best_value >= beta:
                return best_value, best_action
        return best_value, best_action

    def min_value(self,state:GameState, alpha = -math.inf, beta = math.inf,maxDepth = 0):
            
        if state.is_done():
            return state.get_player_score(self), None
        elif maxDepth == 3:
            return self.heuristic(state), None
        best_value = math.inf
        best_action = None
        for action in state.get_possible_actions():
            next_state = action.get_next_game_state()
            v,_ = self.max_value(next_state,alpha,beta,maxDepth+1)
            if v < best_value:
                best_value = v
                best_action = action
                beta = min(beta,best_value)
            if best_value <= alpha:
                return best_value, best_action
        return best_value, best_action
    

    def heuristic(self,state: GameState):
        # neighbours = state.get_neighbours(4,0)
        # is_in_board = state.in_hexa(neighbours['right'][1])  
        # print(is_in_board)

        
        score = 0
        for position,piece in state.get_rep().env.items():
            if piece.__dict__['piece_type'] == self.piece_type:    
                neighbours = state.get_neighbours(position[0],position[1])
                for direction,neighbour in neighbours.items():
                    # Verifying if the neighbour is the same color
                    if neighbour and neighbour[0] == self.piece_type and state.in_hexa(neighbour[1]):
                        score += 1
                    # Verifying if the neighbour is not the same color
                    elif neighbour and neighbour[0] != self.piece_type:
                        score += 3
                # Having more pieces near the center is better
                score -= self.euclidean_distance(position,(8,4))
        return score

    def manhattan_distance(self,position1,position2):
        return abs(position1[0]-position2[0]) + abs(position1[1]-position2[1])
    
    def euclidean_distance(self,position1,position2):
        return math.sqrt((position1[0]-position2[0])**2 + (position1[1]-position2[1])**2)