# Notes 

# Required modules: numpy


import numpy as np
from functools import partial
from collections import Counter
import matplotlib.pyplot as plt
import pickle

from pig_strategies_sim import *


# Taken simulation setup from testing the optimal policy against hold_at strategies and adapted for finding reachable states using simulation
np.random.seed(1)
reachable_states = set()

def pig_sim_rs(target_score : int, random_order : bool, strategies : tuple[callable, ...]) -> int:
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
        score_list = list(map(lambda x,y: x+y, score_list, map(play_turn_rs,turn_details)))
        
    # The winner is the one who reaches the target score first, so we choose the leftmost value which is at least the target score
    winning_score_index = (min([i for i in range(len(score_list)) if score_list[i] >= target_score]) + shift_int) % N
    
    return winning_score_index



    
def play_turn_rs(turn_details : tuple[callable,list]) -> int:
    """This function takes the current turn details (composed of the strategy we are playing and the current total score of the relevant player);
    this returns the integer value gained by the strategy in the turn (which of course is random)."""
    
    player_num,strategy,all_scores = turn_details
    current_score = all_scores[player_num]
    
    hold = False
    total_score = 0
    play_hist = []
    
    while hold == False:
        
        opponent_score = all_scores[1-player_num]
        
        score_hist = (tuple(play_hist), current_score, opponent_score, all_scores)
        
        if player_num == 0:
            reachable_states.add((current_score,opponent_score,total_score))
                
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





# Load pickle file with results in it
with open("pig_vi_results.pkl", "rb") as f:
    results = pickle.load(f)

target = results["target"]
states = results["states"]
values = results["values"]
policy = results["policy"]



def random_strategy(score_hist):

    return np.random.random() < 0.68


# Run simulation

T = 100
R = 2000000

opt_strat_1 = optimal_strategy_fact()
rep_results = replications(pig_sim_rs, R, T, False, (opt_strat_1, random_strategy))

# Create the (i,j) space grid for the reachable states
reachable_grid = np.zeros((100,100))
for i,j,k in reachable_states:
    reachable_grid[i,j] = 1

# Save using pickle
with open("rpig_vi/eachable_states.pkl", "wb") as f:
    pickle.dump(reachable_states, f)
print("Saved.")