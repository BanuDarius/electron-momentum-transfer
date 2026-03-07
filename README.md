## Introduction
This is a C program that calculates the linear momentum transfer caused by multiple laser beams coming from arbitrary directions, to an assembly of electrons, producing a 2D momentum map.
Parallelized with OpenMP.

## Compilation
The installation is as follows:
```
git clone --depth 1 https://github.com/BanuDarius/electron-momentum-transfer
cd electron-momentum-transfer/
cmake -B build -S .
cmake --build build
```

If you have an older computer and the program doesn't compile, use:
```
cmake -B build -S . -DGENERIC=ON
cmake --build build
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

## Gallery
<img width="1072" height="1078" alt="1_out-2d-heatmap-electromag-yy" src="https://github.com/user-attachments/assets/9be7793a-a5a0-4938-9984-07a3faf16b83" />
<img width="1056" height="1078" alt="1_out-2d-heatmap-errors-yy" src="https://github.com/user-attachments/assets/50f1659c-f66d-4705-893b-606e386e63dc" />
<img width="2147" height="2158" alt="_out-2d-heatmap-electromag-xy" src="https://github.com/user-attachments/assets/6848d32b-2676-467e-9d53-9f75aa6dd72b" />
<img width="2115" height="2158" alt="_out-2d-heatmap-errors-xy" src="https://github.com/user-attachments/assets/d5495d2d-7e0f-4479-8370-483b5ef522cd" />
<img width="2115" height="2158" alt="_out-2d-heatmap-errors-xx" src="https://github.com/user-attachments/assets/492e1f95-70cb-448c-a0cf-85e120a8e6ab" />
<img width="2124" height="2156" alt="_out-average-errors-x" src="https://github.com/user-attachments/assets/7417622b-7c2f-4ba3-b2c0-84dd7edfa005" />

## Performance
<img width="2147" height="1771" alt="_out-performance" src="https://github.com/user-attachments/assets/a207fe88-fa66-461f-9d62-b21125465cea" />
This performance test was made on a system consisting of 2x AMD EPYC 7713 64-core processors.

## References
[1] Higuera, Adam V., and John R. Cary. "Structure-preserving second-order integration of relativistic charged particle trajectories in electromagnetic fields." Physics of Plasmas 24.5 (2017).
