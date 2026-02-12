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

#include <math.h>
#include <stdlib.h>
#include <string.h>

#include "units.h"
#include "extra.h"
#include "hc_func.h"

//This is a helper library which includes several simple functions for vector operations and mathematics.

double rand_val(double min, double max) {
	double s = rand() / (double) RAND_MAX;
	return min + s * (max - min);
}

void print_chunk(FILE *out, double *chunk, int core_num) {
	fwrite(chunk, sizeof(double), 2 * U_SIZE * CHUNK_SIZE * core_num, out);
}

void copy_initial(double *ch, double *u, int k, int id) {
	int index = 2 * id * U_SIZE * CHUNK_SIZE + 2 * U_SIZE * k;
	for(int i = index; i < index + U_SIZE; i++)
		ch[i] = u[i - index];
}

void set_chunk(double *out_chunk, double *chunk, int init, int fin) {
	for(int i = init; i < fin; i++)
		out_chunk[i] = chunk[i-init];
}

void set_vec(double *u1, double *u2, int n) {
	for (int i = 0; i < n; i++)
		u1[i] = u2[i];
}

double *new_vec(int n) {
	double *u = malloc(n * sizeof(double));
	return u;
}

void set_zero(double *u) {
	for(int i = 0; i < 3; i++)
		u[i] = 0;
}

void set_zero_n(double *u, int n) {
	for(int i = 0; i < n; i++)
		u[i] = 0;
}

void mult_vec(double *u, double a) {
	for(int i = 0; i < 3; i++)
		u[i] *= a;
}

void mult_vec4(double *u, double a) {
	for(int i = 0; i < 4; i++)
		u[i] *= a;
}

void add_vec(double *u, double *v) {
	for(int i = 0; i < 3; i++)
		u[i] += v[i];
}

void add_vec4(double *u, double *v) {
	for(int i = 0; i < 4; i++)
		u[i] += v[i];
}

void sub_vec(double *x, double *u, double *v) {
	for(int i = 0; i < 3; i++)
		x[i] = u[i] - v[i];
}

void cross(double *a, double *b, double *u) {
	u[0] = a[1] * b[2] - a[2] * b[1];
	u[1] = a[2] * b[0] - a[0] * b[2];
	u[2] = a[0] * b[1] - a[1] * b[0];
}

double dot(double *a, double *b) {
	double x = a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
	return x;
}

double dot4(double *u, double *v) {
	double x = u[0] * v[0] - u[1] * v[1] - u[2] * v[2] - u[3] * v[3];
	return x;
}

double magnitude(double *a) {
	double x = sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);
	return x;
}

double compute_gamma(double *v) {
	double mag = magnitude(v);
	double gamma = 1.0 / sqrt(1.0 - (mag * mag) / (c * c));
	return gamma;
}

void set_spherical_coords(double *u, double phi, double theta) {
	double mag = magnitude(u);
	u[0] = mag * sin(phi) * cos(theta);
	u[1] = mag * sin(phi) * sin(theta);
	u[2] = mag * cos(phi);
}

void rotate_around_z_axis(double *u, double angle) {
	double u_temp[2] = { u[0], u[1] };
	u[0] = u_temp[0] * cos(angle) - u_temp[1] * sin(angle);
	u[1] = u_temp[0] * sin(angle) + u_temp[1] * cos(angle);
}

double *direction_vec(double phi, double theta) {
	double *u = new_vec(3);
	u[0] = 0.0; u[1] = 0.0; u[2] = 1.0;
	set_spherical_coords(u, phi, theta);
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

//These functions are for the envelope.

double env(double xi, double xif, double sigma) {
	if(xi > -xif && xi < xif)
		return 1.0;
	else if(xi >= xif)
		return exp(-(xi - xif) * (xi - xif) / (sigma * sigma));
	else
		return exp(-(xi + xif) * (xi + xif) / (sigma * sigma));
}

double env_prime(double xi, double xif, double sigma) {
	if(xi > -xif && xi < xif)
		return 0.0;
	else if(xi >= xif)
		return - 2.0 * (xi - xif) / (sigma * sigma) * exp(-(xi - xif) * (xi - xif) / (sigma * sigma));
	else
		return - 2.0 * (xi + xif) / (sigma * sigma) * exp(-(xi + xif) * (xi + xif) / (sigma * sigma));
}

//This function is a Runge-Kutta fourth-order solver, with a general compute_function() which can be switched easily.

void rk4_step(double *u, double dt, struct laser *l, void compute_function(double *, double *, struct laser *)) {
	double u0[U_SIZE], u_temp[U_SIZE];
	double k1[U_SIZE]; double k2[U_SIZE];
	double k3[U_SIZE]; double k4[U_SIZE];
	memcpy(u0, u, U_SIZE * sizeof(double));
	
	compute_function(u0, k1, l);
	for (int i = 0; i < U_SIZE; i++)
		u_temp[i] = u0[i] + 0.5 * k1[i] * dt;
	
	compute_function(u_temp, k2, l);
	for (int i = 0; i < U_SIZE; i++)
		u_temp[i] = u0[i] + 0.5 * k2[i] * dt;
	
	compute_function(u_temp, k3, l);
	for (int i = 0; i < U_SIZE; i++)
		u_temp[i] = u0[i] + k3[i] * dt;
	
	compute_function(u_temp, k4, l);
	for (int i = 0; i < U_SIZE; i++)
		u[i] = u0[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]);
}

void higuera_cary_step(double *u, double dt, struct laser *l) {
	double epsilon_vec[3], u_minus[3], beta[3], E[3] = {0.0}, B[3] = {0.0};
	double u_final[3], u_prime[3], u_plus[3], t_rot[3], s_factor;
	double gamma_fac, gamma_minus, gamma_new;
	
	gamma_fac = u[4] / (m * c);
	u[0] += 0.5 * c * dt;
	u[1] += 0.5 * u[5] * dt / gamma_fac;
	u[2] += 0.5 * u[6] * dt / gamma_fac;
	u[3] += 0.5 * u[7] * dt / gamma_fac;
	
	compute_e_b(E, B, u, l);
	
	hc_beta(beta, B, dt);
	hc_epsilon(epsilon_vec, E, dt);
	hc_u_minus(u_minus, &u[5], epsilon_vec);
	
	gamma_minus = hc_gamma(u_minus);
	gamma_new = hc_gamma_new(u_minus, beta, gamma_minus);
	
	hc_t_rot(t_rot, beta, gamma_new);
	s_factor = hc_s_factor(t_rot);
	hc_u_prime(u_prime, u_minus, t_rot);
	hc_u_plus(u_plus, u_minus, u_prime, s_factor, t_rot);
	
	set_vec(u_final, u_plus, 3);
	add_vec(u_final, epsilon_vec);
	set_vec(&u[5], u_final, 3);
	
	gamma_fac = hc_gamma(&u[5]);
	u[0] += 0.5 * c * dt;
	u[1] += 0.5 * u[5] * dt / gamma_fac;
	u[2] += 0.5 * u[6] * dt / gamma_fac;
	u[3] += 0.5 * u[7] * dt / gamma_fac;
	u[4] = gamma_fac * m * c;
}

//Manual calculation of indices for stability.

int initial_index(int n, int thread_num, int core_num) {
	int index = n * thread_num / core_num;
	return index;
}

int final_index(int n, int thread_num, int core_num) {
	int index = n * (thread_num + 1) / core_num;
	return index;
}