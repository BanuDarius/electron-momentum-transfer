#include <math.h>
#include <stdlib.h>

#include "init.h"
#include "extra.h"
#include "ponderomotive.h"

void compute_e(double *E, double *u, struct laser *l, int i) {
	double k = l[i].omega / c;
	double t = u[0] / c;
	double xif = l[i].xif, sigma = l[i].sigma;
	double alpha = l[i].omega * t - k * dot(l[i].n, &u[1]);
	double Ec1 = env(alpha + l[i].psi, xif, sigma);
	double Ec2 = env_prime(alpha + l[i].psi, xif, sigma);
	double E1[3], E2[3];
	for(int j = 0; j < 3; j++)
		E1[j] = l[i].epsilon1[j] * l[i].zetax * cos(alpha) + l[i].epsilon2[j] * l[i].zetay * sin(alpha);
	for(int j = 0; j < 3; j++)
		E2[j] = l[i].epsilon1[j] * l[i].zetax * sin(alpha) + l[i].epsilon2[j] * l[i].zetay * (-cos(alpha));
	mult_vec(E1, Ec1);
	mult_vec(E2, Ec2);
	set_vec(E, E1, 3);
	add_vec(E, E2);
	mult_vec(E, l[i].E0);
}

void compute_b(double *B, double *E, double *u, struct laser *l, int i) {
	cross(l[i].n, E, B);
	mult_vec(B, 1/c);
}

void compute_e_b(double *E, double *B, double *u, struct laser *l) {
	double Et[3], Bt[3];
	for(int i = 0; i < NUM_LASERS; i++) {
		set_zero(Et);
		set_zero(Bt);
		compute_e(Et, u, l, i);
		compute_b(Bt, Et, u, l, i);
		add_vec(E, Et);
		add_vec(B, Bt);
	}
}

void electromag(double *u, double *up, struct laser *l) {
	double E[3], B[3];
	set_zero(E); set_zero(B);
	compute_e_b(E, B, u, l);
	
	up[0] = u[4];
	up[1] = u[5];
	up[2] = u[6];
	up[3] = u[7];
	up[4] = E[0] * u[5] + E[1] * u[6] + E[2] * u[7];
	up[5] = E[0] * u[4] + B[2] * c * u[6] - B[1] * c * u[7];
	up[6] = E[1] * u[4] - B[2] * c * u[5] + B[0] * c * u[7];
	up[7] = E[2] * u[4] + B[1] * c * u[5] - B[0] * c * u[6];
	mult_vec4(&up[4], q / (m * c));
}

void set_position(struct particle *p, double r, double h, double z, int i, int num, int output_mode) {
	double wavelength = 2.0 * pi * c / 0.057;
	if(output_mode == 0) {
		p->u[1] = - r + 2.0 * i * r / num + 50.0;
		p->u[2] = 0.0;
	}
	else {
		p->u[1] = rand_val(h - r, h + r);
		p->u[2] = rand_val(h - r, h + r);
	}
	p->u[3] = rand_val(h - z, h + z);
}

void rotate(double *u, double phi, double theta) {
	double x, y, z;
	y = u[1];
	z = u[2];
	u[1] = y * cos(phi) - z * sin(phi);
	u[2] = y * sin(phi) + z * cos(phi);
	x = u[0];
	y = u[1];
	u[0] = x * cos(theta) - y * sin(theta);
	u[1] = x * sin(theta) + y * cos(theta);
}

double *direction_vec(double phi_l, double theta_l) {
	double *u = new_vec(3);
	u[0] = 0.0;
	u[1] = 0.0;
	u[2] = 1.0;
	rotate(u, phi_l, theta_l);
	return u;
}

void epsilon(double *u, double *w) {
	double v[3];
	v[0] = 1.0;
	v[1] = 0.0;
	v[2] = 0.0;
	cross(u, v, w);
	double mag = magnitude(w);
	double scale = magnitude(u);
	for (int i = 0; i < 3; i++)
		w[i] = scale * w[i] / mag;
}

void set_initial_vel(double *vi, double m, double phi, double theta) {
	set_vec(vi, direction_vec(phi, theta), 3);
	mult_vec(vi, m);
}

void set_laser(struct laser *l, double E0, double phi, double theta, double xif, double omega, double sigma, double psi) {
	l->E0 = E0;
	l->psi = psi;
	l->xif = xif;
	l->zetax = 0.0;
	l->zetay = 1.0;
	l->omega = omega;
	l->sigma = sigma;
	double *nv = direction_vec(phi, theta);
	double epsilon1[3];
	double epsilon2[3];
	epsilon(nv, epsilon1);
	cross(nv, epsilon1, epsilon2);
	set_vec(l->n, nv, 3);
	set_vec(l->epsilon1, epsilon1, 3);
	set_vec(l->epsilon2, epsilon2, 3);
	free(nv);
}

void set_particles(struct particle *p, int num, double r, double h, double z, double phi, double theta, double *vi, int output_mode) {
	for(int i = 0; i < num; i++) {
		p[i].u[0] = 0;
		set_position(&p[i], r, h, z, i, num, output_mode);
		rotate(&p[i].u[1], phi, theta);
		double gamma = compute_gamma(vi);
		p[i].u[4] = m * c * gamma;
		p[i].u[5] = m * vi[0] * gamma;
		p[i].u[6] = m * vi[1] * gamma;
		p[i].u[7] = m * vi[2] * gamma;
	}
}

double *create_out_chunk(int output_mode, int num, int steps, int substeps, int core_num) {
	if(output_mode == 0)
		return malloc(U_SIZE * steps * num / substeps * sizeof(double));
	else
		return malloc(2 * U_SIZE * CHUNK_SIZE * core_num * sizeof(double));
}

void set_mode(void (**compute_function)(double *, double *, struct laser *), int mode) {
	if(mode == 0)
		*compute_function = electromag;
	else if(mode == 1)
		*compute_function = ponderomotive;
}