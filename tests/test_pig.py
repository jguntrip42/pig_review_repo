#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 09:36:38 2026

@author: guntripj
"""

from pig_vi.pig import *
import pickle


def test_pig():
    """Checks we obtain the correct policy for the value iteration algorithm for Pig"""

    # Load pickle file with results in it
    with open("pig_vi_results.pkl", "rb") as f:
        results = pickle.load(f)
    
    main_policy = results["policy"]
    
    game = Pig(target=100)
    game.value_iteration(tolerance=1e-6, max_iterations=10000, print_its=True)
    
    assert game.policy == main_policy
    

