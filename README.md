# Pig Optimal Play Reproduction

**Authors:** Joseph Guntrip, Kyle Russell, Tina Sardashti, Jay Styles

This repository aims to replicate the methodology and results from:  
*"Optimal Play of the Dice Game Pig"* (Neller & Presser, 2004)

---

## Overview:

This repository focuses on the implementation the value iteration algorithm in order to compute the optimal strategy for the dice game *Pig* as well as the simplified version *Piglet*, this is done to reproduce the results of the aforementioned paper, by focusing on reproducing their figures and findings. This includes:
- Computing the optimal policy and the corresponding value function.
- Calculating and visualising the surface between the two possible actions "hold" and "roll".
- Developing ways to reduce the analysed states to remove unreachable states.
- Visualisation of the reachable state policy surface.
- Calculating and visualising the winning probabilities and contours.

  The extent of reproducibility is then explored through the use of the principles of the "5Rs" (Benureau and Rougier, 2018), analysing the original work of Neller and Presser through the lens of re-runability, repeatability, reproducibility, replicability and reusability.
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

---

## Repository Layout:

This is a description of files included in the repository. This repository was developed to work alongside the reproducibility study performed and forms a structured layout of the appropriate scripts and documents in order to accurately reproduce our results and highlight the methodology to which the works of Neller and Presser was reproduced by.

```/papers``` - includes the *"Optimal Play of the Dice Game Pig"* (Neller & Presser, 2004) and *"Re-run, Repeat, Reproduce, Reuse, Replicate: Transforming Code into Scientific Contributions"* (Benureau & Rougier, 2018) along with our report on the replication study.

```/pig_vi``` - includes the relevant files containing the executable functions and simulation results in order to reproduce the results in "Optimal Play of the Dice Game Pig".

 ```/plots``` - includes scripts to produce the figures in "Optimal Play of the Dice Game Pig".
 
```/tests``` - includes testing scripts for the application of value iteration to the game of Piglet and Pig.

Running the simulations and value iteration scripts produces:

- `pig_vi_results.pkl`
  - Stored optimal policy and value function for the game of Pig.

- `reachable_states.pkl`
  - Simulation-based reachable states.

- Figure outputs within `/plots`.
---
Main Functions:
The main value-iteration code is in the `/pig_vi` directory.

`piglet_val_iteration(...)` runs value iteration for the simplified Piglet game. It returns the final value map, the optimal policy, and the value history used for the convergence plot.

`Pig` is the class used for the full game of Pig. It creates the state space, computes the values of rolling and holding, runs value iteration, and stores the final optimal policy.

`save_results(T, tol)` runs the full Pig value iteration for target score `T` and tolerance `tol`. It saves the computed values and policy to `pig_vi/pig_vi_results.pkl`.

The plotting and simulation scripts use these saved results to reproduce the figures and numerical comparisons in the report.

---
## Usage

After installing the dependencies, the main scripts can be run to reproduce the value-iteration results, figures, and simulations used in the report.

The Piglet implementation is used as a small validation case. It checks that value iteration recovers the exact values reported by Neller and Presser for target score 2.

The full Pig implementation computes the optimal value function and roll/hold policy for target score 100. These results are then saved and used to generate the policy boundary plots, reachable-state plots, contour plots, and simulation comparisons.

The **Piglet** value iteration can be run as follows:

```python
from pig_vi.piglet_vi import piglet_val_iteration

policy_map, value_map, value_history = piglet_val_iteration(
    S, A, P, R, T=2, epsilon=1e-6)
```

Here, `S`, `A`, `P`, and `R` are the Piglet state list, action list, transition function, and reward function. The function returns the optimal policy, final value map, and convergence history.

The **Pig** value iteration can be run and saved as follows:

```python
from pig_vi.run_pig import save_results

save_results(T=100, tol=1e-8)
```

This saves the computed Pig value function and optimal policy to:

```text
pig_vi_results.pkl
```
---
## Testing:

Unit tests are available to validate the results of the value iteration algorithm applied to the relevant games of Piglet and Pig themselves. Piglet is tested by using a small target score of 2 and tests the correct handling of terminal states, recovery of the expected value assignment and optimal policy. The game of Pig is tested through the use of using previously calculated results and verifying that the recovered policy ascurately matches the stored policy.

The tests can be executed using:

```bash
pytest
```

---

## References

Neller, T. W., & Presser, C. G. (2004).  
*Optimal Play of the Dice Game Pig.*

Benureau, F. C. Y., & Rougier, N. P. (2018).  
*Re-run, Repeat, Reproduce, Reuse, Replicate: Transforming Code into Scientific Contributions.*
