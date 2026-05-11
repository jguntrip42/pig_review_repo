#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:13:12 2026

@author: guntripj
"""

import numpy as np


# I think the problem in this version is that there is no losing state

def val_iteration(S,A,P,R,epsilon=0.001):
    
    """S is a list of states;
    A is a list of actions;
    P is the state transition function specifying P(s'|s,a);
    R is a reward function R(s'|s,a);
    gamma is the discount factor fixed to 1 in this case (larger value means we prioritise exploration over exploitation);
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
            s_new_m = (0,0,0)
        
        
        q_val = sum([(P(s_new,s,a)*(R(s_new,s,a) + val_func[s_new]*indx(s_new) + (1 - val_func[s_new_m])*(1 - indx(s_new)))) for s_new in S_new])
        
        return q_val
        
    
    val_map = {s:0 for s in S}
    policy_map = {s:None for s in S}
    val_dict = {s:[val_map[s]] for s in S}
    
    val_maps = [val_map]
    
    k = 0
    
    
    while (((k < 1) or max([abs(val_maps[-1][s] - val_maps[-2][s]) for s in S])) >= epsilon):
        
        k += 1
        val_map_k = {s:0 for s in S}
        
        # Calculate new value map 
        for s in S:
            
            A_valid = list(A_valid_dict[s]) # Get possible actions

            if A_valid != []: # Update value only with respect to states we can access from s
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



from functools import partial
from itertools import product


piglet_states = [(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,1,0),(1,0,1),(1,1,1),(0,0,2),(0,1,2),"WIN"]
piglet_actions = ["H","F"]

target = 2



def P_piglet(s_new,s,a):
    
    if s != "WIN":
        if a == "F":
            if (s[0] == s_new[0] and s[1] == s_new[1] and s_new[2] == 0) or (s[0] == s_new[0] and s[1] == s_new[1] and (s[2]+1) == s_new[2]):
                p = 0.5
            else:
                p = 0
        elif a == "H":
            if ((s[0]+s[2]) == s_new[0]) and (s[1] == s_new[1]) and (s_new[2] == 0) and ((s[2]+s[0]) != target):
                p = 1
            elif ((s[2]+s[0]) == target) and (s_new == "WIN"):
                p = 1
            else:
                p = 0
    else:
        p = 0
        
    return p


def R_piglet(s_new,s,a):
    
    # We want to reward only winning, so set reward to 1 for all transitions from nonwinning states to winning states, and zero for all others
    
    if ((s_new == "WIN") and (a == "H") and ((s[2]+s[0]) == target)): # Reward only when current player wins (swap the indices in the triple)
        r = 1
    else:
        r = 0
    
    return r

new_policy,val_map_0,val_dict_0 = val_iteration(piglet_states,piglet_actions,P_piglet,R_piglet,epsilon=0.0001)


import matplotlib.pyplot as plt



iteration_nums = [i for i in range(1,21,1)]


fig, ax_1 = plt.subplots()

for i in range(0,6):
    ax_1.plot(iteration_nums,val_dict_0[piglet_states[i]],label=str(piglet_states[i]))

plt.xlabel("Iteration Number")
plt.ylabel("Value")
plt.legend(loc="lower right",fontsize="x-small")
plt.show()


