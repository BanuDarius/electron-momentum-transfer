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
#include "extra.h"
#include "ponderomotive.h"

//This is a helper library which includes electromagnetic field computation functions, initializing particles and lasers, and parsing the simulation parameters.

void compute_e(double *E, double *u, struct laser *l, int i) {
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
	mult_vec(E1, Ec1);
	mult_vec(E2, Ec2);
	set_vec(E, E1, 3);
	add_vec(E, E2);
	mult_vec(E, E0);
}

void compute_b(double *B, double *E, double *u, struct laser *l, int i) {
	cross(l[i].n, E, B);
	mult_vec(B, 1.0 / c);
}

void compute_e_b(double *E, double *B, double *u, struct laser *l) {
	double Et[3], Bt[3];
	memset(E, 0, 3 * sizeof(double));
	memset(B, 0, 3 * sizeof(double));
	for(int i = 0; i < l[0].num_lasers; i++) {
		memset(Et, 0, 3 * sizeof(double));
		memset(Bt, 0, 3 * sizeof(double));
		compute_e(Et, u, l, i);
		compute_b(Bt, Et, u, l, i);
		add_vec(E, Et);
		add_vec(B, Bt);
	}
}

void electromag(double *u, double *up, struct laser *l) {
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
	mult_vec4(&up[4], q / (m * c));
}

void set_position(struct particle *p, double r, double h, double z, int i, int num, int output_mode) {
	if(output_mode == 0) {
		p->u[1] = - r + 2.0 * i * r / num;
		p->u[2] = 0.0;
		p->u[3] = 0.0;
	}
	else {
		p->u[1] = rand_val(h - r, h + r);
		p->u[2] = 0.0;
		p->u[3] = rand_val(h - r, h + r);
	}
}

void set_initial_vel(double *vi, double m, double phi, double theta) {
	set_vec(vi, direction_vec(phi, theta), 3);
	mult_vec(vi, m);
}

void set_particles(struct particle *p, struct parameters *param, double *vi) {
	for(int i = 0; i < param->num; i++) {
		p[i].u[0] = 0.0;
		set_position(&p[i], param->r, param->h, param->z, i, param->num, param->output_mode);
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
		return malloc(2 * U_SIZE * CHUNK_SIZE * param->core_num * sizeof(double));
}

//This function switched the compute_function to be either the electromagnetic method or the ponderomotive method.

void set_mode(void (**compute_function)(double *, double *, struct laser *), int mode) {
	if(mode == 1)
		*compute_function = ponderomotive;
	else if(mode == 2)
		*compute_function = electromag;
}

void set_parameters(struct parameters *param, char *input) {
	FILE *in = fopen(input, "r");
	if(!in) { perror("Cannot open input file."); abort(); }
	param->h = 0.0;
	param->z = 0.0;
	
	char current[32];
	int i;
	
	while(fscanf(in, "%s", current) != EOF) {
		if(!strcmp(current, "num"))
			i = fscanf(in, "%i", &param->num);
		else if(!strcmp(current, "num_lasers"))
			i = fscanf(in, "%i", &param->num_lasers);
		else if(!strcmp(current, "steps"))
			i = fscanf(in, "%i", &param->steps);
		else if(!strcmp(current, "substeps"))
			i = fscanf(in, "%i", &param->substeps);
		else if(!strcmp(current, "mode"))
			i = fscanf(in, "%i", &param->mode);
		else if(!strcmp(current, "tf"))
			i = fscanf(in, "%lf", &param->tf);
		else if(!strcmp(current, "output_mode"))
			i = fscanf(in, "%i", &param->output_mode);
		else if(!strcmp(current, "core_num"))
			i = fscanf(in, "%i", &param->core_num);
		else if(!strcmp(current, "r"))
			i = fscanf(in, "%lf", &param->r);
		else if(!strcmp(current, "rotate_angle"))
			i = fscanf(in, "%lf", &param->rotate_angle);
	}
	param->dt = param->tf / param->steps;
	fclose(in);
}

void set_lasers(struct laser *l, int num_lasers, char *input) {
	FILE *in = fopen(input, "r");
	if(!in) { perror("Cannot open input file."); abort(); }
	char current[32];
	int k;
	
	for(int i = 0; i < num_lasers; i++) {
		l[i].num_lasers = num_lasers;
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
		}
		double *nv = direction_vec(l[i].phi, l[i].theta);
		double epsilon1[3], epsilon2[3];
		epsilon(nv, epsilon1);
		cross(nv, epsilon1, epsilon2);
		set_vec(l[i].n, nv, 3);
		set_vec(l[i].epsilon1, epsilon1, 3);
		set_vec(l[i].epsilon2, epsilon2, 3);
		free(nv);
	}
}