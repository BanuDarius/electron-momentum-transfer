## Introduction
This is a C program that calculates the linear momentum transfer caused by multiple laser beams coming from arbitrary directions, to an assembly of electrons, producing a 2D momentum map.
Parallelized with OpenMP.

## Usage
The instalation is as follows:
```
git clone --depth 1 https://github.com/BanuDarius/electron-momentum-transfer/
cd electron-momentum-transfer/
make
python3 auto_compute.py
```
This will automatically compute and render the final momentum transfer heatmaps.

## Examples
<img width="1265" height="1282" alt="_out-2d-heatmap-electromag-yy" src="https://github.com/user-attachments/assets/a2f9334b-4f3f-4ac3-884c-c44a8a479e1d" />
<img width="1234" height="1282" alt="_out-2d-heatmap-errors-yy" src="https://github.com/user-attachments/assets/ea77be0c-66a6-4dbe-8655-7c0080c42452" />
<img width="1264" height="1279" alt="_out-average-errors-y" src="https://github.com/user-attachments/assets/36f9731c-5858-4119-83dd-9f718daca3d6" />

### Note
This README is not ready yet!

## References
[1] Higuera, Adam V., and John R. Cary. "Structure-preserving second-order integration of relativistic charged particle trajectories in electromagnetic fields." Physics of Plasmas 24.5 (2017).
