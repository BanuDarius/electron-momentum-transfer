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

#ifndef MATH_TOOLS_H
#define MATH_TOOLS_H

#include <math.h>

#include "units.h"

//This file includes optimized general purpose math functions

static inline void mult_vec(double *u, double *v, const double a) {
	for(int i = 0; i < 3; i++)
		u[i] = v[i] * a;
}

static inline void mult_vec4(double *u, double *v, const double a) {
	for(int i = 0; i < 4; i++)
		u[i] = v[i] * a;
}

static inline void add_vec(double *a, double *b, double *c) {
	for(int i = 0; i < 3; i++)
		a[i] = b[i] + c[i];
}

static inline void add_vec4(double *a, double *b, double *c) {
	for(int i = 0; i < 4; i++)
		a[i] = b[i] + c[i];
}

static inline void cross(double *u, const double *a, const double *b) {
	u[0] = a[1] * b[2] - a[2] * b[1];
	u[1] = a[2] * b[0] - a[0] * b[2];
	u[2] = a[0] * b[1] - a[1] * b[0];
}

static inline double dot(const double *a, const double *b) {
	double x = a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
	return x;
}

static inline double dot4(const double *a, const double *b) {
	double x = a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3];
	return x;
}

static inline double magnitude(const double *a) {
	double x = sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);
	return x;
}

static inline double comp_gamma(const double *p) {
	double mag = magnitude(p);
	double gamma = sqrt(1.0 + (mag * mag) / (m * m * c * c));
	return gamma;
}

//These functions are for the envelope

static inline double env(const double xi, const double xif, const double sigma) {
	if(xi > -xif && xi < xif)
		return 1.0;
	else if(xi >= xif)
		return exp(-(xi - xif) * (xi - xif) / (sigma * sigma));
	else
		return exp(-(xi + xif) * (xi + xif) / (sigma * sigma));
}

static inline double env_prime(const double xi, const double xif, const double sigma) {
	if(xi > -xif && xi < xif)
		return 0.0;
	else if(xi >= xif)
		return - 2.0 * (xi - xif) / (sigma * sigma) * exp(-(xi - xif) * (xi - xif) / (sigma * sigma));
	else
		return - 2.0 * (xi + xif) / (sigma * sigma) * exp(-(xi + xif) * (xi + xif) / (sigma * sigma));
}

#endif