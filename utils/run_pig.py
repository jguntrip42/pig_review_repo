from pig import Pig
import pickle 

game = Pig(target=100)
game.value_iteration(tolerance=1e-6, max_iterations=10000)

print("Pig target:", game.target)
print("Value at (0, 0, 0):", game.get_value(0, 0, 0))
print("Policy at (0, 0, 0):", game.get_policy(0, 0, 0))


results = {"target": game.target,"states": game.states,"values": game.values, "policy": game.policy}
with open("pig_review_repo/pig_policy_results.pkl", "wb") as f:
    pickle.dump(results, f)
print("Results saved.")



# ------------------
# Example load file
import pickle

# Load pickle file
with open("pig_results.pkl", "rb") as f:
    results = pickle.load(f)

target = results["target"]
states = results["states"]
values = results["values"]
policy = results["policy"]

print("Value at (0, 0, 0):",values[(0, 0, 0)])
print("Policy at (0, 0, 0):",policy[(0, 0, 0)])
