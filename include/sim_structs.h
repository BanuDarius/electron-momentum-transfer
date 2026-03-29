/* MIT License
*
* Copyright (c) 2026 Banu Darius-Matei
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"),
* to deal in the Software without restriction, including without limitation the
* rights to use, copy, modify, merge, publish, distribute, sublicense,
* and/or sell copies of the Software, and to permit persons to whom the
* Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included
* in all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
* INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
* FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
* OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
* WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
* OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.*/

#ifndef SIM_STRUCTS_H
#define SIM_STRUCTS_H

#include <stdio.h>
#include <stdalign.h>

#define LASER_PARAMS 11 //How many parameters will be read from a file for one laser
#define PARAMS 15 //How many parameters will be read from a file for the general simulation
#define U_SIZE 8 //Number of elements of the particle struct
#define CHUNK_SIZE 100 //Number of particles in an output chunk

struct particle {
	alignas(64) double u[U_SIZE]; //u[0] = ct, u[1-3] = x, y, z, u[4] = gamma * c, u[5-7] = gamma * v
}; //This struct has sizeof(struct particle) = 64 bytes, which is conveniently equal to a standard cache line

struct laser {
	int num_lasers, pond_integrate_steps;
	double alpha, sigma, zetax, zetay, omega, theta, phi, psi, etaf, a0;
	double epsilon1[3], epsilon2[3], n[3];
};

struct parameters {
	double rotate_angle, theta_v0, phi_v0, v0_mag, r_min, r_max, tf, dt;
	int num, num_lasers, steps, substeps, mode, output_mode, check_polarization, thread_num;
};

#endif