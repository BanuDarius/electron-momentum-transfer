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
	double k_vec4[4], eta, k = l[n].omega / c;
	
	a[0] = 0.0;
	k_vec4[0] = 1.0;
	copy_vec(&k_vec4[1], l[n].n);
	mult_vec4(k_vec4, k_vec4, l[n].omega / c);
	
	eta = dot4(k_vec4, u) + l[n].psi;
	double xp = u[1] * l[n].epsilon1[0] + u[2] * l[n].epsilon1[1] + u[3] * l[n].epsilon1[2];
	double yp = u[1] * l[n].epsilon2[0] + u[2] * l[n].epsilon2[1] + u[3] * l[n].epsilon2[2];
	double zp = u[1] * l[n].n[0] + u[2] * l[n].n[1] + u[3] * l[n].n[2];
	
	double zR = 0.5 * k * l[n].w0 * l[n].w0, z_sq = zp * zp, zR_sq = zR * zR;
	double w2 = l[n].w0 * l[n].w0 * (1.0 + z_sq / zR_sq), inv_w = 1.0 / sqrt(w2), inv_w2 = 1.0 / w2;
	
	double k_over_r = (k * zp) / (z_sq + zR_sq), rho2 = xp * xp + yp * yp;
	double gouy = atan2(zp, zR), theta_phase = eta - 0.5 * k_over_r * rho2 + gouy;
	
	double U0 = (l[n].w0 * inv_w) * exp(-rho2 * inv_w2);
	double A0mult = potentialA0 * U0 * env(eta, l[n].etaf, l[n].sigma);
	
	double Axp = l[n].zetax * sin(theta_phase), Ayp = l[n].zetay * cos(theta_phase);
	double term_cos = 2.0 * l[n].zetax * xp * inv_w2 - k_over_r * l[n].zetay * yp;
	double term_sin = k_over_r * l[n].zetax * xp + 2.0 * l[n].zetay * yp * inv_w2;
	double Azp = (1.0 / k) * (term_cos * cos(theta_phase) - term_sin * sin(theta_phase));
	
	for(int i = 0; i < 3; i++)
		a[i+1] = A0mult * (Axp * l[n].epsilon1[i] + Ayp * l[n].epsilon2[i] + Azp * l[n].n[i]);
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
	double k_vec4[4], eta, sign, k = l[n].omega / c;
	
	a[0] = 0.0;
	k_vec4[0] = 1.0;
	copy_vec(&k_vec4[1], l[n].n);
	mult_vec4(k_vec4, k_vec4, l[n].omega / c);
	
	eta = dot4(k_vec4, u) + l[n].psi;
	sign = (index > 0) ? -1.0 : +1.0;
	double deta_dmu = sign * k_vec4[index]; 
	double dxp_dmu = 0.0, dyp_dmu = 0.0, dzp_dmu = 0.0;
	if (index > 0) {
		dxp_dmu = l[n].epsilon1[index - 1];
		dyp_dmu = l[n].epsilon2[index - 1];
		dzp_dmu = l[n].n[index - 1];
	}
	double xp = u[1] * l[n].epsilon1[0] + u[2] * l[n].epsilon1[1] + u[3] * l[n].epsilon1[2];
	double yp = u[1] * l[n].epsilon2[0] + u[2] * l[n].epsilon2[1] + u[3] * l[n].epsilon2[2];
	double zp = u[1] * l[n].n[0] + u[2] * l[n].n[1] + u[3] * l[n].n[2];
	
	double zR = 0.5 * k * l[n].w0 * l[n].w0, z_sq = zp * zp, zR_sq = zR * zR, den = z_sq + zR_sq;
	double w2 = l[n].w0 * l[n].w0 * (1.0 + z_sq / zR_sq), inv_w = 1.0 / sqrt(w2), inv_w2 = 1.0 / w2;
	
	double k_over_r = (k * zp) / den, rho2 = xp * xp + yp * yp;
	double dw2_dzp = 2.0 * l[n].w0 * l[n].w0 * zp / zR_sq, dw2_dmu = dw2_dzp * dzp_dmu;
	double dinv_w2_dmu = -inv_w2 * inv_w2 * dw2_dmu, dinv_w_over_w = -0.5 * inv_w2 * dw2_dmu;
	
	double dk_over_R_dzp = k * (zR_sq - z_sq) / (den * den), dk_over_R_dmu = dk_over_R_dzp * dzp_dmu;
	double dgouy_dzp = zR / den, dgouy_dmu = dgouy_dzp * dzp_dmu, drho2_dmu = 2.0 * xp * dxp_dmu + 2.0 * yp * dyp_dmu;
	
	double U0 = (l[n].w0 * inv_w) * exp(-rho2 * inv_w2);
	double dU0_dmu = U0 * (dinv_w_over_w - (drho2_dmu * inv_w2 + rho2 * dinv_w2_dmu));
	
	double env_val = env(eta, l[n].etaf, l[n].sigma);
	double env_prime_val = env_prime(eta, l[n].etaf, l[n].sigma);
	double denv_dmu = env_prime_val * deta_dmu;
	
	double S = potentialA0 * env_val * U0;
	double dS_dmu = potentialA0 * (denv_dmu * U0 + env_val * dU0_dmu);
	
	double gouy = atan2(zp, zR);
	double theta_phase = eta - 0.5 * k_over_r * rho2 + gouy;
	double dTheta_dmu = deta_dmu - 0.5 * (dk_over_R_dmu * rho2 + k_over_r * drho2_dmu) + dgouy_dmu;
	
	double Px = l[n].zetax * sin(theta_phase), Py = l[n].zetay * cos(theta_phase);
	
	double dPx_dmu = l[n].zetax * cos(theta_phase) * dTheta_dmu;
	double dPy_dmu = -l[n].zetay * sin(theta_phase) * dTheta_dmu;
	
	double Gamma_r = 2.0 * l[n].zetax * xp * inv_w2 - k_over_r * l[n].zetay * yp;
	double Gamma_i = 2.0 * l[n].zetay * yp * inv_w2 + k_over_r * l[n].zetax * xp;
	
	double dGamma_r_dmu = 2.0 * l[n].zetax * (dxp_dmu * inv_w2 + xp * dinv_w2_dmu) - l[n].zetay * (dyp_dmu * k_over_r + yp * dk_over_R_dmu);
	double dGamma_i_dmu = 2.0 * l[n].zetay * (dyp_dmu * inv_w2 + yp * dinv_w2_dmu) + l[n].zetax * (dxp_dmu * k_over_r + xp * dk_over_R_dmu);
	
	double Pz = (1.0 / k) * (Gamma_r * cos(theta_phase) - Gamma_i * sin(theta_phase));
	double dPz_dmu = (1.0 / k) * ((dGamma_r_dmu - Gamma_i * dTheta_dmu) * cos(theta_phase) - (dGamma_i_dmu + Gamma_r * dTheta_dmu) * sin(theta_phase));
	
	double Axp_deriv = dS_dmu * Px + S * dPx_dmu;
	double Ayp_deriv = dS_dmu * Py + S * dPy_dmu;
	double Azp_deriv = dS_dmu * Pz + S * dPz_dmu;
	
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