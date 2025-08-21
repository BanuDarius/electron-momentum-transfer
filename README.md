## Introduction
This is a C program that calculates the linear momentum transfer caused by multiple laser beams coming from arbitrary directions, to an assembly of electrons, producing a 2D momentum map.
Parallelized with POSIX threads.

## Examples

https://github.com/user-attachments/assets/90a7d7d3-5d6a-4e61-8df4-b9b999851b62

https://github.com/user-attachments/assets/06e6861b-48ff-45ea-b6d0-f5003de2d465

## Installation
To use the program, clone it, compile the `LaserElectron.c` file with a C compiler such as `gcc`, and run the `AutoCompute.py` script using python. For example:
```
git clone https://github.com/BanuDarius/electron-momentum-transfer.git
cd electron-momentum-transfer
gcc LaserElectron.c
py AutoCompute.py
```

## Usage
By default, the `AutoCompute.py` script will create a single 2D transfer map. In order to create a parameter sweep, change the range of the main loop from the python script.

## Output
The main program is created to simulate 2 laser beams coming head-on, both having an intensity parameter a0 specified in the first parameter of the program: `./LaserElectron <a0>`

So executing `./LaserElectron 0.500` will create a file named `out-0.500.txt`, containing 16 numbers per column. The first 8 numbers are the initial 4-positions and 4-velocities of an electron, and the last 8 numbers are the final 4-positions and 4-velocities of the same electron, after the interaction with the lasers.

## References
[1] Runge-Kutta 4th order solver: https://people.math.sc.edu/Burkardt/c_src/rk4/rk4.html
