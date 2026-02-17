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
<img width="1072" height="1078" alt="2_out-2d-heatmap-electromag-yy" src="https://github.com/user-attachments/assets/5e353c1e-afe2-46d1-8671-dda3d4f7b000" />
<img width="1048" height="1078" alt="2_out-2d-heatmap-errors-yy" src="https://github.com/user-attachments/assets/5a4478af-e259-4b54-821d-ec557ef03e57" />
<img width="1072" height="1078" alt="1_out-2d-heatmap-electromag-yy" src="https://github.com/user-attachments/assets/156deeb0-b06e-4a04-9105-776a7ff9369d" />
<img width="1059" height="1076" alt="1_out-average-errors-y" src="https://github.com/user-attachments/assets/0e2f3c96-7aa8-4020-9953-cd7eece8bcb0" />

## References
[1] Higuera, Adam V., and John R. Cary. "Structure-preserving second-order integration of relativistic charged particle trajectories in electromagnetic fields." Physics of Plasmas 24.5 (2017).
