## Introduction
This is a program which computes the linear momentum transfer to electrons interacting with plane wave laser beams, using both the Lorentz force formalism and the relativistic ponderomotive approximation. Its main purpose is creating visual representations of the final momentum distribution for the particle ensemble, and calculating the errors between the two methods.

## Compilation
The installation is as follows:
```
git clone --depth 1 https://github.com/BanuDarius/electron-momentum-transfer
cd electron-momentum-transfer/
cmake -B build
cmake --build build
```

If you have an older computer and the program doesn't compile, use:
```
cmake -B build -DGENERIC=ON
cmake --build build
```

Which will compile for a generic x86 CPU.

To remove the previously generated output data (images, videos), use:
```
cmake --build build --target clean-output
```

### Usage
```
python3 auto_compute.py
```
This will automatically compute and render the final momentum transfer heatmaps for an example scenario.

For more instructions, see `docs/user-manual.pdf`,

## Gallery
<img width="1072" height="1078" alt="1_out-2d-heatmap-electromag-yy" src="https://github.com/user-attachments/assets/9be7793a-a5a0-4938-9984-07a3faf16b83" />
<img width="1056" height="1078" alt="1_out-2d-heatmap-errors-yy" src="https://github.com/user-attachments/assets/50f1659c-f66d-4705-893b-606e386e63dc" />
<img width="2147" height="2158" alt="_out-2d-heatmap-electromag-xy" src="https://github.com/user-attachments/assets/6848d32b-2676-467e-9d53-9f75aa6dd72b" />
<img width="2115" height="2158" alt="_out-2d-heatmap-errors-xy" src="https://github.com/user-attachments/assets/d5495d2d-7e0f-4479-8370-483b5ef522cd" />
<img width="2115" height="2158" alt="_out-2d-heatmap-errors-xx" src="https://github.com/user-attachments/assets/492e1f95-70cb-448c-a0cf-85e120a8e6ab" />
<img width="2124" height="2156" alt="_out-average-errors-x" src="https://github.com/user-attachments/assets/7417622b-7c2f-4ba3-b2c0-84dd7edfa005" />

## Performance
<img width="2120" height="1771" alt="_out-performance" src="https://github.com/user-attachments/assets/d44f3ffa-875a-4e94-b633-403938971564" />
This performance test was made on a system consisting of an AMD EPYC 7713 64-core processor.

## References
[1] Higuera, Adam V., and John R. Cary. "Structure-preserving second-order integration of relativistic charged particle trajectories in electromagnetic fields." Physics of Plasmas 24.5 (2017).
