#ifndef POTENTIALS_H
#define POTENTIALS_H

#include "sim_structs.h"

void potential_a(double *a, double *u, const struct laser *restrict l, int n);
void potential_deriv_a(double *a, double *u, const struct laser *restrict l, int index, int n);
void potential_a_phi(double *a, double phi, const struct laser *restrict l, int n);

#endif