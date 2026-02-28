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

#include "units.h"
#include "math_tools.h"
#include "potentials.h"

void potential_a(double *a, double *u, const struct laser *restrict l, int n) {
	double potentialA0 = l[n].a0 * m * c / fabs(q);
	double epsilon4[4], k_vec4[4], phi, A0mult;
	
	a[0] = 0.0;
	k_vec4[0] = 1.0;
	epsilon4[0] = 0.0;
	memcpy(&k_vec4[1], l[n].n, 3 * sizeof(double));
	mult_vec4(k_vec4, k_vec4, l[n].omega / c);
	
	phi = dot4(k_vec4, u) + l[n].psi;
	A0mult = env(phi, l[n].xif, l[n].sigma) * potentialA0;
	for(int i = 0; i < 3; i++)
		a[i+1] = l[n].epsilon1[i] * l[n].zetax * (sin(phi)) + l[n].epsilon2[i] * l[n].zetay * cos(phi);
	mult_vec(&a[1], &a[1], A0mult);
}

void potential_deriv_a(double *a, double *u, const struct laser *restrict l, int index, int n) {
	double potentialA0 = l[n].a0 * m * c / fabs(q);
	double epsilon4[4], k_vec4[4], phi, sign;
	
	a[0] = 0.0;
	k_vec4[0] = 1.0;
	epsilon4[0] = 0.0;
	memcpy(&k_vec4[1], l[n].n, 3 * sizeof(double));
	mult_vec4(k_vec4, k_vec4, l[n].omega / c);
	
	phi = dot4(k_vec4, u) + l[n].psi;
	sign = (index > 0) ? -1.0 : +1.0;
	for(int i = 0; i < 3; i++) {
		double t1 = l[n].epsilon1[i] * l[n].zetax * (sin(phi)) + l[n].epsilon2[i] * l[n].zetay * (cos(phi));
		double t2 = l[n].epsilon1[i] * l[n].zetax * (cos(phi)) + l[n].epsilon2[i] * l[n].zetay * (-sin(phi));
		a[i+1] = sign * potentialA0 * k_vec4[index] * (env(phi, l[n].xif, l[n].sigma) * t2 + env_prime(phi, l[n].xif, l[n].sigma) * t1);
	}
}

void potential_a_phi(double *a, double phi, const struct laser *restrict l, int n) {
	double potentialA0 = l[n].a0 * m * c / fabs(q);
	double epsilon4[3], k_vec[3], A0mult;
	
	memcpy(k_vec, l[n].n, 3 * sizeof(double));
	mult_vec(k_vec, k_vec, l[n].omega / c);
	phi += l[n].psi;
	
	A0mult = env(phi, l[n].xif, l[n].sigma) * potentialA0;
	for(int i = 0; i < 3; i++)
		a[i] = l[n].epsilon1[i] * l[n].zetax * (sin(phi)) + l[n].epsilon2[i] * l[n].zetay * cos(phi);
	mult_vec(a, a, A0mult);
}