#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 16:48:42 2026

@author: guntripj
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle

import os.path


with open(os.path.pardir+"/pig_vi/pig_vi_results.pkl", "rb") as f:
    pig_policy = pickle.load(f)["policy"]

T = 100

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
                if pig_policy[(i, j, k)] == "hold":
                    decision[i, j, k] = 1
                else:
                    decision[i, j, k] = 0

print(decision.shape)

from skimage import measure # Note skimage requires the scikit-image package

verts, faces, normals, values = measure.marching_cubes(decision, level=0.5)


from mpl_toolkits.mplot3d.art3d import Poly3DCollection

mesh = verts[faces]

fig = plt.figure(figsize=(8, 12))

views = [
    (25, -135, "Figure 3 - View 1"),
    (20,  -45, "Figure 3 - View 2")
]

for n, (elev, azim, title) in enumerate(views, start=1):
    ax = fig.add_subplot(2, 1, n, projection="3d")

    surface = Poly3DCollection(
        mesh,
        facecolor="0.55",
        edgecolor="0.25",
        linewidth=0.03
    )

    ax.add_collection3d(surface)

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
    ax.set_title(title)

plt.tight_layout()
plt.show()