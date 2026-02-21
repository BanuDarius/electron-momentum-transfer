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
#include <string.h>
#include <stdlib.h>

#include "units.h"
#include "init.h"
#include "tools.h"
#include "math_tools.h"
#include "ponderomotive.h"

//This is a helper library which includes electromagnetic field computation functions, initializing particles and lasers, and parsing the simulation parameters

void compute_e(double *E, double *u, const struct laser *restrict l, int i) {
	double E0 = l[i].omega * c * l[i].a0;
	double k = l[i].omega / c;
	double t = u[0] / c;
	double xif = l[i].xif, sigma = l[i].sigma;
	double alpha = l[i].omega * t - k * dot(l[i].n, &u[1]);
	double Ec1 = env(alpha + l[i].psi, xif, sigma);
	double Ec2 = env_prime(alpha + l[i].psi, xif, sigma);
	double E1[3], E2[3];
	for(int j = 0; j < 3; j++) {
		E1[j] = l[i].epsilon1[j] * l[i].zetax * (-cos(alpha)) + l[i].epsilon2[j] * l[i].zetay * sin(alpha);
		E2[j] = l[i].epsilon1[j] * l[i].zetax * (-sin(alpha)) + l[i].epsilon2[j] * l[i].zetay * (-cos(alpha));
	}
	mult_vec(E1, E1, Ec1);
	mult_vec(E2, E2, Ec2);
	memcpy(E, E1, 3 * sizeof(double));
	add_vec(E, E, E2);
	mult_vec(E, E, E0);
}

void compute_b(double *B, double *E, double *u, const struct laser *restrict l, int i) {
	cross(B, l[i].n, E);
	mult_vec(B, B, 1.0 / c);
}

void compute_e_b(double *E, double *B, double *u, const struct laser *restrict l) {
	double Et[3], Bt[3];
	memset(E, 0, 3 * sizeof(double));
	memset(B, 0, 3 * sizeof(double));
	for(int i = 0; i < l[0].num_lasers; i++) {
		memset(Et, 0, 3 * sizeof(double));
		memset(Bt, 0, 3 * sizeof(double));
		compute_e(Et, u, l, i);
		compute_b(Bt, Et, u, l, i);
		add_vec(E, E, Et);
		add_vec(B, B, Bt);
	}
}

void electromag(double *restrict u, double *restrict up, const struct laser *restrict l) {
	double E[3], B[3];
	compute_e_b(E, B, u, l);
	
	up[0] = u[4];
	up[1] = u[5];
	up[2] = u[6];
	up[3] = u[7];
	up[4] = E[0] * u[5] + E[1] * u[6] + E[2] * u[7];
	up[5] = E[0] * u[4] + B[2] * c * u[6] - B[1] * c * u[7];
	up[6] = E[1] * u[4] - B[2] * c * u[5] + B[0] * c * u[7];
	up[7] = E[2] * u[4] + B[1] * c * u[5] - B[0] * c * u[6];
	mult_vec4(&up[4], &up[4], q / (m * c));
}

void ponderomotive(double *restrict u, double *restrict up, const struct laser *restrict l) {
	double a = compute_a(u, l);
	double mass = m * sqrt(1.0 + a);
	double dmdx[4];
	
	double m_sqrt_a = 0.5 * m / sqrt(1.0 + a);
	for(int i = 0; i < 4; i++)
		dmdx[i] = derivative_a(u, l, i) * m_sqrt_a;
	
	up[0] = u[4];
	up[1] = u[5];
	up[2] = u[6];
	up[3] = u[7];
	up[4] = - u[4] * u[4] * dmdx[0] / c + c * dmdx[0] - u[4] * u[5] * dmdx[1] - u[4] * u[6] * dmdx[2] - u[4] * u[7] * dmdx[3];
	up[5] = - u[5] * u[4] * dmdx[0] / c - (c * c) * dmdx[1] - u[5] * u[5] * dmdx[1] - u[5] * u[6] * dmdx[2] - u[5] * u[7] * dmdx[3];
	up[6] = - u[6] * u[4] * dmdx[0] / c - u[6] * u[5] * dmdx[1] - (c * c) * dmdx[2] - u[6] * u[6] * dmdx[2] - u[6] * u[7] * dmdx[3];
	up[7] = - u[7] * u[4] * dmdx[0] / c - u[7] * u[5] * dmdx[1] - u[7] * u[6] * dmdx[2] - (c * c) * dmdx[3] - u[7] * u[7] * dmdx[3];
	mult_vec4(&up[4], &up[4], 1.0 / mass);
}

void set_position(double *u, double r_min, double r_max, double h, double z, int i, int num, int output_mode) {
	if(output_mode == 0) {
		u[0] = r_min + i * (r_max - r_min) / num;
		u[1] = 0.0;
		u[2] = 0.0;
	}
	else {
		u[0] = rand_val(h + r_min, h + r_max);
		u[1] = 0.0;
		u[2] = rand_val(h + r_min, h + r_max);
	}
}

void set_initial_vel(double *vi, double m, double phi, double theta) {
	direction_vec(vi, phi, theta);
	mult_vec(vi, vi, m);
}

void set_particles(struct particle *p, struct parameters *param, double *vi) {
	for(int i = 0; i < param->num; i++) {
		p[i].u[0] = 0.0;
		set_position(&p[i].u[1], param->r_min, param->r_max, param->h, param->z, i, param->num, param->output_mode);
		rotate_around_z_axis(&p[i].u[1], param->rotate_angle);
		double gamma = comp_gamma(vi);
		p[i].u[4] = gamma * m * c;
		p[i].u[5] = gamma * m * vi[0];
		p[i].u[6] = gamma * m * vi[1];
		p[i].u[7] = gamma * m * vi[2];
	}
}

//This function dynamically allocates output_chunk based on the output mode.

double *create_out_chunk(struct parameters *param) {
	if(param->output_mode == 0)
		return malloc(U_SIZE * param->steps * param->num / param->substeps * sizeof(double));
	else
		return malloc(2 * U_SIZE * CHUNK_SIZE * param->thread_num * sizeof(double));
}

//This function switched the compute_function to be either the electromagnetic method or the ponderomotive method.

void set_mode(void (**compute_function)(double *, double *, const struct laser *restrict), int mode) {
	if(mode == 1)
		*compute_function = ponderomotive;
	else if(mode == 2)
		*compute_function = electromag;
}

void set_parameters(struct parameters *param, char *input) {
	FILE *in = fopen(input, "r");
	if(!in) { perror("Cannot open input file."); exit(1); }
	param->h = 0.0;
	param->z = 0.0;
	
	char current[32];
	int i, count = 0;
	
	while(fscanf(in, "%s", current) != EOF) {
		if(!strcmp(current, "num")) {
			i = fscanf(in, "%i", &param->num);
			count++;
		}
		else if(!strcmp(current, "num_lasers")) {
			i = fscanf(in, "%i", &param->num_lasers);
			count++;
		}
		else if(!strcmp(current, "steps")) {
			i = fscanf(in, "%i", &param->steps);
			count++;
		}
		else if(!strcmp(current, "substeps")) {
			i = fscanf(in, "%i", &param->substeps);
			count++;
		}
		else if(!strcmp(current, "mode")) {
			i = fscanf(in, "%i", &param->mode);
			count++;
		}
		else if(!strcmp(current, "tf")) {
			i = fscanf(in, "%lf", &param->tf);
			count++;
		}
		else if(!strcmp(current, "output_mode")) {
			i = fscanf(in, "%i", &param->output_mode);
			count++;
		}
		else if(!strcmp(current, "thread_num")) {
			i = fscanf(in, "%i", &param->thread_num);
			count++;
		}
		else if(!strcmp(current, "r_min")) {
			i = fscanf(in, "%lf", &param->r_min);
			count++;
		}
		else if(!strcmp(current, "r_max")) {
			i = fscanf(in, "%lf", &param->r_max);
			count++;
		}
		else if(!strcmp(current, "rotate_angle")) {
			i = fscanf(in, "%lf", &param->rotate_angle);
			count++;
		}
		else if(!strcmp(current, "check_polarization")) {
			i = fscanf(in, "%i", &param->check_polarization);
			count++;
		}
	}
	if(count != PARAMS) {
		printf("Error: Invalid input file.\n");
		exit(1);
	}
	param->dt = param->tf / param->steps;
	fclose(in);
}

void set_lasers(struct laser *l, struct parameters *param, char *input) {
	FILE *in = fopen(input, "r");
	if(!in) { perror("Cannot open input file."); abort(); }
	char current[32];
	int k;
	
	for(int i = 0; i < param->num_lasers; i++) {
		l[i].num_lasers = param->num_lasers;
		for(int j = 0; j < LASER_PARAMS; j++) {
			k = fscanf(in, "%s", current);
			if(!strcmp(current, "a0"))
				k = fscanf(in, "%lf", &l[i].a0);
			else if(!strcmp(current, "sigma"))
				k = fscanf(in, "%lf", &l[i].sigma);
			else if(!strcmp(current, "omega"))
				k = fscanf(in, "%lf", &l[i].omega);
			else if(!strcmp(current, "xif"))
				k = fscanf(in, "%lf", &l[i].xif);
			else if(!strcmp(current, "zetax"))
				k = fscanf(in, "%lf", &l[i].zetax);
			else if(!strcmp(current, "zetay"))
				k = fscanf(in, "%lf", &l[i].zetay);
			else if(!strcmp(current, "phi"))
				k = fscanf(in, "%lf", &l[i].phi);
			else if(!strcmp(current, "theta"))
				k = fscanf(in, "%lf", &l[i].theta);
			else if(!strcmp(current, "psi"))
				k = fscanf(in, "%lf", &l[i].psi);
			else if(!strcmp(current, "pond_integrate_steps"))
				k = fscanf(in, "%i", &l[i].pond_integrate_steps);
			else if(!strcmp(current, "alpha"))
				k = fscanf(in, "%lf", &l[i].alpha);
		}
		double epsilon1[3], epsilon2[3], nv[3];
		direction_vec(nv, l[i].phi, l[i].theta);
		epsilon(nv, epsilon1);
		cross(epsilon2, nv, epsilon1);
		rotate_polarization(epsilon1, epsilon2, l[i].alpha);
		memcpy(l[i].n, nv, 3 * sizeof(double));
		memcpy(l[i].epsilon1, epsilon1, 3 * sizeof(double));
		memcpy(l[i].epsilon2, epsilon2, 3 * sizeof(double));
	}
	if(param->check_polarization) {
		for(int i = 0; i < param->num_lasers; i++) {
			printf("Propagation vector for laser %i:\n%0.2f %0.2f %0.2f\n", i, l[i].n[0], l[i].n[1], l[i].n[2]);
			printf("Epsilon 1 polarization for laser %i:\n%0.2f %0.2f %0.2f\n", i, l[i].epsilon1[0], l[i].epsilon1[1], l[i].epsilon1[2]);
			printf("Epsilon 2 polarization for laser %i:\n%0.2f %0.2f %0.2f\n\n", i, l[i].epsilon2[0], l[i].epsilon2[1], l[i].epsilon2[2]);
		}
		exit(1);
	}
}