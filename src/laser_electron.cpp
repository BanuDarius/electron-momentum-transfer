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

#include "init.h"

void *Simulate(void *data) {
	struct SharedData *sdata = (struct SharedData*)data;
	struct Particle *e = sdata->e;
	struct Laser *l = sdata->l;

	int id = sdata->id;
	int num = sdata->num;
	FILE *out = sdata->out;
	int steps = sdata->steps;
	double dtau = sdata->dtau;
	double *ochunk = sdata->ochunk;
	int initIndex = sdata->initIndex;
	int finalIndex = sdata->finalIndex;
	int outputMode = sdata->outputMode;

	boost::numeric::odeint::runge_kutta4<std::array<double, U_SIZE>> stepper;

	double tau;
	unsigned int chunkC = 0;
	auto arrayFC = [&](const std::array<double, U_SIZE> &u, std::array<double, U_SIZE> &up, double t) {
		sdata->fc(const_cast<double*>(u.data()), up.data(), t);
	}; //Complicated data transformation...
	std::array<double, U_SIZE> newV;
	
	bool run = true;

	if(outputMode == 0) {
		finalIndex = num;
		if(id != 0)
			run = false;
	}

	if(run)
	for(int k = initIndex; k < finalIndex; k++) {
		tau = 0;
		CopyInitial(ochunk, e[k].u, (k - initIndex) % CHUNK_SIZE, id);
		for(int i = 0; i < steps; i++) {
			std::copy(e[k].u, e[k].u + U_SIZE, newV.begin());
			stepper.do_step(arrayFC, newV, tau, dtau);
			std::copy(newV.begin(), newV.end(), e[k].u);
			tau += dtau;
			if(outputMode == 0 && id == 0) {
				double outVec[8];
				SetVec(outVec, &e[k].u[0], 8);
				/*double average = ComputeAverage(outVec, l);
				double time = outVec[0] / c;
				fwrite(&time, sizeof(double), 1, out);
				fwrite(&average, sizeof(double), 1, out);*/
				fwrite(outVec, sizeof(double), 8, out);
			}
		}
		if(outputMode == 1) {
			for(int j = U_SIZE; j < 2 * U_SIZE; j++) {
				ochunk[id * 2 * U_SIZE * CHUNK_SIZE + chunkC + j] = e[k].u[j - U_SIZE];
			}
			chunkC += 2 * U_SIZE;
			if((k + 1) % CHUNK_SIZE == 0 && k - initIndex != 0) {
				pthread_barrier_wait(&barrierCompute);
				if(id == 0) {
					printf("Particles processed: %i/%i.\n", CORE_NUM * (k - initIndex + 1), CORE_NUM * finalIndex);
					PrintChunk(out, ochunk);
					SetZeroN(ochunk, 2 * U_SIZE * CHUNK_SIZE * CORE_NUM);
				}
				chunkC = 0;
				pthread_barrier_wait(&barrierSync);
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
	int mode = atoi(argv[1]), outputMode = atoi(argv[2]);
	double a0 = atof(argv[3]);
	double omega = 0.057;
	double E0 = omega * c * a0;
	double tauf = atof(argv[8]), dtau = tauf / steps;
	double wavelength = 2.0 * pi * c / omega;
	double r = atoi(argv[6]) * wavelength, h = 0.0, z = 0.0, xif = atof(argv[7]);
	double alpha = pi / 2.0, beta = 0.0;
	pthread_barrier_init(&barrierSync, NULL, CORE_NUM);
	pthread_barrier_init(&barrierCompute, NULL, CORE_NUM);

	l = (struct Laser*)malloc(2 * sizeof(struct Laser));
	struct Particle *e = (struct Particle*)malloc(num * sizeof(struct Particle));
	double *ochunk = NewVec(2 * U_SIZE * CHUNK_SIZE * CORE_NUM);
	struct SharedData *sdata = (struct SharedData*)malloc(CORE_NUM * sizeof(struct SharedData));
	void (*computeFunction)(double*, double*, double);

	CheckErrors(out, sdata);
	SetInitialVel(vi, 0.0, 0.0, 0.0);
	SetMode(&computeFunction, mode);
	//Mode "0" for electromagnetic, "1" for ponderomotive
	SetLaser(&l[0], E0, -alpha, beta, xif, omega, -120.0 * pi);
	SetLaser(&l[1], E0, alpha, -beta, xif, omega, -120.0 * pi);
	SetParticles(e, num, r, h, z, pi / 2.0, pi / 2.0, vi, outputMode);
	//Output mode "0" for all positions and velocities, "1" for only the final positions and velocities
	SetSharedData(sdata, e, l, out, ochunk, num, steps, dtau, outputMode, computeFunction);

	printf("Start simulation.\n");
	for(int i = 0; i < CORE_NUM; i++)
		pthread_create(&thread[i], NULL, Simulate, (void*)&sdata[i]);
	for(int i = 0; i < CORE_NUM; i++)
		pthread_join(thread[i], NULL);

	fclose(out);
	printf("Simulation ended.\n");
	printf("Time taken: %0.3fs.\n", (double)(clock() - ti) / (CLOCKS_PER_SEC * CORE_NUM));
	pthread_barrier_destroy(&barrierCompute);
	pthread_barrier_destroy(&barrierSync);
	return 0;
}

