

def save_results(T,tol):
    
    from pig_vi.pig import Pig
    import pickle 

    game = Pig(target=T)
    game.value_iteration(tolerance=tol, max_iterations=10000, print_its=True)
    
    
    print("Pig target:", game.target)
    print("Value at (0, 0, 0):", game.get_value(0, 0, 0))
    print("Policy at (0, 0, 0):", game.get_policy(0, 0, 0))
    
    
    results = {"target": game.target,"states": game.states,"values": game.values, "policy": game.policy}
    with open("pig_vi/pig_vi_results.pkl", "wb") as f:
        pickle.dump(results, f)
    print("Results saved.")

