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
        # print(current_state.rep)
            
        _,action = self.max_value(current_state)
        return action
    
    def max_value(self, state: GameState, alpha = -math.inf, beta = math.inf):
        #TODO
        # print(state)

        if state.is_done():
            return state.get_player_score(self), None
        best_value = -math.inf
        best_action = None
        possible_actions = state.generate_possible_actions()
        for action in possible_actions:
            next_state = action.get_next_game_state()
            v,_ = self.min_value(next_state,alpha,beta)
            # print(v)
            if v > best_value:
                # print('v :' + str(v))
                # print('v* : ' + str(best_value))
                # print(action)
                best_value = v
                best_action = action
                alpha = max(alpha,best_value)
            if best_value >= beta:
                return best_value, best_action
        return best_value, best_action

    def min_value(self,state:GameState, alpha = -math.inf, beta = math.inf):
            
        if state.is_done():
            # print(state.get_player_score(self))
            return state.get_player_score(self), None
        best_value = math.inf
        best_action = None
        possible_actions = state.generate_possible_actions()
        for action in possible_actions:
            next_state = action.get_next_game_state()
            v,_ = self.max_value(next_state,alpha,beta)
            if v < best_value:
                best_value = v
                best_action = action
                beta = min(beta,best_value)
            if best_value <= alpha:
                return best_value, best_action
        return best_value, best_action