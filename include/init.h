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

#ifndef INIT_H
#define INIT_H

#include <stdio.h>

//Definitions for the particle struct, laser struct, and parameter struct.
//All of which are passed to the simulate() function.

#define LASER_PARAMS 10 //This defines how many parameters will be read from a file for one laser.

struct particle {
	double u[8];
};

struct laser {
	int num_lasers, pond_integrate_steps;
	double sigma, zetax, zetay, omega, theta, phi, psi, xif, a0;
	double epsilon1[3], epsilon2[3], n[3];
};

struct parameters {
	double rotate_angle, r_min, r_max, tf, dt, h, z;
	int num, num_lasers, steps, substeps, mode, output_mode, core_num;
};

void compute_e(double *E, double *u, const struct laser *restrict l, int i);
void compute_b(double *B, double *E, double *u, const struct laser *restrict l, int i);
void compute_e_b(double *E, double *B, double *u, const struct laser *restrict l);
void electromag(double *u, double *restrict up, const struct laser *restrict l);
void set_position(double *u, double r_min, double r_max, double h, double z, int i, int num, int output_mode);
void set_initial_vel(double *vi, double m, double phi, double theta);
void set_particles(struct particle *p, struct parameters *param, double *vi);
double *create_out_chunk(struct parameters *param);
void set_mode(void (**compute_function)(double *restrict, double *restrict, const struct laser *restrict), int mode);
void set_parameters(struct parameters *param, char *input);
void set_lasers(struct laser *l, int num_lasers, char *input);

#endif