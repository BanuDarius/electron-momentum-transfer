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

#include <math.h>
#include <stdlib.h>
#include <string.h>

#include "init.h"
#include "tools.h"
#include "math_tools.h"

//This is a helper library which includes several simple functions

double rand_val(double min, double max) {
	double s = rand() / (double) RAND_MAX;
	return min + s * (max - min);
}

void print_chunk(FILE *out, double *chunk, int thread_num) {
	fwrite(chunk, sizeof(double), 2 * U_SIZE * CHUNK_SIZE * thread_num, out);
}

void copy_initial(double *ch, double *u, int k, int id) {
	int index = 2 * id * U_SIZE * CHUNK_SIZE + 2 * U_SIZE * k;
	for(int i = index; i < index + U_SIZE; i++)
		ch[i] = u[i - index];
}

void rotate_around_z_axis(double *u, double angle) {
	double u_temp[2] = { u[0], u[1] };
	u[0] = u_temp[0] * cos(angle) - u_temp[1] * sin(angle);
	u[1] = u_temp[0] * sin(angle) + u_temp[1] * cos(angle);
}

void set_spherical_coords(double *u, double phi, double theta) {
	double mag = magnitude(u);
	u[0] = mag * sin(phi) * cos(theta);
	u[1] = mag * sin(phi) * sin(theta);
	u[2] = mag * cos(phi);
}

void direction_vec(double *u, double phi, double theta) {
	u[0] = 0.0; u[1] = 0.0; u[2] = 1.0;
	set_spherical_coords(u, phi, theta);
}

void epsilon(double *u, double *w) {
	double v[3];
	if (fabs(u[0]) > 0.99) { 
		v[0] = 0.0; v[1] = 1.0; v[2] = 0.0;
	}
	else {
		v[0] = 1.0; v[1] = 0.0; v[2] = 0.0;
	}
	cross(w, u, v);
	double mag = magnitude(w);
	double scale = magnitude(u);
	for (int i = 0; i < 3; i++)
		w[i] = scale * w[i] / mag;
}

void rotate_polarization(double *epsilon1, double *epsilon2, double alpha) {
	double e1_temp[3], e2_temp[3];
	memcpy(e1_temp, epsilon1, 3 * sizeof(double));
	memcpy(e2_temp, epsilon2, 3 * sizeof(double));
	for(int j = 0; j < 3; j++) {
		epsilon1[j] = e1_temp[j] * cos(alpha) + e2_temp[j] * sin(alpha);
		epsilon2[j] = e2_temp[j] * cos(alpha) - e1_temp[j] * sin(alpha);
	}
}

//Manual calculation of indices for stability.

int initial_index(int n, int thread_idx, int thread_num) {
	int index = n * thread_idx / thread_num;
	return index;
}

int final_index(int n, int thread_idx, int thread_num) {
	int index = n * (thread_idx + 1) / thread_num;
	return index;
}