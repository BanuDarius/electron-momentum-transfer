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

#ifndef GAUSSIAN_H
#define GAUSSIAN_H

#include <math.h>
#include <complex.h>

#include "sim_structs.h"
#include "math_tools.h"

static inline double compute_w_z(double w0, double z, double z_r) {
	double w_z = w0 * sqrt(1.0 + z * z / (z_r * z_r));
	return w_z;
}

static inline double compute_r_z(double z, double z_r) {
	double r_z = z + z_r * z_r / z;
	return r_z;
}

static inline double compute_guoy(double z, double z_r) {
	double psi = atan(z / z_r);
	return psi;
}

static inline double compute_phi(double x, double y) {
	double phi = atan2(y, x);
	return phi;
}

static inline double complex compute_u(const Laser *laser, double r_vec[3], double r_z, double w_z) {
	double w0 = laser->w0, k = laser->omega / c, z_r = laser->z_r;
	double x = r_vec[0], y = r_vec[1], z = r_vec[2];
	double rho = sqrt(x * x + y * y);
	double w_z2 = w_z * w_z, rho2 = rho * rho;
	
	double psi_g = compute_guoy(z, z_r);
	double amplitude, phase, phi;
	
	amplitude = w0 / w_z * exp(-rho2 / w_z2);
	phase = - k * rho2 / (2.0 * r_z) + psi_g;
	
	double real = amplitude * cos(phase);
	double imag = amplitude * sin(phase);
	double complex u = CMPLX(real, imag);
	return u;
}

static inline void compute_e_b_gauss_one(double e_vec[3], double b_vec[3], const Laser *laser, double r_vec[3], double t) {
	double w0 = laser->w0, z_r = laser->z_r, etaf = laser->etaf, psi = laser->psi, sigma = laser->sigma;
	double k = laser->omega / c, E0 = laser->a0 * m * c * laser->omega / fabs(q);
	double complex zeta_x = laser->zeta_x_gauss, zeta_y = laser->zeta_y_gauss;
	double x = r_vec[0], y = r_vec[1], z = r_vec[2];
	
	double r_z = compute_r_z(z, z_r);
	double w_z = compute_w_z(w0, z, z_r);
	double eta = laser->omega * t - k * z + psi;
	
	double complex u_pm = compute_u(laser, r_vec, r_z, w_z);
	double complex phase = CMPLX(cos(eta), sin(eta));
	u_pm *= E0 * phase * env(eta, etaf, sigma);
	
	double complex field_term = CMPLX(1.0 / r_z, -2.0 / (k * w_z * w_z));
	
	double complex e_z = field_term * (zeta_x * x + zeta_y * y);
	double complex b_z = field_term * (zeta_x * y - zeta_y * x);
	
	e_vec[0] = creal(u_pm * zeta_x);
	e_vec[1] = creal(u_pm * zeta_y);
	e_vec[2] = creal(u_pm * e_z);
	
	b_vec[0] = - creal(u_pm * zeta_y) / c;
	b_vec[1] = creal(u_pm * zeta_x) / c;
	b_vec[2] = creal(u_pm * b_z) / c;
}

static inline void compute_e_b_gauss(double e_vec[3], double b_vec[3], const Laser *laser, double r_vec[3], double t) {
	double e_vec_temp[3], b_vec_temp[3];
	for(int i = 0; i < laser[0].num_lasers; i++) {
		compute_e_b_gauss_one(e_vec_temp, b_vec_temp, laser, r_vec, t);
		add_vec(e_vec, e_vec, e_vec_temp);
		add_vec(b_vec, b_vec, b_vec_temp);
	}
}

#endif