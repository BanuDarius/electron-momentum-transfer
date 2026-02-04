#include <omp.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#include "init.h"
#include "extra.h"
#include "ponderomotive.h"

void simulate(FILE *out, struct particle *e, struct laser *l, double *out_chunk, int output_mode, int num, int steps, int substeps, double dtau, void (*compute_function)(double *, double *, struct laser *)) {
	#pragma omp parallel
	{
		int chunk_current = 0;
		int id = omp_get_thread_num();
		int initial_idx = initial_index(num, id);
		int final_idx = final_index(num, id);
		
		for(int k = initial_idx; k < final_idx; k++) {
			if(output_mode == 1)
				copy_initial(out_chunk, e[k].u, (k - initial_idx) % CHUNK_SIZE, id);
			for(int i = 0; i < steps; i++) {
				rk4_step(&e[k].u[0], dtau, l, compute_function);
				
				if(output_mode == 0 && i % substeps == 0) {
					int idx = id * U_SIZE * steps * num / (substeps * CORE_NUM) + (k - initial_idx) * U_SIZE * steps / substeps + i * U_SIZE / substeps;
					memcpy(&out_chunk[idx], &e[k].u[0], sizeof(double) * U_SIZE);
					#pragma omp master
					{
						if((k + 1) % CHUNK_SIZE == 0 && i == 0) {
							int current = CORE_NUM * (k - initial_idx + 1);
							int total = CORE_NUM * final_idx;
							printf("Particles processed: %i/%i.\n", current, total);
						}
					}
				}
			}
			
			if(output_mode == 1) {
				#pragma omp barrier
				for(int j = U_SIZE; j < 2 * U_SIZE; j++) {
					out_chunk[id * 2 * U_SIZE * CHUNK_SIZE + chunk_current + j] = e[k].u[j - U_SIZE];
				}
				chunk_current += 2 * U_SIZE;
				if((k + 1) % CHUNK_SIZE == 0 && k - initial_idx != 0) {
					#pragma omp master
					{
						int current = CORE_NUM * (k - initial_idx + 1);
						int total = CORE_NUM * final_idx;
						printf("Particles processed: %i/%i.\n", current, total);
						print_chunk(out, out_chunk);
						set_zero_n(out_chunk, 2 * U_SIZE * CHUNK_SIZE * CORE_NUM);
					}
					#pragma omp barrier
					chunk_current = 0;
				}
			}
		}
	}
	
	#pragma omp barrier
	if(output_mode == 0)
		fwrite(out_chunk, sizeof(double), U_SIZE * steps * num / substeps, out);
}

int main(int argc, char **argv) {
	srand(128);
	clock_t ti = clock();
	FILE *out = fopen(argv[11], "wb");
	
	double vi[3], alpha = pi / 2.0, beta = 0.0;
	int num = atoi(argv[4]), steps = atoi(argv[5]);
	int mode = atoi(argv[1]), output_mode = atoi(argv[2]), substeps = atoi(argv[9]);
	double a0 = atof(argv[3]), omega = 0.057, wavelength = 2.0 * pi * c / omega;
	double E0 = omega * c * a0, tauf = atof(argv[8]), sigma = atof(argv[10]), dtau = tauf / steps;
	double r = atoi(argv[6]) * wavelength, h = 0.0, z = 0.0, xif = atof(argv[7]);
	
	struct laser *l = malloc(NUM_LASERS * sizeof(struct laser));
	struct particle *e = malloc(num * sizeof(struct particle));
	double *out_chunk = create_out_chunk(output_mode, num, steps, substeps);
	void (*compute_function)(double *, double *, struct laser *);
	
	if(!l || !e || !out_chunk) { perror("Memory allocation error."); abort(); }
	
	set_initial_vel(vi, 0.0, 0.0, 0.0);
	set_mode(&compute_function, mode);
	//Mode "0" for electromagnetic, "1" for ponderomotive
	set_laser(&l[0], E0, -alpha, beta, xif, omega, sigma, -60.0 * pi);
	set_laser(&l[1], E0, alpha, -beta, xif, omega, sigma, -60.0 * pi);
	set_particles(e, num, r, h, z, pi / 2.0, pi / 2.0, vi, output_mode);
	//Output mode "0" for all positions and velocities, "1" for only the final positions and velocities
	
	printf("Simulation started.\n");
	simulate(out, e, l, out_chunk, output_mode, num, steps, substeps, dtau, compute_function);
	printf("Simulation ended.\n");
	
	printf("Time taken: %0.3fs.\n", (double)(clock() - ti) / (CLOCKS_PER_SEC * CORE_NUM));
	free(out_chunk); free(e);
	fclose(out);
	return 0;
}

