
import numpy as np
import matplotlib.pyplot as plt
import pickle

import os.path

# Load pickle file with results in it
with open(os.path.dirname(__file__) + "/pig_vi_results.pkl", "rb") as f:
    results = pickle.load(f)

T = results["target"]
main_values = results["values"]
main_policy = results["policy"]





# -----------------
# First reachable rule, regarding the max k value a player can obtain in each (i,j) state
def reachable_k_boundary_cross(policy,j_cross):
    """
    Finds the reachable boundary of k for each player score i at a fixed crossection of j
    """
    reachable_boundary = np.full(T, np.nan)
    # Iterate through all player scores
    for i in range(T):
        k = 0
        
        # Iterate while the state isnt winning and the optimal policy says to roll
        while (k < T - i and policy[(i, j_cross, k)] == "roll"):
            # Largest possible increase in k
            k += 6
        reachable_boundary[i] = min(k, T - i)

    return reachable_boundary

def reachable_k_boundary(policy):
    """
    Finds the reachable boundary of k for each (i,j) intersection
    """
    boundary = np.full((T, T), np.nan)
    # Iterate across all crossections oj j
    for j_cross in range(T):
        reachable_boundary = reachable_k_boundary_cross(policy,j_cross=j_cross)
        # Add each crossection to form the full boundary
        boundary[:, j_cross] = reachable_boundary
    return boundary

reachable_boundary = reachable_k_boundary(main_policy)

# ---------------------------------
# Second reachable rule, finding the states the player cannot enter, using a simulation approach
with open("reachable_states.pkl", "rb") as f:
    reachable_states = pickle.load(f)

# -----------------------------------
# Combine to find the reachable states for the whole state space
combined_reachable = np.zeros((T, T, T + 1))
for i in range(T):
    for j in range(T):
        # RULE 1
        k_max = reachable_boundary[i, j]
        if np.isnan(k_max):
            continue
        k_max = int(k_max)
        # Iterate through states under the max value of k
        for k in range(k_max + 1):
            # RULE 2
            if (i, j, k) in reachable_states:
                combined_reachable[i, j, k] = 1
                







# 0 is roll and 1 is hold
decision = np.zeros((T, T, T + 1))

for i in range(T):
    for j in range(T):
        for k in range(T + 1):

            # If current score + turn total reaches target,
            # holding wins immediately.
            if i + k >= T:
                decision[i, j, k] = 1

            else:
                if main_policy[(i, j, k)] == "hold":
                    decision[i, j, k] = 1
                else:
                    decision[i, j, k] = 0







# Determine all states that are to roll again
roll = (decision == 0)
# Mask to remove unreachable states
roll_reachable = roll * (combined_reachable == 1)

# Plot using voxels to show the whole filled volume that are reachable and to roll
fig = plt.figure(figsize=(8, 12))

views = [
    (25, -135, "Figure 3 - View 1"),
    (20,  -45, "Figure 3 - View 2")
]

for n, (elev, azim, title) in enumerate(views, start=1):

    ax = fig.add_subplot(2, 1, n, projection="3d")

    ax.voxels(
        roll_reachable,
        facecolors="0.5",
        edgecolor="k",
        linewidth=0.02
    )

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_zlim(0, 100)

    ax.set_xlabel("Player 1 Score (i)")
    ax.set_ylabel("Player 2 Score (j)")
    ax.set_zlabel("Turn Total (k)")

    ax.set_xticks([0, 100])
    ax.set_yticks([0, 100])
    ax.set_zticks([0, 100])

    ax.view_init(elev=elev, azim=azim)

    ax.grid(False)

    ax.set_box_aspect((1,1,1))

    ax.set_title(title)

plt.tight_layout()

plt.show()









j_cross = 30
Z_full = decision[:, j_cross, :]
# Mask to see only the reachable states
Z_reachable = combined_reachable[:, j_cross, :]

plt.figure(figsize=(8, 5))

# Reachable region highlighted
plt.imshow(Z_reachable.T,origin="lower",cmap="Greys",interpolation="nearest",extent=[0, 100, 0, 100],aspect="auto",alpha=0.5)

# Hold Boundary
plt.contour(Z_full.T,levels=[0.5],colors="black",linewidths=1.2,extent=[0, 100, 0, 100])

# Hold-at-20 reference
plt.axhline(20,linestyle="--",color="black")

plt.xlabel("Player 1 Score (i)")
plt.ylabel("Turn Total (k)")
plt.title(f"Figure 4. Cross-section, opponent score = {j_cross}")
plt.xlim(0, 100)
plt.ylim(0, 50)
plt.show()



