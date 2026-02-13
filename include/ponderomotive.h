#ifndef PONDEROMOTIVE_H
#define PONDEROMOTIVE_H

void potential_deriv_a(double *a, double *u, const struct laser *restrict l, int index, int n);
void potential_a(double *a, double *u, const struct laser *restrict l, int n);
double integrate(double *u, const struct laser *restrict l);
double integrate_dmuda(double *u, const struct laser *restrict l, int index);
double compute_a(double *u, const struct laser *restrict l);
double derivative_a(double *u, const struct laser *restrict l, int index);
void ponderomotive(double *restrict u, double *restrict up, const struct laser *restrict l);

#endif