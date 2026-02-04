#ifndef INIT_H
#define INIT_H

#include <stdio.h>

struct particle {
	double u[8];
};

struct laser {
	double E0, sigma, omega, xif, zetax, zetay, psi;
	double epsilon1[3], epsilon2[3], n[3];
};

void compute_e(double *E, double *u, struct laser *l, int i);
void compute_b(double *B, double *E, double *u, struct laser *l, int i);
void compute_e_b(double *E, double *B, double *u, struct laser *l);
void electromag(double *u, double *up, struct laser *l);
void set_position(struct particle *p, double r, double h, double z, int i, int num, int output_mode);
void rotate(double *u, double phi, double theta);
double *direction_vec(double phi_l, double theta_l);
void epsilon(double *u, double *w);
void set_initial_vel(double *vi, double m, double phi, double theta);
void set_laser(struct laser *l, double E0, double phi, double theta, double xif, double omega, double sigma, double psi);
void set_particles(struct particle *p, int num, double r, double h, double z, double phi, double theta, double *vi, int output_mode);
double *create_out_chunk(int output_mode, int num, int steps, int substeps);

#endif