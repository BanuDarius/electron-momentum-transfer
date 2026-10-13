<div align="center">

## EMT: Electron Momentum Transfer

[![Paper DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.cpc.2026.110445-blue.svg)](https://doi.org/10.1016/j.cpc.2026.110445)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Language: C](https://img.shields.io/badge/Language-C11-00599C.svg)](https://en.wikipedia.org/wiki/C11_(C_revision))
[![Parallelization: OpenMP](https://img.shields.io/badge/Parallelization-OpenMP-green.svg)](https://www.openmp.org/)

</div>

## Overview

Electron Momentum Transfer is a simulation program created to map the validity domains of the relativistic ponderomotive approximation against the exact Lorentz force in multi-beam laser configurations.

Full kinetic Particle-In-Cell (PIC) codes frequently use the time-averaged ponderomotive approximation to average out small scale oscillations of the motion of the particles, and accelerate the computation. However, in complex multi-beam interference fields or relativistic intensities, chaotic behaviour can invalidate the ponderomotive approximation. EMT simulates single particle relativistic trajectories to generate automated parameter sweeps and produce 2D momentum transfer and error heatmaps.

## Publication
This software has been published as an open-access paper:

"EMT: A multi-threaded particle pusher for validating the ponderomotive approximation in relativistic laser-electron interactions"

Computer Physics Communications, Volume 330, 2027, 110445.

DOI: [10.1016/j.cpc.2026.110445](https://doi.org/10.1016/j.cpc.2026.110445)

## Gallery
<img width="1072" height="1078" alt="1_out-2d-heatmap-electromag-yy" src="https://github.com/user-attachments/assets/9be7793a-a5a0-4938-9984-07a3faf16b83" />

<img width="1056" height="1078" alt="1_out-2d-heatmap-errors-yy" src="https://github.com/user-attachments/assets/50f1659c-f66d-4705-893b-606e386e63dc" />

<img width="2271" height="2199" alt="3_out-2d-heatmap-electromag-yy" src="https://github.com/user-attachments/assets/65746253-5e52-4519-9899-c0d6e56285e9" />

<img width="2228" height="2199" alt="3_out-2d-heatmap-errors-yy" src="https://github.com/user-attachments/assets/cd61461f-a81d-463c-94af-699c3bac44e5" />

<img width="2154" height="2194" alt="3_out-average-errors-y" src="https://github.com/user-attachments/assets/7e8bc865-e120-4344-b938-e8d191d0f890" />
