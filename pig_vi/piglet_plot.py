

from pig_vi.piglet_vi import *

piglet_states = [(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,1,0),(1,0,1),(1,1,1),(0,0,2),(0,1,2),"WIN"]
piglet_actions = ["H","F"]

target = 2


def P_piglet(s_new,s,a):
    """Returns probabilities for taking action a in state s and transitioning to state s_new"""
    
    if s != "WIN":
        if a == "F":
            if (s[0] == s_new[0] and s[1] == s_new[1] and s_new[2] == 0): # Case where we obtain tails
                p = 0.5
            elif (s[0] == s_new[0] and s[1] == s_new[1] and (s[2]+1) == s_new[2]): # Case where we obtain heads
                p = 0.5
            else:
                p = 0
        elif a == "H":
            if ((s[0]+s[2]) == s_new[0]) and (s[1] == s_new[1]) and (s_new[2] == 0) and ((s[2]+s[0]) != target): # Case where one holds but doesn't win immediately
                p = 1
            elif ((s[2]+s[0]) == target) and (s_new == "WIN"): # Case where holding will inveitably cause the player to win
                p = 1
            else:
                p = 0
    else:
        p = 0
        
    return p


def R_piglet(s_new,s,a):
    """Returns the reward for performing action a and moving from state s to state s_new"""
    
    if ((s_new == "WIN") and (a == "H") and ((s[2]+s[0]) == target)): # Reward only when player wins
        r = 1
    else:
        r = 0
    
    return r



new_policy,val_map_0,val_dict_0 = piglet_val_iteration(piglet_states,piglet_actions,P_piglet,R_piglet,target,0.00001)

import matplotlib.pyplot as plt

iteration_nums = [i for i in range(1,27,1)]


fig, ax_1 = plt.subplots()

for i in range(0,6):
    ax_1.plot(iteration_nums,val_dict_0[piglet_states[i]],label=str(piglet_states[i]))

plt.xlabel("Iteration Number")
plt.ylabel("Value")
plt.legend(loc="lower right",fontsize="x-small")
plt.show()
