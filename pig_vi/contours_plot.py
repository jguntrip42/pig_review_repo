#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 15:27:42 2026

@author: stylesj
"""


import numpy as np
import matplotlib.pyplot as plt


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


T = 100

#define probability
win_prob = np.zeros((T, T, T + 1))

for i in range(T):
    for j in range(T):
        for k in range(T + 1):

            #If already guaranteed win
            if i + k >= T:
                win_prob[i, j, k] = 1.0

            else:
                win_prob[i, j, k] = values[(i, j, k)]
                
print(win_prob.shape)



from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Patch

levels = [0.03, 0.09, 0.27, 0.81]

# Different grey shades
shades = ["0.1", "0.2", "0.3", "0.4"]

fig = plt.figure(figsize=(9, 10))
ax = fig.add_subplot(111, projection="3d")

legend_handles = []

for level, shade in zip(levels, shades):

    # Extract isosurface
    verts, faces, normals, vals = measure.marching_cubes(
        win_prob,
        level=level
    )

    mesh = verts[faces]

    # Surface
    surface = Poly3DCollection(
        mesh,
        facecolor=shade,
        edgecolor="0.15",
        linewidth=0.05,
        alpha=0.65
    )

    ax.add_collection3d(surface)

    # Legend entry
    legend_handles.append(
        Patch(facecolor=shade,
              edgecolor="0.15",
              label=f"{int(level*100)}%")
    )

# Axes formatting
ax.set_xlim(0, T)
ax.set_ylim(0, T)
ax.set_zlim(0, T)

ax.set_xlabel("Player 1 Score (i)")
ax.set_ylabel("Player 2 Score (j)")
ax.set_zlabel("Turn Total (k)")

ax.set_xticks([0, T])
ax.set_yticks([0, T])
ax.set_zticks([0, T])

# View looking along j-axis
ax.view_init(elev=10, azim=175)

ax.grid(False)

# Legend
ax.legend(
    handles=legend_handles,
    title="Winning Probability",
    loc="upper right"
)

ax.set_title("Winning Probability Contours for optimal play")

plt.tight_layout()
plt.show()