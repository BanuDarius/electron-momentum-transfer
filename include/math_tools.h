#ifndef H_MATH_TOOLS
#define H_MATH_TOOLS

#include <math.h>

//This file includes optimized general purpose math functions

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