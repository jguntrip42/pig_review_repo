from pig import Pig

game = Pig(target=100)
game.value_iteration(tolerance=1e-6, max_iterations=10000)

print("Pig target:", game.target)
print("Value at (0, 0, 0):", game.get_value(0, 0, 0))
print("Policy at (0, 0, 0):", game.get_policy(0, 0, 0))