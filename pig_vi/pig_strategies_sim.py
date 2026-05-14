
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 11:39:57 2026

@author: guntripj
"""


# Notes 

# Required modules: numpy


import numpy as np

from functools import partial
from collections import Counter


import pickle



np.random.seed(1)


def pig_sim(target_score : int, random_order : bool, strategies : tuple[callable, ...]) -> int:
    """The argument strategies should be a tuple of functions representing different strategies, which return True to continue rolling and False to hold;
    target_score is the integer value a strategy must exceed first for it to win;
    random_order is a boolean value which when true will shuffle the strategies before simulation;
    note that the order the strategies are passed in is significant: this function returns the index of the winning strategy as in the tuple passed as argument."""
    
    shift_int = 0
    N = len(strategies)
    
    # Section allow for random "starting" player, shifts the order of strategies by a random integer
    # (Note that we do not need to totally randomise the order of players, only the player who goes first, since we assume turns are independent)
    if random_order == True:
        shift_int = int(np.random.randint(0,N)) # Choose random integer to represent strategy to begin round with
        ord_strategies = strategies[shift_int:] + strategies[:shift_int]
    
    else:
        ord_strategies = strategies
        
    
    score_list = [0]*N
    
    while all([(score < target_score) for score in score_list]):
        
        turn_details = zip(list(range(0,N)), ord_strategies,[score_list]*N)
        score_list = list(map(lambda x,y: x+y, score_list, map(play_turn,turn_details)))
        
    # The winner is the one who reaches the target score first, so we choose the leftmost value which is at least the target score
    winning_score_index = (min([i for i in range(len(score_list)) if score_list[i] >= target_score]) + shift_int) % N
    
    return winning_score_index



    
def play_turn(turn_details : tuple[callable,list]) -> int:
    """This function takes the current turn details (composed of the strategy we are playing and the current total score of the relevant player);
    this returns the integer value gained by the strategy in the turn (which of course is random)."""
    
    player_num,strategy,all_scores = turn_details
    current_score = all_scores[player_num]
    
    hold = False
    total_score = 0
    play_hist = []
    
    while hold == False:
        
        score_hist = (tuple(play_hist),current_score,all_scores)
        
        if strategy(score_hist) == True:
            
            val = roll_dice() # Get result from simulated dice roll
            play_hist.append(val) # Update history of dice rolls
            
            if val == 1: # End turn if a 1 is rolled
                total_score = 0
                hold = True
                break
            else:
                total_score += val
                
        elif strategy(score_hist) == False:
            hold = True
            
    return total_score


def roll_dice() -> int:
    return np.random.randint(1,7)


def strategy_factory_1(M : int,target_score : int) -> callable:

    def strat_hold(score_hist : tuple[tuple,int]) -> bool:
        """" The argument score_hist is a tuple where the first element is the previous rolls in the turn and the second element is the players overall score so far;
        this strategy chooses to continue rolling until a total of at least M has been rolled in a single turn (or we exceed the target score)."""
        
        play_hist, current_score, all_scores = score_hist
        turn_score = sum(play_hist) 
        
        # Check if we've reached the threshold M or exceeded the required overall target score
        if (turn_score >= M) or (turn_score + current_score >= target_score): # Hold if we obtain more than M in the turn or if the total score is at least the target score
            return False
        else:
            return True
    
    strat_hold.__name__ = "strat_hold_at_"+str(M)

    return strat_hold



# Load pickle file
with open("pig_vi_results.pkl", "rb") as f:
    results = pickle.load(f)

target = results["target"]
states = results["states"]
values = results["values"]
policy = results["policy"]

def optimal_strategy_fact() -> callable:

    def strat_opt(score_hist : tuple[tuple,int]) -> bool:
        """Rolls and holds in accordance with the optimal strategy; 
        note that this strategy is only suitable for two player games and when the target score is exactly 100"""
        
        
        play_hist, current_score, all_scores = score_hist
        turn_score = sum(play_hist) 
        opponents_score = all_scores[1-all_scores.index(current_score)] # Note the 1- switches the index of the player to the opponent when there are two players
        
        if (turn_score + current_score) >= 100:
            val = False
        else:
            if policy[(current_score,opponents_score,turn_score)] == 'roll':
                val = True
            else:
                val = False
                
        return val
    
    strat_opt.__name__ = "opt_strat"

    return strat_opt



def replications(sim_func : callable, N : int, target_score : int, randomiser : bool, strategies : tuple[callable, ...]) -> dict:
    """N is the number of replications;
    runs replications of rounds with all the strategies passed in as arguments, randomising the starting player;
    allows for repeated strategies (i.e. strategies can be a tuple of functions pointing to the same underlying function);
    the randomiser will randomly change the starting player in each round."""
    
    plays = [strategies] * N
    part_sim_func = partial(sim_func,target_score,randomiser) # Fixes a simulation type with specific parameters
    
    results = list(map(part_sim_func,plays))
    count_dict = Counter(results)
    
    summary_dict = dict()
    
    # Convert numbers to percentages and format for presenting in dictionary
    for i in range(len(strategies)):
        key = 'S'+str(i+1)+' '+'(' + strategies[i].__name__ + ')'
        summary_dict[key] = 100 * count_dict[i] / N 
    
    return summary_dict
    

