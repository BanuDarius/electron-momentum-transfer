#ifndef EXTRA_H
#define EXTRA_H

#include <stdio.h>

#include "init.h"

#define U_SIZE 8
#define NUM_LASERS 2
#define CHUNK_SIZE 100
#define PONDEROMOTIVE_STEPS 4
#define DEG_TO_RAD (pi / 180.0)

static const double m = 1.0; //The mass of an electron in atomic units.
static const double q = -1.0; //The electric charge of an electron in atomic units.
static const double c = 137.036; //The speed of light in a.u.
static const double pi = 3.1415926535;

//These are the function declarations implemented in extra.c

double rand_val(double min, double max);
void print_chunk(FILE *out, double *chunk, int core_num);
void copy_initial(double *ch, double *u, int k, int id);
void set_chunk(double *out_chunk, double *chunk, int init, int fin);
void set_vec(double *u1, double *u2, int n);
double *new_vec(int n);
void set_zero(double *u);
void set_zero_n(double *u, int n);
void mult_vec(double *u, double a);
void mult_vec4(double *u, double a);
void add_vec(double *u, double *v);
void add_vec4(double *u, double *v);
void sub_vec(double *x, double *u, double *v);
void cross(double *a, double *b, double *u);
double dot(double *a, double *b);
double dot4(double *u, double *v);
double magnitude(double *a);
double compute_gamma(double *v);
void rotate(double *u, double phi, double theta);
double *direction_vec(double phi_l, double theta_l);
void epsilon(double *u, double *w);
double env(double xi, double xif, double sigma);
double env_prime(double xi, double xif, double sigma);
void rk4_step(double *u, double dt, struct laser *l, void compute_function(double *, double *, struct laser *));
int initial_index(int n, int thread_num, int core_num);
int final_index(int n, int thread_num, int core_num);

#endif