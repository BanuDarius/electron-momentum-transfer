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

#include "init.h"
#include "hc_func.h"
#include "particle_push.h"

//The Higuera-Cary particle pusher

void higuera_cary_step(double *u, const double dt, const struct laser *restrict l) {
	double epsilon_vec[3], u_minus[3], beta[3], E[3], B[3];
	double u_final[3], u_prime[3], u_plus[3], t_rot[3], s_factor;
	double gamma_fac, gamma_minus, gamma_new;
	
	gamma_fac = u[4] / (m * c);
	u[0] += 0.5 * c * dt;
	u[1] += 0.5 * u[5] * dt / (gamma_fac * m);
	u[2] += 0.5 * u[6] * dt / (gamma_fac * m);
	u[3] += 0.5 * u[7] * dt / (gamma_fac * m);
	
	compute_e_b(E, B, u, l);
	
	hc_beta(beta, B, dt);
	hc_epsilon(epsilon_vec, E, dt);
	hc_u_minus(u_minus, &u[5], epsilon_vec);
	
	gamma_minus = comp_gamma(u_minus);
	gamma_new = hc_gamma_new(u_minus, beta, gamma_minus);
	
	hc_t_rot(t_rot, beta, gamma_new);
	s_factor = hc_s_factor(t_rot);
	hc_u_prime(u_prime, u_minus, t_rot);
	hc_u_plus(u_plus, u_minus, u_prime, s_factor, t_rot);
	
	memcpy(u_final, u_plus, 3 * sizeof(double));
	add_vec(u_final, u_final, epsilon_vec);
	memcpy(&u[5], u_final, 3 * sizeof(double));
	
	gamma_fac = comp_gamma(&u[5]);
	u[0] += 0.5 * c * dt;
	u[1] += 0.5 * u[5] * dt / (gamma_fac * m);
	u[2] += 0.5 * u[6] * dt / (gamma_fac * m);
	u[3] += 0.5 * u[7] * dt / (gamma_fac * m);
	u[4] = gamma_fac * m * c;
}

//This function is a Runge-Kutta fourth-order solver, with a general compute function

void rk4_step(double *u, double dt, const struct laser *restrict l, void compute_function(double *, double *, const struct laser *restrict)) {
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