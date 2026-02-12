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

#include "units.h"
#include "extra.h"
#include "hc_func.h"

//This file contains the definitions of the helper functions for the Higuera-Cary push

double hc_s_factor(double *t_rot) {
	double s_factor = 2.0 / (1.0 + dot(t_rot, t_rot));
	return s_factor;
}

void hc_beta(double *beta, double *B, double dt) {
	for(int i = 0; i < 3; i++)
		beta[i] = B[i] * q * dt / (2.0 * m);
}

void hc_epsilon(double *epsilon, double *E, double dt) {
	for(int i = 0; i < 3; i++)
		epsilon[i] = E[i] * q * dt / 2.0;
}

void hc_t_rot(double *t_rot, double *beta, double gamma_new) {
	for(int i = 0; i < 3; i++)
		t_rot[i] = beta[i] / gamma_new;
}

void hc_u_minus(double *u_minus, double *u_i, double *epsilon) {
	for(int i = 0; i < 3; i++)
		u_minus[i] = u_i[i] + epsilon[i];
}

void hc_u_prime(double *u_prime, double *u_minus, double *t_rot) {
	double t1[3];
	cross(u_minus, t_rot, t1);
	for(int i = 0; i < 3; i++)
		u_prime[i] = u_minus[i] + t1[i];
}

double hc_gamma_new(double *u_minus, double *beta, double gamma_minus) {
	double t1 = gamma_minus * gamma_minus - dot(beta, beta);
	double t2 = dot(beta, beta) + fabs(dot(beta, u_minus) * dot(beta, u_minus) / (c * c));
	double t3 = 0.5 * (gamma_minus * gamma_minus - dot(beta, beta) + sqrt(t1 * t1 + 4.0 * t2));
	double gamma_new = sqrt(t3);
	return gamma_new;
}

void hc_u_plus(double *u_plus, double *u_minus, double *u_prime, double s_factor, double *t_rot) {
	double t1[3], t2[3];
	set_vec(t1, t_rot, 3);
	mult_vec(t1, s_factor);
	cross(u_prime, t1, t2);
	for(int i = 0; i < 3; i++)
		u_plus[i] = u_minus[i] + t2[i];
}