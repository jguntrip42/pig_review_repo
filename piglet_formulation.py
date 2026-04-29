from valueiteration import valueiteration_pig

target = 2

S_piglet = []

for pscore in range(target):
    for oscore in range(target):
        max_turn_total = target - pscore
        for turn_total in range(max_turn_total):
            S_piglet.append((pscore, oscore, turn_total))
            
A_piglet = ["roll", "hold"]

def piglet(s, a, V):
    
    pscore, oscore, turn_total = s
    if pscore + turn_total >= target:
        return 1.0

    # Hold logic, update score
    if a == "hold":
        return 1 - V[(oscore, pscore + turn_total, 0)]

    # Roll logic
    if a == "roll":
        return 0.5 * (
            # Tails logic
            (1 - V[(oscore, pscore, 0)]) +
            # Heads logic
            (1.0 if turn_total + 1 >= target - pscore else V[(pscore, oscore, turn_total + 1)]))

pi, V, k, V_hist = valueiteration_pig(S_piglet, A_piglet, piglet, 1e-6)

print("Converged in", k, "iterations\n")

for s in sorted(V):
    print(f"{s} = {V[s]:.3f}")

for s in sorted(pi):
    print(f"{s}: {pi[s]}")