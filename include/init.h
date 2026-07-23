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

#ifndef INIT_H
#define INIT_H

#include "sim_structs.h"

void compute_e(double *E, double *u, const Laser *restrict l, int i);
void compute_b(double *B, double *E, double *u, const Laser *restrict l, int i);
void compute_e_b(double *E, double *B, double *u, const Laser *restrict l);
void electromag(double *restrict u, double *restrict up, const Laser *restrict l);
void ponderomotive(double *restrict u, double *restrict up, const Laser *restrict l);
void set_position(double *u, double r_min, double r_max, int i, int num, int output_mode);
void set_initial_vel(double *vi, double v_mag, double phi, double theta);
void set_particles(Particles *p, Parameters *param, double *vi);
double *create_out_chunk(Parameters *param);
void set_mode(void (**compute_function)(double *restrict, double *restrict, const Laser *restrict), int mode);
void set_parameters(Parameters *param, char *input);
void set_lasers(Laser *l, Parameters *param, char *input);

#endif