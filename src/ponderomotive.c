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
#include "init.h"
#include "math_tools.h"
#include "ponderomotive.h"

void potential_deriv_a(double *a, double *u, const struct laser *restrict l, int index, int n) {
	double potentialA0 = l[n].a0 * m * c / fabs(q);
	double epsilon4[4], k_vec4[4];
	
	k_vec4[0] = 1.0;
	epsilon4[0] = 0.0;
	set_vec(&k_vec4[1], l[n].n, 3);
	mult_vec4(k_vec4, l[n].omega / c);
	
	double phi = dot4(k_vec4, u) + l[n].psi;
	a[0] = 0.0;
	double sign = (index > 0) ? -1.0 : +1.0;
	for(int i = 0; i < 3; i++) {
		double t1 = l[n].epsilon1[i] * l[n].zetax * (sin(phi)) + l[n].epsilon2[i] * l[n].zetay * (cos(phi));
		double t2 = l[n].epsilon1[i] * l[n].zetax * (cos(phi)) + l[n].epsilon2[i] * l[n].zetay * (-sin(phi));
		a[i+1] = sign * potentialA0 * k_vec4[index] * (env(phi, l[n].xif, l[n].sigma) * t2 + env_prime(phi, l[n].xif, l[n].sigma) * t1);
	}
}

void potential_a(double *a, double *u, const struct laser *restrict l, int n) {
	double potentialA0 = l[n].a0 * m * c / fabs(q);
	double epsilon4[4], k_vec4[4];
	
	k_vec4[0] = 1.0;
	epsilon4[0] = 0.0;
	set_vec(&k_vec4[1], l[n].n, 3);
	mult_vec4(k_vec4, l[n].omega / c);
	
	double phi = dot4(k_vec4, u) + l[n].psi;
	double A0mult = env(phi, l[n].xif, l[n].sigma) * potentialA0;
	a[0] = 0.0;
	for(int i = 0; i < 3; i++)
		a[i+1] = l[n].epsilon1[i] * l[n].zetax * (sin(phi)) + l[n].epsilon2[i] * l[n].zetay * cos(phi);
	mult_vec(&a[1], A0mult);
}

double integrate(double *u, const struct laser *restrict l) {
	double integral = 0.0;
	double a1_left[4], a1_right[4], a1_mid[4], a1_temp[4], u_temp[4];
	double lambda = 2.0 * M_PI * c / l[0].omega, dh = lambda / (double) l[0].pond_integrate_steps;
	
	set_vec(u_temp, u, 4);
	u_temp[0] -= lambda / 2.0;
	
	for(int i = 0; i < l[0].pond_integrate_steps; i++) {
		set_zero_n(a1_left, 4);
		set_zero_n(a1_mid, 4);
		set_zero_n(a1_right, 4);
		
		for(int j = 0; j < l[0].num_lasers; j++) {
			potential_a(a1_temp, u_temp, l, j);
			add_vec4(a1_left, a1_temp);
			u_temp[0] += dh / 2.0;
			
			potential_a(a1_temp, u_temp, l, j);
			add_vec4(a1_mid, a1_temp);
			u_temp[0] += dh / 2.0;
			
			potential_a(a1_temp, u_temp, l, j);
			add_vec4(a1_right, a1_temp);
			
			u_temp[0] -= dh;
		}
		
		integral += dh / 6.0 * (dot4(a1_left, a1_left) + 4.0 * dot4(a1_mid, a1_mid) + dot4(a1_right, a1_right));
		u_temp[0] += dh;
	}
	return integral;
}

double integrate_dmuda(double *u, const struct laser *restrict l, int index) {
	double integral = 0.0;
	double a1_left[4], a1_right[4], a1_mid[4], a2_left[4], a2_right[4], a2_mid[4], a1_temp[4], a2_temp[4], u_temp[4];
	double lambda = 2.0 * M_PI * c / l[0].omega, dh = lambda / (double) l[0].pond_integrate_steps;
	
	set_vec(u_temp, u, 4);
	u_temp[0] -= lambda / 2.0;
	
	for(int i = 0; i < l[0].pond_integrate_steps; i++) {
		set_zero_n(a1_left, 4); set_zero_n(a1_right, 4);
		set_zero_n(a1_mid, 4); set_zero_n(a2_mid, 4);
		set_zero_n(a2_left, 4); set_zero_n(a2_right, 4);
		
		for(int j = 0; j < l[0].num_lasers; j++) {
			potential_a(a1_temp, u_temp, l, j);
			potential_deriv_a(a2_temp, u_temp, l, index, j);
			add_vec4(a1_left, a1_temp);
			add_vec4(a2_left, a2_temp);
			u_temp[0] += dh / 2.0;
			
			potential_a(a1_temp, u_temp, l, j);
			potential_deriv_a(a2_temp, u_temp, l, index, j);
			add_vec4(a1_mid, a1_temp);
			add_vec4(a2_mid, a2_temp);
			u_temp[0] += dh / 2.0;
			
			potential_a(a1_temp, u_temp, l, j);
			potential_deriv_a(a2_temp, u_temp, l, index, j);
			add_vec4(a1_right, a1_temp);
			add_vec4(a2_right, a2_temp);
			
			u_temp[0] -= dh;
		}
		
		integral += dh / 6.0 * (dot4(a1_left, a2_left) + 4.0 * dot4(a1_mid, a2_mid) + dot4(a1_right, a2_right));
		u_temp[0] += dh;
	}
	return integral;
}

double compute_a(double *u, const struct laser *restrict l) {
	double lambda = 2.0 * M_PI * c / l[0].omega;
	double a = - (q * q) / (m * m * c * c) * (1.0 / lambda);
	a *= integrate(u, l);
	return a;
}

double derivative_a(double *u, const struct laser *restrict l, int index) {
	double lambda = 2.0 * M_PI * c / l[0].omega;
	double dmuda = - 2.0 * (q * q) / (m * m * c * c ) * (1.0 / lambda);
	dmuda *= integrate_dmuda(u, l, index);
	return dmuda;
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
	mult_vec4(&up[4], 1.0 / mass);
}