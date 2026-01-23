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

extern struct laser *l;

struct shared_data {
	FILE *out;
	struct laser *l;
	struct particle *e;
	double *out_chunk;
	double dtau;
	int initial_index, final_index, substeps, steps, output_mode, num, id;
	void (*fc)(double*, double*);
};

void compute_e(double *E, double *u, struct laser *l, int i);
void compute_b(double *B, double *E, double *u, struct laser *l, int i);
void compute_e_b(double *E, double *B, double *u);
void electromag(double *u, double *up);
void set_position(struct particle *p, double r, double h, double z, int i, int num, int output_mode);
void rotate(double *u, double phi, double theta);
double *direction_vec(double phi_l, double theta_l);
void epsilon(double *u, double *w);
void set_initial_vel(double *vi, double m, double phi, double theta);
void set_laser(struct laser *l, double E0, double phi, double theta, double xif, double omega, double sigma, double psi);
void set_particles(struct particle *p, int num, double r, double h, double z, double phi, double theta, double *vi, int output_mode);
void set_shared_data(struct shared_data *sdata, struct particle *e, struct laser *l, FILE *out, double *out_chunk,
	int num, int steps, double dtau, int output_mode, int substeps, void (*fc)(double*, double*));
double *create_out_chunk(int output_mode, int num, int steps, int substeps);
void check_errors(void *out, void *sdata);

#endif