from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError
import math

class MyPlayer(PlayerAbalone):
    """
    Player class for Abalone game.

    Attributes:
        piece_type (str): piece type of the player
    """
    keep=[]
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
        _,action = self.max_value(current_state)
        self.keep.append((_,action))
        compare=self.get_time_limit()-self.get_remaining_time()
                
        if compare>=float(15):
            best=[]
            for act in current_state.get_possible_actions():
                if act in self.keep:
                    best.append(self.keep[self.keep.index(act)])
            if len(best)>0:
                _,action=max(best)
        return action
    
    def max_value(self, state: GameState, alpha = -math.inf, beta = math.inf, maxDepth = 0):

        if state.is_done():
            return state.get_player_score(self), None
        elif maxDepth == 3:
            return self.center_heuristic(state), None
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
            return self.center_heuristic(state), None
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

    def center_heuristic(self,state: GameState):
        
        """
        Function that evaluates the score of a state.
        This heuristic is based on the number of pieces near the center of the board.
        The closer the piece is to the center, the better.
        On the opposite, the pieces on the edge of the board are bad,
        meaning that they will have a negative impact on the score.

        Score placements for player:
            Manhantan Distance from center -> score :
                0 or 1 -> +10
                2 -> +8
                3 -> -4
                4 -> -6

        """
        size = state.get_rep().get_dimensions()
        center = (size[0]//2,size[1]//2)
        score_player = 0
        score_opponent = 0 
        for position,piece in state.get_rep().env.items():
            distance = int(self.manhattan_distance(position,center)/2)
            neighbours = state.get_neighbours(position[0],position[1])
            if piece.__dict__['piece_type'] == self.piece_type:
                score_player += self.score_calc(distance)
                if self.is_alone(neighbours,piece):
                    score_player -= 15
                if not state.in_hexa(position):
                    score_player -= 30
            else:
                score_opponent += self.score_calc(distance)
                if self.is_alone(neighbours,piece):
                    score_opponent += 15
                if not state.in_hexa(position):
                    score_opponent += 30
        facteurScore = 50
        for player in state.get_players():
            if player.get_id() == state.get_next_player().get_id():
                score_player += facteurScore * state.get_player_score(player)
            else:
                score_opponent -= facteurScore * state.get_player_score(player)
        return score_player - score_opponent
        

    def is_alone(self,neighbours, piece):
        for neighbour in neighbours.values():
            if neighbour and neighbour[0] == piece.get_type():
                return False
        return True
    
    def score_calc(self,distance):
        score_list = {0:10,1:10,2:8,3:-4,4:-6}
        return score_list[distance]
    def manhattan_distance(self,position1,position2):
        return abs(position1[0]-position2[0]) + abs(position1[1]-position2[1])
    
    def euclidean_distance(self,position1,position2):
        return math.sqrt((position1[0]-position2[0])**2 + (position1[1]-position2[1])**2)