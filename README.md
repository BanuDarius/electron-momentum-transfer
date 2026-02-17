## Introduction
This is a C program that calculates the linear momentum transfer caused by multiple laser beams coming from arbitrary directions, to an assembly of electrons, producing a 2D momentum map.
Parallelized with OpenMP.

## Compilation
The installation is as follows:
```
git clone --depth 1 https://github.com/BanuDarius/electron-momentum-transfer/
cd electron-momentum-transfer/
make
```

If you have an older computer and the program doesn't compile, use:
```
make generic
```

Which will compile for a generic x86 CPU.

### Usage
```
python3 auto_compute.py
```
This will automatically compute and render the final momentum transfer heatmaps.

### Run quick test
To run a quick parameter sweep (1 minute on consumer hardware):
```
python3 -c "import sys; sys.path.append('tests'); from tests.quick_example import run_quick_example; run_quick_example(<num_threads>)
```
And replace `<num_threads>` with the number of threads to be used in the simulation.
### Reproduce examples

In order to reproduce the results from the examples/ directory:
```
python3 -c "import sys; sys.path.append('scripts'); from scripts.examples import run_example; run_example(<num_example>, <num_threads>)"
```

And replace `<num_example>` with the respective example number `(1, 2, 3)`.

## Examples
<img width="1072" height="1078" alt="1_out-2d-heatmap-electromag-yy" src="https://github.com/user-attachments/assets/9be7793a-a5a0-4938-9984-07a3faf16b83" />
<img width="1056" height="1078" alt="1_out-2d-heatmap-errors-yy" src="https://github.com/user-attachments/assets/50f1659c-f66d-4705-893b-606e386e63dc" />
<img width="1061" height="1076" alt="1_out-average-errors-y" src="https://github.com/user-attachments/assets/8ee0470a-6922-493f-868e-413b8adf2fa0" />
<img width="1072" height="1078" alt="2_out-2d-heatmap-electromag-yx" src="https://github.com/user-attachments/assets/4b71dcb1-b0bf-421e-87aa-b0fe3f7c0c73" />
<img width="1056" height="1078" alt="2_out-2d-heatmap-errors-yx" src="https://github.com/user-attachments/assets/620599b2-ebb5-4655-aefa-204000dcdc6f" />
<img width="1061" height="1076" alt="2_out-average-errors-x" src="https://github.com/user-attachments/assets/102a5ed2-c8e3-447c-8548-3f7b053ea589" />

## References
[1] Higuera, Adam V., and John R. Cary. "Structure-preserving second-order integration of relativistic charged particle trajectories in electromagnetic fields." Physics of Plasmas 24.5 (2017).
