#include <omp.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#include "init.h"
#include "extra.h"
#include "ponderomotive.h"

void simulate(struct parameters *param, void (*compute_function)(double *, double *, struct laser *), FILE *out, double *out_chunk, struct laser *l, struct particle *p) {
	int num = param->num;
	int steps = param->steps;
	int substeps = param->substeps;
	int core_num = param->core_num;
	int output_mode = param->output_mode;
	
	double dtau = param->dtau;
	
	#pragma omp parallel num_threads(core_num)
	{
		int chunk_current = 0;
		int id = omp_get_thread_num();
		int initial_idx = initial_index(num, id, core_num);
		int final_idx = final_index(num, id, core_num);
		
		for(int k = initial_idx; k < final_idx; k++) {
			if(output_mode == 1)
				copy_initial(out_chunk, p[k].u, (k - initial_idx) % CHUNK_SIZE, id);
			for(int i = 0; i < steps; i++) {
				rk4_step(&p[k].u[0], dtau, l, compute_function);
				
				if(output_mode == 0 && i % substeps == 0) {
					int idx = id * U_SIZE * steps * num / (substeps * core_num) + (k - initial_idx) * U_SIZE * steps / substeps + i * U_SIZE / substeps;
					memcpy(&out_chunk[idx], &p[k].u[0], sizeof(double) * U_SIZE);
					#pragma omp master
					{
						if((k + 1) % CHUNK_SIZE == 0 && i == 0) {
							int current = core_num * (k - initial_idx + 1);
							int total = core_num * final_idx;
							printf("Particles processed: %i/%i.\n", current, total);
						}
					}
				}
			}
			
			if(output_mode == 1) {
				#pragma omp barrier
				for(int j = U_SIZE; j < 2 * U_SIZE; j++) {
					out_chunk[id * 2 * U_SIZE * CHUNK_SIZE + chunk_current + j] = p[k].u[j - U_SIZE];
				}
				chunk_current += 2 * U_SIZE;
				if((k + 1) % CHUNK_SIZE == 0 && k - initial_idx != 0) {
					#pragma omp master
					{
						int current = core_num * (k - initial_idx + 1);
						int total = core_num * final_idx;
						printf("Particles processed: %i/%i.\n", current, total);
						print_chunk(out, out_chunk, core_num);
						set_zero_n(out_chunk, 2 * U_SIZE * CHUNK_SIZE * core_num);
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
	FILE *out = fopen(argv[12], "wb");
	
	double vi[3], alpha = pi / 2.0, beta = 0.0;
	struct parameters *param = malloc(sizeof(struct parameters));
	set_parameters(param, argv);
	
	struct laser *l = malloc(NUM_LASERS * sizeof(struct laser));
	struct particle *p = malloc(param->num * sizeof(struct particle));
	double *out_chunk = create_out_chunk(param->output_mode, param->num, param->steps, param->substeps, param->core_num);
	void (*compute_function)(double *, double *, struct laser *);
	
	if(!l || !p || !out_chunk) { perror("Memory allocation error."); abort(); }
	
	set_initial_vel(vi, 0.0, 0.0, 0.0);
	set_mode(&compute_function, param->mode);
	//Mode "0" for electromagnetic, "1" for ponderomotive
	set_laser(&l[0], param->E0, -alpha, beta, param->xif, param->omega, param->sigma, -60.0 * pi);
	set_laser(&l[1], param->E0, alpha, -beta, param->xif, param->omega, param->sigma, -60.0 * pi);
	set_particles(p, param->num, param->r, param->h, param->z, pi / 2.0, pi / 2.0, vi, param->output_mode);
	//Output mode "0" for all positions and velocities, "1" for only the final positions and velocities
	
	printf("Simulation started.\n");
	simulate(param, compute_function, out, out_chunk, l, p);
	printf("Simulation ended.\n");
	
	printf("Time taken: %0.3fs.\n", (double)(clock() - ti) / (CLOCKS_PER_SEC * param->core_num));
	free(out_chunk); free(param); free(p);
	fclose(out);
	return 0;
}

