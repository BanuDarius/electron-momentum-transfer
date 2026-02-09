#ifndef INIT_H
#define INIT_H

#include <stdio.h>

//Definitions for the particle struct, laser struct, and parameter struct.
//All of which are passed to the simulate() function.

struct particle {
	double u[8];
};

struct laser {
	double E0, sigma, omega, xif, zetax, zetay, psi;
	double epsilon1[3], epsilon2[3], n[3];
};

struct parameters {
	int num, steps, mode, output_mode, substeps, core_num;
	double a0, omega, wavelength, E0, tauf, sigma, dtau, r, h, z, xif;
};

//Function declarations, which are defined fully in init.c.

void compute_e(double *E, double *u, struct laser *l, int i);
void compute_b(double *B, double *E, double *u, struct laser *l, int i);
void compute_e_b(double *E, double *B, double *u, struct laser *l);
void electromag(double *u, double *up, struct laser *l);
void set_position(struct particle *p, double r, double h, double z, int i, int num, int output_mode);
void set_initial_vel(double *vi, double m, double phi, double theta);
void set_laser(struct laser *l, double E0, double phi, double theta, double xif, double omega, double sigma, double psi);
void set_particles(struct particle *p, int num, double r, double h, double z, double phi, double theta, double *vi, int output_mode);
double *create_out_chunk(int output_mode, int num, int steps, int substeps, int core_num);
void set_mode(void (**compute_function)(double *, double *, struct laser *l), int mode);
void set_parameters(struct parameters *param, char *input);

#endif