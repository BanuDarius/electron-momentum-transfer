#ifndef PONDEROMOTIVE_H
#define PONDEROMOTIVE_H

void potential_deriv_a(double *a, double *u, struct laser *l, int index, int n);
void potential_a(double *a, double *u, struct laser *l, int n);
double integrate(double *u, struct laser *l);
double integrate_dmuda(double *u, struct laser *l, int index);
double compute_a(double *u, struct laser *l);
double derivative_a(double *u, struct laser *l, int index);
void ponderomotive(double *u, double *up, struct laser *l);
void set_mode(void (**compute_function)(double *, double *, struct laser *l), int mode);

#endif