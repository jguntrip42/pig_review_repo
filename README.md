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
This project was developed using:
- Python 3.12

## Repository Layout:

This is a description of files included in the repository. This repository was developed to work alongside the reproducability study performed and forms a structured layout of the appropriate scripts and documents in order to accurately reproduce our results and highlight the methodology to which the works of Neller and Presser was reproduced by.

```/papers``` - includes the *"Optimal Play of the Dice Game Pig"* (Neller & Presser, 2004) and *"Re-run, Repeat, Reproduce, Reuse, Replicate: Transforming Code into Scientific Contributions"* (Benureau & Rougier, 2008) along with our report on the replication study.

```/pig_vi``` - includes the relevant files containing the executable functions and simulation results in order to reproduce the results in "Optimal Play of the Dice Game Pig".

 ```/plots``` - includes scripts to produce the figures in "Optimal Play of the Dice Game Pig".
 
```/tests``` - includes testing scripts for the application of value iteration to the game of Piglet and Pig.

Running the simulations and value iteration scripts produces:

- `pig_vi_results.pkl`
  - Stored optimal policy and value function for the game of Pig.

- `reachable_states.pkl`
  - Simulation-based reachable states.
    
## Testing:

Unit tests are available to validate the results of the value iteration algorithm applied to the relevant games of Piglet and Pig themselves. Piglet is tested by using a small target score of 2 and tests the correct handling of terminal states, recovery of the expected value assignment and optimal policy. The game of Pig is testd through the use of using perviously calculated results and verifying that the recovered policy acurately matches the stored policy.

The tests can be executed using:

```bash
pytest
```


