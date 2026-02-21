#ifndef SIM_STRUCTS_H
#define SIM_STRUCTS_H

#include <stdio.h>
#include <stdalign.h>

#define LASER_PARAMS 11 //This defines how many parameters will be read from a file for one laser
#define PARAMS 12 //This defines how many parameters will be read from a file for the general simulation
#define U_SIZE 8 //Number of elements of the particle struct
#define CHUNK_SIZE 100 //Number of particles in an output chunk

struct particle {
	alignas(64) double u[U_SIZE];
}; //This struct has sizeof(struct particle) = 64 bytes, which is conveniently equal to a standard cache line

struct laser {
	int num_lasers, pond_integrate_steps;
	double alpha, sigma, zetax, zetay, omega, theta, phi, psi, xif, a0;
	double epsilon1[3], epsilon2[3], n[3];
};

struct parameters {
	double rotate_angle, r_min, r_max, tf, dt, h, z;
	int num, num_lasers, steps, substeps, mode, output_mode, check_polarization, thread_num;
};

#endif