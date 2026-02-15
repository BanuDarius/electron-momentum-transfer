## Introduction
This is a C program that calculates the linear momentum transfer caused by multiple laser beams coming from arbitrary directions, to an assembly of electrons, producing a 2D momentum map.
Parallelized with OpenMP.

## Usage
The installation is as follows:
```
git clone --depth 1 https://github.com/BanuDarius/electron-momentum-transfer/
cd electron-momentum-transfer/
make
python3 auto_compute.py
```
This will automatically compute and render the final momentum transfer heatmaps.

## Reproduce examples
In order to reproduce the results from the examples/ directory, run this command:
```
python -c "import sys; sys.path.append('scripts'); from scripts.examples import run_example; run_example(<num_example>, <num_threads>)"
```
And replace `<num_example>` with the respective example number `(1, 2, 3...)`, and `num_threads` with the number of threads to be used in the simulation.

## Examples
<img width="2143" height="2155" alt="_out-2d-heatmap-electromag-yy" src="https://github.com/user-attachments/assets/35a51f1a-d56a-4e27-afee-275067766dfa" />
<img width="2143" height="2155" alt="_out-2d-heatmap-electromag-yx" src="https://github.com/user-attachments/assets/dda0d6b3-5b19-44f2-8145-1092c0e30c51" />
<img width="1234" height="1282" alt="_out-2d-heatmap-errors-yy" src="https://github.com/user-attachments/assets/ea77be0c-66a6-4dbe-8655-7c0080c42452" />
<img width="2153" height="2154" alt="_out-max-py-electromag" src="https://github.com/user-attachments/assets/2513b091-ada2-4326-bb59-89393373db75" />

### Note
This README is not ready yet!

## References
[1] Higuera, Adam V., and John R. Cary. "Structure-preserving second-order integration of relativistic charged particle trajectories in electromagnetic fields." Physics of Plasmas 24.5 (2017).
