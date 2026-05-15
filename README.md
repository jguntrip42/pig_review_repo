# Pig Optimal Play Reproduction

**Authors:** Joseph Guntrip, Kyle Russell, Tina Sardashti, Jay Styles

This respository aims to replicate the methodology and results from:  
*"Optimal Play of the Dice Game Pig"* (Neller & Presser, 2004)

---

## Overview:

This respository focuses on the implementation the value iteration algorithm in order to compute the optimal strategy for the dice game *Pig* as well as the simplified version *Piglet*, this is done to reproduce the results of the aforementioned paper, by focusing on reproducing their figures and findings. This includes:
- Computing the optimal policy and through the corresponding value.
- Calculating and visualising the surface between the two possible actions "hold" and "roll".
- Developing ways to reduce the analysed states to remove unreachable states.
- Visualisation of the reachable state policy surface.
- Calculating and visualising the winning proabilities and contours.


---

## Installation and Setup:

To clone the repository:

```bash
git clone https://github.com/jguntrip42/pig_review_repo.git
cd pig_review_repo
```
Install dependencies:

```bash
pip install -r dependencies.txt
```
