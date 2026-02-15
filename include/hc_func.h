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

#ifndef HC_FUNC_H
#define HC_FUNC_H

#include <math.h>
#include <string.h>

#include "units.h"
#include "math_tools.h"

//These are optimized helper functions for the Higuera-Cary push

static inline double hc_s_factor(const double *restrict t_rot) {
	double s_factor = 2.0 / (1.0 + dot(t_rot, t_rot));
	return s_factor;
}

static inline void hc_beta(double *restrict beta, const double *restrict B, const double dt) {
	for(int i = 0; i < 3; i++)
		beta[i] = B[i] * q * dt / (2.0 * m);
}

static inline void hc_epsilon(double *restrict epsilon, const double *restrict E, const double dt) {
	for(int i = 0; i < 3; i++)
		epsilon[i] = E[i] * q * dt / 2.0;
}

static inline void hc_t_rot(double *restrict t_rot, const double *restrict beta, const double gamma_new) {
	for(int i = 0; i < 3; i++)
		t_rot[i] = beta[i] / gamma_new;
}

static inline void hc_u_minus(double *restrict u_minus, const double *restrict u_i, const double *restrict epsilon) {
	for(int i = 0; i < 3; i++)
		u_minus[i] = u_i[i] + epsilon[i];
}

static inline void hc_u_prime(double *restrict u_prime, const double *restrict u_minus, const double *restrict t_rot) {
	double t1[3];
	cross(t1, u_minus, t_rot);
	for(int i = 0; i < 3; i++)
		u_prime[i] = u_minus[i] + t1[i];
}

static inline double hc_gamma_new(double *restrict u_minus, const double *restrict beta, const double gamma_minus) {
	double t1 = gamma_minus * gamma_minus - dot(beta, beta);
	double t2 = dot(beta, beta) + fabs(dot(beta, u_minus) * dot(beta, u_minus) / (c * c));
	double t3 = 0.5 * (gamma_minus * gamma_minus - dot(beta, beta) + sqrt(t1 * t1 + 4.0 * t2));
	double gamma_new = sqrt(t3);
	return gamma_new;
}

static inline void hc_u_plus(double *restrict u_plus, const double *restrict u_minus, const double *restrict u_prime, const double s_factor, const double *restrict t_rot) {
	double t1[3], t2[3];
	memcpy(t1, t_rot, 3 * sizeof(double));
	mult_vec(t1, t1, s_factor);
	cross(t2, u_prime, t1);
	for(int i = 0; i < 3; i++)
		u_plus[i] = u_minus[i] + t2[i];
}

#endif