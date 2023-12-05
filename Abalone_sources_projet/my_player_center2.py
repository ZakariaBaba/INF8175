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
        #Time management 
        compare=self.get_time_limit()-self.get_remaining_time()
        
        #Choose the action following the high cost after half 70 time
        if compare>=float(70):
            info='N'
            best=[]
            for act in current_state.get_possible_actions():
                
                for a in self.keep:
                    if act in a:
                        info='Y'
                        best.append(self.keep[self.keep.index(a)])
            if len(best)>3 and info=='Y':
                _, action = max(best, key=lambda x: x[0])
        
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
        Bad_position = ((0,4),(3,1), (2,2), (1,3), (4,0),(6,0),(1,5),(8,0), (2,6),(10,0),  (3,7),
        (12,0),(4,8),(13,1),  (6,8),(14,2), (8,8),(15,3),(10,8),(16,4), (15,5), (14,6), (13,7), (12,8))
        
        Good_position= ((6,2), (5,3), (4,4), (8,2), (7,3), (6,4), (5,5),
            (10,2), (9,3), (8,4), (7,5), (6,6), (11,3), (10,4),(8,6), (12,4),(11,5),(10,6))
        for position,piece in state.get_rep().env.items():
            distance = int(self.manhattan_distance(position,center)/2)
            neighbours = state.get_neighbours(position[0],position[1])
            if piece.__dict__['piece_type'] == self.piece_type:
                score_player += self.score_calc(distance)
                for po in position:
                    if po in Bad_position:
                       
                        score_player -=7
                    elif po in Good_position:
                        
                        score_player +=7
                if self.is_alone(neighbours,piece):
                    score_player -= 15
                if not state.in_hexa(position):
                    score_player -= 30
            else:
                for po in position:
                    if po in Bad_position:
                       
                        score_opponent -=7
                    elif po in Good_position:
                        
                        score_opponent +=7
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