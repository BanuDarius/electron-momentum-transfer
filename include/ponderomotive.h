#ifndef PONDEROMOTIVE_H
#define PONDEROMOTIVE_H

struct laser;
void potential_deriv_a(double *a, double *u, struct laser *l, int index, int n);
void potential_a(double *a, double *u, struct laser *l, int n);
double integrate(double *u, struct laser *l);
double integrate_dmuda(double *u, struct laser *l, int index);
double compute_a(double *u, struct laser *l);
double derivative_a(double *u, struct laser *l, int index);
void ponderomotive(double *u, double *up);
void set_mode(void (**compute_function)(double *, double *), int mode);

#endif