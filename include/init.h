#ifndef INIT_H
#define INIT_H

#include <stdio.h>

//Definitions for the particle struct, laser struct, and parameter struct.
//All of which are passed to the simulate() function.

#define LASER_PARAMS 9 //This defines how many parameters will be read from a file for one laser.

struct particle {
	double u[8];
};

struct laser {
	int num_lasers;
	double a0, sigma, omega, xif, zetax, zetay, phi, theta, psi;
	double epsilon1[3], epsilon2[3], n[3];
};

struct parameters {
	double wavelength, tauf, dtau, r, h, z;
	int num, num_lasers, steps, substeps, mode, output_mode, core_num;
};

//Function declarations, which are defined fully in init.c.

void compute_e(double *E, double *u, struct laser *l, int i);
void compute_b(double *B, double *E, double *u, struct laser *l, int i);
void compute_e_b(double *E, double *B, double *u, struct laser *l);
void electromag(double *u, double *up, struct laser *l);
void set_position(struct particle *p, double r, double h, double z, int i, int num, int output_mode);
void set_initial_vel(double *vi, double m, double phi, double theta);
void set_particles(struct particle *p, int num, double r, double h, double z, double angle, double *vi, int output_mode);
double *create_out_chunk(int output_mode, int num, int steps, int substeps, int core_num);
void set_mode(void (**compute_function)(double *, double *, struct laser *l), int mode);
void set_parameters(struct parameters *param, char *input);
void set_lasers(struct laser *l, int num_lasers, char *input);
#endif