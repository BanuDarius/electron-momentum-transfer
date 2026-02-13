#ifndef H_MATH_TOOLS
#define H_MATH_TOOLS

#include <math.h>

static inline void cross(const double *a, const double *b, double *u) {
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

#endif