from typing import Any, Callable

def valueiteration_pig(S: list[Any], A: list[Any], Q: Callable,threshold: float, maxiters: int = 1000):

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
                
                v = Q(s, a, V)

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

