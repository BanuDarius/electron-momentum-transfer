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
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "init.h"
#include "tools.h"
#include "units.h"
#include "potentials.h"
#include "math_tools.h"
#include "ponderomotive.h"

double displacement(struct parameters *param, struct laser *l) {
	double A0 = l->a0 * m * c / fabs(q);
	double delta_x = q * q * A0 * A0 / (4.0 * m * m * c) * sqrt(M_PI / 2.0) * l->sigma / l->omega;
	return delta_x;
}

void simulate_analytic(FILE *out, struct particle *p, struct parameters *param, struct laser *l) {
	double u_i[4], u_c[4], d = 0.0, r_1[3], r_2[3] = { 0.0 }, r_tot[3], r_temp[3], k_vec[3];
	double dphi = param->tf * l->omega / param->steps, phi_rel, phi_abs;
	int i = 0;
	
	memcpy(u_i, p->u, 4 * sizeof(double));
	memcpy(u_c, p->u, 4 * sizeof(double));
	
	memcpy(k_vec, l->n, 3 * sizeof(double));
	mult_vec(k_vec, k_vec, l->omega / c);
	double phi_0 = - dot(k_vec, &u_i[1]);
	
	while(u_c[0] / c < param->tf) {
		phi_rel = phi_0 + i * dphi;
		phi_abs = i * dphi;
		d += q * q / (2.0 * m * m * c * l->omega) * integrate_phi(phi_rel, phi_rel + dphi, l);
		u_c[0] = c * (phi_abs / l->omega + d / c);
		
		mult_vec(r_1, l->n, d);
		
		integrate_phi_vec(r_temp, phi_rel, phi_rel + dphi, l);
		mult_vec(r_temp, r_temp, - q / (m * l->omega));
		add_vec(r_2, r_2, r_temp);
		
		add_vec(r_tot, r_1, r_2);
		add_vec(&u_c[1], &u_i[1], r_tot);
		
		fwrite(u_c, sizeof(double), 4, out);
		i++;
	}
}

int main(int argc, char **argv) {
	if(argc != 5) {
		printf("This is a program which simulates the trajectories of an electron interacting with a single laser, using an analytic solution.\n"); 
		printf("Usage: %s <filename_input> <filename_lasers> <filename_output>\n", argv[0]);
		printf("For more details visit: https://github.com/BanuDarius/electron-momentum-transfer.\n");
		return 1;
	}
	FILE *out = fopen(argv[3], "wb");
	if(!out) { perror("Cannot open output file."); return 1; }
	FILE *out_displacement = fopen(argv[4], "ab");
	if(!out_displacement) { perror("Cannot open output displacement file."); return 1; }
	
	struct parameters *param = malloc(sizeof(struct parameters));
	set_parameters(param, argv[1]);
	
	struct laser *l = malloc(param->num_lasers * sizeof(struct laser));
	struct particle *p = aligned_alloc(64, param->num * sizeof(struct particle));
	
	if(!l || !p) { perror("Memory allocation error."); return 1; }
	
	double vi[3];
	set_initial_vel(vi, 0.0, 0.0, 0.0);
	set_lasers(l, param, argv[2]);
	set_particles(p, param, vi);
	
	printf("Simulation started.\n");
	simulate_analytic(out, p, param, &l[0]);
	printf("Simulation ended.\n");
	
	double delta_x = displacement(param, l);
	fwrite(&delta_x, sizeof(double), 1, out_displacement);
	
	fclose(out_displacement); fclose(out);
	free(param); free(p); free(l);
	return 0;
}