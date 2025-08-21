#include <math.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include <complex.h>

#include "Init.h"
#include "RK4.c"
#include "Debug.h"

void *Simulate(void *data) {
	struct SharedData *sdata = (struct SharedData*)data;
	struct Particle *e = sdata->e;
	struct Laser *l = sdata->l;

	int id = sdata->id;
	FILE *out = sdata->out;
	int steps = sdata->steps;
	double dtau = sdata->dtau;
	double *ochunk = sdata->ochunk;
	int initIndex = sdata->initIndex;
	int finalIndex = sdata->finalIndex;
	double *(*fc)(double, int, double*, struct Laser*) = sdata->fc;

	double tau;
	unsigned int chunkC = 0;
	double *new = NewVec(U_SIZE);

	for(int k = initIndex; k < finalIndex; k++) {
		tau = 0;
		CopyInitial(ochunk, e[k].u, (k - initIndex) % CHUNK_SIZE, id);
		for(int i = 0; i < steps; i++) {
			rk4vec(tau, U_SIZE, e[k].u, dtau, l, new, fc);
			SetVec(e[k].u, new, U_SIZE);
			tau += dtau;
			//fprintf(out, "%0.4f %0.4f %0.4f %0.4f %0.4f %0.4f %0.4f %0.4f\n", e[k].u[0], e[k].u[1], e[k].u[2], e[k].u[3], e[k].u[4], e[k].u[5], e[k].u[6], e[k].u[7]);
		}
		for(int j = U_SIZE; j < 2 * U_SIZE; j++) {
			ochunk[id * 2 * U_SIZE * CHUNK_SIZE + chunkC + j] = e[k].u[j - U_SIZE];
		}
		chunkC += 2 * U_SIZE;
		if((k + 1) % CHUNK_SIZE == 0 && k - initIndex != 0) {
			pthread_barrier_wait(&barrierCompute);
			if(id == 0) {
				printf("Chunk processed: %i/%i\n", CORE_NUM * (k - initIndex + 1), CORE_NUM * finalIndex);
				PrintChunk(out, ochunk);
				SetZeroN(ochunk, 2 * U_SIZE * CHUNK_SIZE * CORE_NUM);
			}
			chunkC = 0;
			pthread_barrier_wait(&barrierSync);
		}
	}
	return NULL;
}

int main(int argc, char **argv) {
	srand(time(NULL));
	clock_t ti = clock();
	pthread_t thread[CORE_NUM];
	char *name = SetFilename(argv[1]);
	printf("Output file: %s\n", name);
	FILE *out = fopen(name, "w");

	int num = 8000, steps = 8000;
	double a0 = atof(argv[1]);
	double E0 = 0.057 * c * a0;
	double tauf = 10000, dtau = tauf / steps;
	double r = 20000, h = 0, z = 1e-12, xif = 0.0;
	double alpha = pi / 2.0, beta = 0.0;
	pthread_barrier_init(&barrierSync, NULL, CORE_NUM);
	pthread_barrier_init(&barrierCompute, NULL, CORE_NUM);

	double *vi = malloc(3 * sizeof(double));
	struct Laser *l = malloc(2 * sizeof(struct Laser));
	struct Particle *e = malloc(num * sizeof(struct Particle));
	double *ochunk = NewVec(2 * U_SIZE * CHUNK_SIZE * CORE_NUM);
	struct SharedData *sdata = malloc(CORE_NUM * sizeof(struct SharedData));

	CheckErrors(out, sdata);
	SetInitialVel(vi, 0, 0, 0);
	SetLaser(&l[0], E0, -alpha, beta, xif, -120*pi);
	SetLaser(&l[1], E0, alpha, -beta, xif, -120*pi);
	SetParticles(e, num, r, h, z, pi / 2.0, pi / 2.0, vi);
	SetSharedData(sdata, e, l, out, ochunk, num, steps, dtau, fP2G);
	//Here "f" for lorentz force and "fP2G" for ponderomotive

	printf("Start simulation\n");
	for(int i = 0; i < CORE_NUM; i++)
		pthread_create(&thread[i], NULL, Simulate, (void*)&sdata[i]);
	for(int i = 0; i < CORE_NUM; i++)
		pthread_join(thread[i], NULL);

	printf("Simulation ended\n");
	printf("Time taken: %0.3f\n", (double)(clock() - ti) / (CLOCKS_PER_SEC));
	pthread_barrier_destroy(&barrierCompute);
	pthread_barrier_destroy(&barrierSync);
	fclose(out);
	return 0;
}
