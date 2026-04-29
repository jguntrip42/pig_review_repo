from collections.abc import Callable
from typing import Any
from functools import lru_cache

def valueiteration(S:list[Any], A:list[Any], P:Callable, R:Callable, threshold:float, gamma:float, maxiters:int=100) -> tuple[dict[Any, Any], dict[Any, float], int, list[dict[Any, float]]]:
    '''
    Value iteration algorithm (synchronous) for Markov Decision Processes.

    Parameters
    ----------
    S : list
        set of states
    A : list
        set of actions
    P : function
        state transition function
    R : function
        reward function
    threshold : float
        threshold at which differeence between iterations terminates the loop
    gamma : float
        discount factor, between 0.0 and 1.0
    maxiters : integer
        maximum number of iterations
        
    Returns
    -------
    pi : dict
        optimal policy
    V : dict
        Value function
    k : integer
        num of iterations for congergence
    V_hist : list 
        history of value function over iterations
    '''
    
    # Add assurances to that the function doesnt break
    if not (0 < gamma <= 1): 
        raise ValueError("gamma must be between 0.0 and 1.0")
    if not (threshold > 0):
        raise ValueError("threshold must be positive")
    if not (len(S) > 0):
        raise ValueError("S must have some states")
    if not (len(A) > 0):
        raise ValueError("A must have some actions")

    @lru_cache(maxsize=None)
    def P_cached(s_next, s, a):
        return P(s_next, s, a)
    
    @lru_cache(maxsize=None)
    def R_cached(s, a):
        return R(s, a)

    # Intitialise two dictionaries for the current and last iteration's values
    V = {s: 0.0 for s in S}
    V_update = {s: 0.0 for s in S}

    # Initialise iteration counter
    k = 0
    # Setup delta value to arbitrarily large
    delta = float("inf")
    # Initialise policy dictionary
    pi = {}
    # Create Value history  
    V_hist = [V.copy()]
    
    # Termination conditions
    while delta > threshold and k < maxiters:
        delta = 0.0
        # Iteration counter
        k += 1
        # Iterate for each possible state
        for s in S:
            # Initialise best value and action to nothing
            best_v = float("-inf")
            best_a = None
            
            # Iterate for each possible action
            for a in A:
                # Account for terminal states, where probability is zero
                if all(P_cached(s_next, s, a) == 0.0 for s_next in S):
                    continue

                # Calculate expected value from future states, now using map function 
                exp_v = sum(map(lambda s_next: P_cached(s_next, s, a) * V[s_next], S))
                
                # Update value
                v = R_cached(s, a) + gamma * exp_v
                
                # Update best value found from best action
                if v > best_v:
                    best_v = v
                    best_a = a
                    
            # Store best value and action for that stat, accounting for terminal states
            if best_a is None:
                V_update[s] = V[s]
            else:
                V_update[s] = best_v
            pi[s] = best_a
            
            # Update delta with largest change between iterations
            delta = max(delta, abs(V_update[s] - V[s]))
        
        
        # Update value with the new iteration's value
        V = V_update.copy()
        # Store value history
        V_hist.append(V.copy())
    
    # Termination due to max number of iterations warning
    if delta > threshold:
        print("Maximum number of iterations reached")

    return pi, V, k, V_hist