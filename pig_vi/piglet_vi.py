#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:13:12 2026

@author: guntripj
"""

import numpy as np



def piglet_val_iteration(S,A,P,R,epsilon=0.001):
    
    """S is a list of states;
    A is a list of actions;
    P is the state transition function specifying P(s'|s,a);
    R is a reward function R(s'|s,a);
    gamma is the discount factor fixed to 1 in this case (we care only for eventual win regardless of score);
    epsilon is the maximum difference we consider for a solution for the value map to have converged"""
    

    # Set up accessible actions and states from specified state
    A_valid_dict = {s:{} for s in S}
    S_valid_dict = {s:{} for s in S}
    
    
    for i in range(len(S)):
        for a in A:
            for s_new in S:
                if P(s_new,S[i],a) != 0:
                    A_valid_dict[S[i]] = set(A_valid_dict[S[i]]).union({a})
                    S_valid_dict[S[i]] = set(S_valid_dict[S[i]]).union({s_new})                            
    
    # Q function
    
    def q_func(s,a,val_func):
        """This is now an adapted version of the Q function specifically to exploit the symmetry involved in the game of pig"""
    
        S_new = S_valid_dict[s]
        
        def indx(s_val):
            """Indicator function to control the value (probability of winning) when turn switches to opponent"""
            if s_val == "WIN":
                val = 1
            else:
                if (s_val[0] == s[0] and s_val[1] == s[1] and s_val[2] == (s[2]+1)):
                    val = 1
                else:
                    val = 0
            return val
        
        if (s[0]+s[2]) != target:
            s_new_m = (s[1],s[0]+s[2]*(int(a == "H")),0)
        else:
            s_new_m = (0,0,0) # We set this arbitrarily to ensure the code is well-defined (the opponents state is unimportant if the player can win)
        
        
        q_val = sum([(P(s_new,s,a)*(R(s_new,s,a) + val_func[s_new]*indx(s_new) + (1 - val_func[s_new_m])*(1 - indx(s_new)))) for s_new in S_new])
        
        return q_val
        
    
    val_map = {s:0 for s in S} # Initialise values to be zero for each state
    policy_map = {s:None for s in S} # Initialise empty policy
    val_dict = {s:[val_map[s]] for s in S} # Tracks the values of each state as they are being updated
    
    val_maps = [val_map]
    
    k = 0
    
    
    while (((k < 1) or max([abs(val_maps[-1][s] - val_maps[-2][s]) for s in S])) >= epsilon):
        
        k += 1
        val_map_k = {s:0 for s in S}
        
        # Calculate new value map 
        for s in S:
            
            A_valid = list(A_valid_dict[s]) # Get possible actions

            if A_valid != []: # Update value only with respect to states we can access from s using q function
                val_map_k[s] = max([q_func(s,a,val_maps[-1]) for a in A_valid])
        
        val_maps.append(val_map_k)
        
        for s in S:
            val_dict[s].append(val_map_k[s])
        
    # Calculate updated policy
    for s in S:
        
        A_valid = list(A_valid_dict[s]) # Get possible actions
        
        if A_valid != []: # Update value only of states we can access from s (BR is a terminal state)
            a_index = np.argmax(np.array([q_func(s,a,val_maps[-1]) for a in A_valid]))
            policy_map[s] = A_valid[a_index]


    return policy_map,val_maps[-1],val_dict



