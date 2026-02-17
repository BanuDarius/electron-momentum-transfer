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
#include <math.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#include "init.h"
#include "tools.h"
#include "particle_push.h"

void simulate(struct parameters *param, void (*compute_function)(double *restrict, double *restrict, const struct laser *restrict), FILE *out,
	double *out_chunk, struct laser *l, struct particle *p) {
	int num = param->num;
	int mode = param->mode;
	int steps = param->steps;
	int substeps = param->substeps;
	int thread_num = param->thread_num;
	int output_mode = param->output_mode;
	
	double dt = param->dt;
	
	#pragma omp parallel num_threads(thread_num)
	{
		int chunk_current = 0;
		int id = omp_get_thread_num();
		int initial_idx = initial_index(num, id, thread_num);
		int final_idx = final_index(num, id, thread_num);
		
		for(int k = initial_idx; k < final_idx; k++) {
			if(output_mode == 1)
				copy_initial(out_chunk, p[k].u, (k - initial_idx) % CHUNK_SIZE, id);
			for(int i = 0; i < steps; i++) {
				if(mode > 0)
					rk4_step(&p[k].u[0], dt, l, compute_function);
				else
					higuera_cary_step(&p[k].u[0], dt, l);
				
				if(output_mode == 0 && i % substeps == 0) {
					unsigned long idx = (unsigned long)id * U_SIZE * steps * num / (substeps * thread_num)
						+ (unsigned long)(k - initial_idx) * U_SIZE * steps / substeps
						+ (unsigned long)i * U_SIZE / substeps;
					
					memcpy(&out_chunk[idx], &p[k].u[0], U_SIZE * sizeof(double));
					#pragma omp master
					{
						if((k + 1) % CHUNK_SIZE == 0 && i == 0) {
							int current = thread_num * (k - initial_idx + 1);
							int total = thread_num * final_idx;
							printf("Particles processed: %i/%i.\n", current, total);
						}
					}
				}
			}
			
			if(output_mode == 1) {
				for(int j = U_SIZE; j < 2 * U_SIZE; j++) {
					out_chunk[id * 2 * U_SIZE * CHUNK_SIZE + chunk_current + j] = p[k].u[j - U_SIZE];
				}
				chunk_current += 2 * U_SIZE;
				if((k + 1) % CHUNK_SIZE == 0 && k - initial_idx != 0) {
					#pragma omp barrier
					#pragma omp master
					{
						int current = thread_num * (k - initial_idx + 1);
						int total = thread_num * final_idx;
						printf("Particles processed: %i/%i.\n", current, total);
						print_chunk(out, out_chunk, thread_num);
						memset(out_chunk, 0, 2 * U_SIZE * CHUNK_SIZE * thread_num * sizeof(double));
					}
					chunk_current = 0;
					#pragma omp barrier
				}
			}
		}
	}
	if(output_mode == 0)
		fwrite(out_chunk, sizeof(double), U_SIZE * steps * num / substeps, out);
}

int main(int argc, char **argv) {
	srand(128);
	double start_time = omp_get_wtime();
	if(argc != 4) {
		printf("This is a program which simulates laser-electron interactions.\n"); 
		printf("Usage: %s <filename_input> <filename_lasers> <filename_output>\n", argv[0]);
		printf("For more details visit: https://github.com/BanuDarius/electron-momentum-transfer.\n");
		return 1;
	}
	FILE *out = fopen(argv[3], "wb");
	if(!out) { perror("Cannot open output file."); return 1; }
	
	double vi[3];
	set_initial_vel(vi, 0.0, 0.0, 0.0);
	struct parameters *param = malloc(sizeof(struct parameters));
	set_parameters(param, argv[1]);
	
	struct laser *l = malloc(param->num_lasers * sizeof(struct laser));
	struct particle *p = aligned_alloc(64, param->num * sizeof(struct particle));
	double *out_chunk = create_out_chunk(param);
	void (*compute_function)(double *restrict, double *restrict, const struct laser *restrict);
	
	if(!l || !p || !out_chunk) { perror("Memory allocation error."); return 1; }
	
	set_lasers(l, param->num_lasers, argv[2]);
	set_particles(p, param, vi);
	set_mode(&compute_function, param->mode);
	
	printf("Simulation started.\n");
	simulate(param, compute_function, out, out_chunk, l, p);
	printf("Simulation ended.\n");
	
	printf("Time taken: %0.3fs.\n", omp_get_wtime() - start_time);
	free(out_chunk); free(param); free(p); free(l);
	fclose(out);
	return 0;
}

