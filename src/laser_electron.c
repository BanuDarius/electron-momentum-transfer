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

#include <omp.h>
#include <time.h>
#include <math.h>
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
	FILE *out = fopen(argv[3], "wb");
	if(!out) { perror("Cannot open output file."); return 1; }
	
	double vi[3];
	set_initial_vel(vi, 0.0, 0.0, 0.0);
	struct parameters *param = malloc(sizeof(struct parameters));
	set_parameters(param, argv[1]);
	
	struct laser *l = malloc(param->num_lasers * sizeof(struct laser));
	set_lasers(l, param->num_lasers, argv[2]);
	
	struct particle *p = malloc(param->num * sizeof(struct particle));
	set_particles(p, param, vi);
	
	double *out_chunk = create_out_chunk(param);
	void (*compute_function)(double *, double *, struct laser *);
	set_mode(&compute_function, param->mode);
	
	if(!l || !p || !out_chunk) { perror("Memory allocation error."); return 1; }
	
	printf("Simulation started.\n");
	simulate(param, compute_function, out, out_chunk, l, p);
	printf("Simulation ended.\n");
	
	printf("Time taken: %0.3fs.\n", (double)(clock() - ti) / (CLOCKS_PER_SEC * param->core_num));
	free(out_chunk); free(param); free(p);
	fclose(out);
	return 0;
}

