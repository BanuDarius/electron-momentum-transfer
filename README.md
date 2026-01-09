## Introduction
This is a C/C++ program that calculates the linear momentum transfer caused by multiple laser beams coming from arbitrary directions, to an assembly of electrons, producing a 2D momentum map.
Parallelized with POSIX threads.

## Examples

https://github.com/user-attachments/assets/1535b362-bc3e-450c-ba59-d7517e42125d

https://github.com/user-attachments/assets/06e6861b-48ff-45ea-b6d0-f5003de2d465

## Installation
To use the program, clone it, compile the `LaserElectron.cpp` file with a C++ compiler such as `g++`, and run the `AutoCompute.py` script using python. For example:
```
git clone https://github.com/BanuDarius/electron-momentum-transfer.git
cd electron-momentum-transfer
g++ LaserElectron.cpp
py AutoCompute.py
```

## Usage
In this version, the `AutoCompute.py` script will create a single 2D transfer map. In order to create a parameter sweep, change the range of the main loop from the python script.

## Output
<b> The primary scope of this program is to visualize the momentum transfer, by creating a 2D graph for a parameter set. </b> In each graph, you can see a bunch of dots, each representing the initial position of an electron. This is the initial scenario. 

Then, the simulation is ran, and the lasers interact with the electrons. This usually results in a linear momentum transfer, so some electrons will have a final speed different from zero.

The colors, by default are as such: For positive final momentum in the specified direction, red, for zero, white, and for negative final momentum, blue. The color map is included in the right of each graph for easier understanding.

The main program is created to simulate 2 laser beams coming head-on, both having an intensity parameter a0 specified in the first parameter of the program: `./LaserElectron <a0>`

So executing `./LaserElectron 0.500` will create a file named `out-0.500.txt`, containing 16 numbers per column. The first 8 numbers are the initial 4-positions and 4-velocities of an electron, and the last 8 numbers are the final 4-positions and 4-velocities of the same electron, after the interaction with the lasers.



## References
[1] Boost ODEINT library: https://www.boost.org/
