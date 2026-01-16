/*
 Copyright 2010-2012 Karsten Ahnert
 Copyright 2011-2013 Mario Mulansky
 Copyright 2013 Pascal Germroth

 Distributed under the Boost Software License, Version 1.0.
 (See accompanying file LICENSE_1_0.bin or
 copy at http://www.boost.org/LICENSE_1_0.bin)
 */

#include <boost/numeric/odeint.hpp>
#include <math.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include <complex.h>
#include <array>
#include <algorithm>

#include "extra.h"
#include "init.h"
#include "ponderomotive.h"


void *simulate(void *data) {
	struct shared_data *sdata = (struct shared_data*)data;
	struct particle *e = sdata->e;
	struct laser *l = sdata->l;

	int id = sdata->id;
	int num = sdata->num;
	FILE *out = sdata->out;
	int steps = sdata->steps;
	double dtau = sdata->dtau;
	double *ochunk = sdata->ochunk;
	int initial_index = sdata->initial_index;
	int final_index = sdata->final_index;
	int output_mode = sdata->output_mode;

	boost::numeric::odeint::runge_kutta4<std::array<double, U_SIZE>> stepper;

	double tau;
	unsigned int chunk_current = 0;
	auto arrayFC = [&](const std::array<double, U_SIZE> &u, std::array<double, U_SIZE> &up, double t) {
		sdata->fc(const_cast<double*>(u.data()), up.data(), t);
	}; //Complicated data transformation...
	std::array<double, U_SIZE> newV;
	
	bool run = true;

	if(output_mode == 0) {
		final_index = num;
		if(id != 0)
			run = false;
	}

	if(run)
	for(int k = initial_index; k < final_index; k++) {
		tau = 0;
		copy_initial(ochunk, e[k].u, (k - initial_index) % CHUNK_SIZE, id);
		for(int i = 0; i < steps; i++) {
			std::copy(e[k].u, e[k].u + U_SIZE, newV.begin());
			stepper.do_step(arrayFC, newV, tau, dtau);
			std::copy(newV.begin(), newV.end(), e[k].u);
			tau += dtau;
			if(output_mode == 0 && id == 0)
				fwrite(&e[k].u[0], sizeof(double), 8, out);
		}
		if(output_mode == 1) {
			for(int j = U_SIZE; j < 2 * U_SIZE; j++) {
				ochunk[id * 2 * U_SIZE * CHUNK_SIZE + chunk_current + j] = e[k].u[j - U_SIZE];
			}
			chunk_current += 2 * U_SIZE;
			if((k + 1) % CHUNK_SIZE == 0 && k - initial_index != 0) {
				pthread_barrier_wait(&barrier_compute);
				if(id == 0) {
					printf("particles processed: %i/%i.\n", CORE_NUM * (k - initial_index + 1), CORE_NUM * final_index);
					print_chunk(out, ochunk);
					set_zero_n(ochunk, 2 * U_SIZE * CHUNK_SIZE * CORE_NUM);
				}
				chunk_current = 0;
				pthread_barrier_wait(&barrier_sync);
			}
		}
	}
	return NULL;
}

int main(int argc, char **argv) {
	srand(128);
	clock_t ti = clock();
	pthread_t thread[CORE_NUM];
	char name[32] = "./output/out-data.bin";
	FILE *out = fopen(name, "wb");

	double vi[3];
	int num = atoi(argv[4]), steps = atoi(argv[5]);
	int mode = atoi(argv[1]), output_mode = atoi(argv[2]);
	double a0 = atof(argv[3]);
	double omega = 0.057;
	double E0 = omega * c * a0;
	double tauf = atof(argv[8]), dtau = tauf / steps;
	double wavelength = 2.0 * pi * c / omega;
	double r = atoi(argv[6]) * wavelength, h = 0.0, z = 0.0, xif = atof(argv[7]);
	double alpha = pi / 2.0, beta = 0.0;
	pthread_barrier_init(&barrier_sync, NULL, CORE_NUM);
	pthread_barrier_init(&barrier_compute, NULL, CORE_NUM);

	l = (struct laser*)malloc(2 * sizeof(struct laser));
	struct particle *e = (struct particle*)malloc(num * sizeof(struct particle));
	double *ochunk = new_vec(2 * U_SIZE * CHUNK_SIZE * CORE_NUM);
	struct shared_data *sdata = (struct shared_data*)malloc(CORE_NUM * sizeof(struct shared_data));
	void (*compute_function)(double*, double*, double);

	check_errors(out, sdata);
	set_initial_vel(vi, 0.0, 0.0, 0.0);
	set_mode(&compute_function, mode);
	//Mode "0" for electromagnetic, "1" for ponderomotive
	set_laser(&l[0], E0, -alpha, beta, xif, omega, -60.0 * pi);
	set_laser(&l[1], E0, alpha, -beta, xif, omega, -60.0 * pi);
	set_particles(e, num, r, h, z, pi / 2.0, pi / 2.0, vi, output_mode);
	//Output mode "0" for all positions and velocities, "1" for only the final positions and velocities
	set_shared_data(sdata, e, l, out, ochunk, num, steps, dtau, output_mode, compute_function);

	printf("Start simulation.\n");
	for(int i = 0; i < CORE_NUM; i++)
		pthread_create(&thread[i], NULL, simulate, (void*)&sdata[i]);
	for(int i = 0; i < CORE_NUM; i++)
		pthread_join(thread[i], NULL);

	fclose(out);
	printf("Simulation ended.\n");
	printf("Time taken: %0.3fs.\n", (double)(clock() - ti) / (CLOCKS_PER_SEC * CORE_NUM));
	pthread_barrier_destroy(&barrier_compute);
	pthread_barrier_destroy(&barrier_sync);
	return 0;
}

