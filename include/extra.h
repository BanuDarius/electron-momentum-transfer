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

#ifndef EXTRA_H
#define EXTRA_H

#include <stdio.h>

#include "init.h"

#define U_SIZE 8
#define CHUNK_SIZE 100

//These are the function declarations implemented in extra.c

double rand_val(double min, double max);
void print_chunk(FILE *out, double *chunk, int core_num);
void copy_initial(double *ch, double *u, int k, int id);
void rotate_around_z_axis(double *u, double angle);
void set_spherical_coords(double *u, double phi, double theta);
void direction_vec(double *u, double phi, double theta);
void epsilon(double *u, double *w);
void rk4_step(double *u, double dt, const struct laser *restrict l, void compute_function(double *, double *, const struct laser *restrict));
void higuera_cary_step(double *u, const double dt, const struct laser *restrict l);
int initial_index(int n, int thread_num, int core_num);
int final_index(int n, int thread_num, int core_num);

#endif