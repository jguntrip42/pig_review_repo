#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 15:01:35 2026

@author: guntripj
"""

import numpy as np
from collections import deque


def reachable_k_boundary_cross(policy, j_cross, T):
    """
    Finds the reachable boundary of k for each player score i at a fixed crossection of j
    """
    reachable_boundary = np.full(T, np.nan)

    # Iterate through all player scores
    for i in range(T):

        reachable_k = set([0])
        queue = deque([0])
        while queue:
            k = queue.popleft()

            if k >= T - i:
                continue

            if policy[(i, j_cross, k)] == "hold":
                continue

            for roll in [2, 3, 4, 5, 6]:
                k_new = k + roll

                if i + k_new >= T:
                    reachable_k.add(T - i)
                    continue

                if k_new not in reachable_k:
                    reachable_k.add(k_new)
                    queue.append(k_new)

        if len(reachable_k) > 0:
            reachable_boundary[i] = max(reachable_k)
           
    return reachable_boundary


def reachable_k_boundary(policy, T):
    """
    Finds the reachable boundary of k for each (i,j) intersection
    """
    boundary = np.full((T, T), np.nan)
    # Iterate across all crossections oj j
    for j_cross in range(T):
        reachable_boundary = reachable_k_boundary_cross(policy,j_cross,T)
        # Add each crossection to form the full boundary
        boundary[:, j_cross] = reachable_boundary
    return boundary