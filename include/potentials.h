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

#ifndef POTENTIALS_H
#define POTENTIALS_H

#include <math.h>

#include "units.h"
#include "gaussian.h"
#include "math_tools.h"
#include "sim_structs.h"

//This helper library contains functions for the electromagnetic potentials

static inline void potential_a(double *a, double *u, const Laser *restrict l, int n) {
	double potentialA0 = l[n].a0 * m * c / fabs(q);
	double epsilon4[4], k_vec4[4], eta, A0mult;
	
	a[0] = 0.0;
	k_vec4[0] = 1.0;
	copy_vec(&k_vec4[1], l[n].n);
	mult_vec4(k_vec4, k_vec4, l[n].omega / c);
	
	eta = dot4(k_vec4, u) + l[n].psi;
	A0mult = env(eta, l[n].etaf, l[n].sigma) * potentialA0;
	for(int i = 0; i < 3; i++)
		a[i+1] = l[n].epsilon1[i] * l[n].zetax * (sin(eta)) + l[n].epsilon2[i] * l[n].zetay * cos(eta);
	mult_vec(&a[1], &a[1], A0mult);
}

static inline void potential_a_gauss(double *a, double *u, const Laser *restrict l, int n) {
	double potentialA0 = l[n].a0 * m * c / fabs(q);
	double r_vec_local[3], r_vec_global[3], k_vec4[4], eta;
	double k = l[n].omega / c;

	a[0] = 0.0;
	k_vec4[0] = 1.0;
	copy_vec(&k_vec4[1], l[n].n);
	copy_vec(r_vec_global, &u[1]);
	mult_vec4(k_vec4, k_vec4, l[n].omega / c);
	eta = dot4(k_vec4, u) + l[n].psi;
	
	pos_global_to_local(r_vec_local, r_vec_global, &l[n]);

	double complex zeta_x = l[n].zeta_x_gauss, zeta_y = l[n].zeta_y_gauss;
	
	double r_z = compute_r_z(r_vec_local[2], l[n].z_r);
	double w_z = compute_w_z(l[n].w0, r_vec_local[2], l[n].z_r);
	double complex u_pm = compute_u(&l[n], r_vec_local, r_z, w_z);
	
	double complex phase = CMPLX(cos(eta), sin(eta));
	u_pm *= potentialA0 * phase * env(eta, l[n].etaf, l[n].sigma);
	
	double complex field_term = CMPLX(1.0 / r_z, -2.0 / (k * w_z * w_z));
	double complex a_z = - field_term * (zeta_x * r_vec_local[0] + zeta_y * r_vec_local[1]);
	
	double Axp = -cimag(u_pm * zeta_x);
	double Ayp = -cimag(u_pm * zeta_y);
	double Azp = -cimag(u_pm * a_z);
	
	for(int i = 0; i < 3; i++)
		a[i+1] = Axp * l[n].epsilon1[i] + Ayp * l[n].epsilon2[i] + Azp * l[n].n[i];
}

static inline void potential_deriv_a(double *a, double *u, const Laser *restrict l, int index, int n) {
	double potentialA0 = l[n].a0 * m * c / fabs(q);
	double epsilon4[4], k_vec4[4], eta, sign;
	
	a[0] = 0.0;
	k_vec4[0] = 1.0;
	copy_vec(&k_vec4[1], l[n].n);
	mult_vec4(k_vec4, k_vec4, l[n].omega / c);
	
	eta = dot4(k_vec4, u) + l[n].psi;
	sign = (index > 0) ? -1.0 : +1.0;
	for(int i = 0; i < 3; i++) {
		double t1 = l[n].epsilon1[i] * l[n].zetax * (sin(eta)) + l[n].epsilon2[i] * l[n].zetay * (cos(eta));
		double t2 = l[n].epsilon1[i] * l[n].zetax * (cos(eta)) + l[n].epsilon2[i] * l[n].zetay * (-sin(eta));
		a[i+1] = sign * potentialA0 * k_vec4[index] * (env(eta, l[n].etaf, l[n].sigma) * t2 + env_prime(eta, l[n].etaf, l[n].sigma) * t1);
	}
}

static inline void potential_deriv_a_gauss(double *a, double *u, const Laser *restrict l, int index, int n) {
	double potentialA0 = l[n].a0 * m * c / fabs(q);
	double r_vec_local[3], r_vec_global[3], k_vec4[4], eta, sign, k = l[n].omega / c;
	
	a[0] = 0.0;
	k_vec4[0] = 1.0;
	copy_vec(&k_vec4[1], l[n].n);
	copy_vec(r_vec_global, &u[1]);
	mult_vec4(k_vec4, k_vec4, l[n].omega / c);
	
	eta = dot4(k_vec4, u) + l[n].psi;
	sign = (index > 0) ? -1.0 : +1.0;
	double deta_dmu = sign * k_vec4[index]; 
	double dxp_dmu = 0.0, dyp_dmu = 0.0, dzp_dmu = 0.0;
	if(index > 0) {
		dxp_dmu = l[n].epsilon1[index - 1];
		dyp_dmu = l[n].epsilon2[index - 1];
		dzp_dmu = l[n].n[index - 1];
	}
	pos_global_to_local(r_vec_local, r_vec_global, &l[n]);
	
	double zR = 0.5 * k * l[n].w0 * l[n].w0, z_sq = r_vec_local[2] * r_vec_local[2], zR_sq = zR * zR, den = z_sq + zR_sq;
	double w2 = l[n].w0 * l[n].w0 * (1.0 + z_sq / zR_sq), inv_w = 1.0 / sqrt(w2), inv_w2 = 1.0 / w2;
	
	double k_over_r = (k * r_vec_local[2]) / den, rho2 = r_vec_local[0] * r_vec_local[0] + r_vec_local[1] * r_vec_local[1];
	double dw2_dzp = 2.0 * l[n].w0 * l[n].w0 * r_vec_local[2] / zR_sq, dw2_dmu = dw2_dzp * dzp_dmu;
	double dinv_w2_dmu = - inv_w2 * inv_w2 * dw2_dmu, dinv_w_over_w = - 0.5 * inv_w2 * dw2_dmu;
	
	double dk_over_R_dzp = k * (zR_sq - z_sq) / (den * den), dk_over_R_dmu = dk_over_R_dzp * dzp_dmu;
	double dgouy_dzp = zR / den, dgouy_dmu = dgouy_dzp * dzp_dmu, drho2_dmu = 2.0 * r_vec_local[0] * dxp_dmu + 2.0 * r_vec_local[1] * dyp_dmu;
	
	double U0 = (l[n].w0 * inv_w) * exp(- rho2 * inv_w2);
	double dU0_dmu = U0 * (dinv_w_over_w - (drho2_dmu * inv_w2 + rho2 * dinv_w2_dmu));
	
	double env_val = env(eta, l[n].etaf, l[n].sigma);
	double env_prime_val = env_prime(eta, l[n].etaf, l[n].sigma);
	double denv_dmu = env_prime_val * deta_dmu;
	
	double S = potentialA0 * env_val * U0;
	double dS_dmu = potentialA0 * (denv_dmu * U0 + env_val * dU0_dmu);
	
	double gouy = atan2(r_vec_local[2], zR);
	double theta_phase = eta - 0.5 * k_over_r * rho2 + gouy;
	double dTheta_dmu = deta_dmu - 0.5 * (dk_over_R_dmu * rho2 + k_over_r * drho2_dmu) + dgouy_dmu;
	
	double complex zeta_x = l[n].zeta_x_gauss, zeta_y = l[n].zeta_y_gauss;
	
	double complex phase_comp = CMPLX(cos(theta_phase), sin(theta_phase));
	double complex S_comp = potentialA0 * phase_comp * U0 * env_val;
	double complex dS_comp_dmu = potentialA0 * phase_comp * (denv_dmu * U0 + env_val * dU0_dmu + I * env_val * U0 * dTheta_dmu);
	
	double complex field_term = CMPLX(k_over_r / k, -2.0 * inv_w2 / k); 
	double complex d_field_term_dmu = CMPLX(dk_over_R_dmu / k, -2.0 * dinv_w2_dmu / k);
	
	double complex Gamma_comp = - field_term * (zeta_x * r_vec_local[0] + zeta_y * r_vec_local[1]);
	double complex dGamma_comp_dmu = - d_field_term_dmu * (zeta_x * r_vec_local[0] + zeta_y * r_vec_local[1]) - field_term * (zeta_x * dxp_dmu + zeta_y * dyp_dmu);
	
	double Axp_deriv = - cimag(dS_comp_dmu * zeta_x);
	double Ayp_deriv = - cimag(dS_comp_dmu * zeta_y);
	double Azp_deriv = - cimag(dS_comp_dmu * Gamma_comp + S_comp * dGamma_comp_dmu);
	
	for(int i = 0; i < 3; i++)
		a[i+1] = Axp_deriv * l[n].epsilon1[i] + Ayp_deriv * l[n].epsilon2[i] + Azp_deriv * l[n].n[i];
}

static inline void potential_a_phi(double *a, double eta, const Laser *restrict l, int n) {
	double potentialA0 = l[n].a0 * m * c / fabs(q);
	double epsilon4[3], k_vec[3], A0mult;
	
	copy_vec(k_vec, l[n].n);
	mult_vec(k_vec, k_vec, l[n].omega / c);
	eta += l[n].psi;
	
	A0mult = env(eta, l[n].etaf, l[n].sigma) * potentialA0;
	for(int i = 0; i < 3; i++)
		a[i] = l[n].epsilon1[i] * l[n].zetax * (sin(eta)) + l[n].epsilon2[i] * l[n].zetay * cos(eta);
	mult_vec(a, a, A0mult);
}

#endif