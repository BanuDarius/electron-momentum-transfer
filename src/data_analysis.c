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
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "data_analysis.h"

void post_process_data(double *out_chunk, Parameters *param, char *filename_max_p, char *filename_final_p, char *filename_initial_pos, char *filename_final_pos) {
	int num = param->num;
	int total_steps = param->steps / param->substeps;
	
	FILE *out_max_p = fopen(filename_max_p, "ab");
	FILE *out_final_p = fopen(filename_final_p, "ab");
	if(!out_max_p || !out_final_p) {
		fprintf(stderr, "Cannot open data analysis files!\n"); exit(1);
	}
	if(param->is_first_run) {
		FILE *out_initial_pos = fopen(filename_initial_pos, "wb");
		if(!out_initial_pos) {
			fprintf(stderr, "Cannot open initial particle positions file!\n"); exit(1);
		}
	
		double *initial_pos = malloc(3 * num * sizeof(double));
		if(!initial_pos) {
			fprintf(stderr, "Cannot allocate memory!\n"); exit(1);
		}
		
		for(int i = 0; i < num; i++)
			memcpy(&initial_pos[3 * i], &out_chunk[i * total_steps * U_SIZE + 1], 3 * sizeof(double));
		
		fwrite(initial_pos, sizeof(double), 3 * num, out_initial_pos);
		fclose(out_initial_pos);
		free(initial_pos);
	}
	if(param->output_final_pos) {
		FILE *out_final_pos = fopen(filename_final_pos, "ab");
		if(!out_final_pos) {
			fprintf(stderr, "Cannot open final particle positions file!\n"); exit(1);
		}
	
		double *final_pos = malloc(3 * num * sizeof(double));
		if(!final_pos) {
			fprintf(stderr, "Cannot allocate memory!\n"); exit(1);
		}
		
		for(int i = 0; i < num; i++)
			memcpy(&final_pos[3 * i], &out_chunk[(i + 1) * total_steps * U_SIZE - 7], 3 * sizeof(double));
		
		fwrite(final_pos, sizeof(double), 3 * num, out_final_pos);
		fclose(out_final_pos);
		free(final_pos);
	}
	
	double *final_p = malloc(3 * num * sizeof(double));
	if(!final_p) {
		fprintf(stderr, "Cannot allocate memory!\n"); exit(1);
	}
	
	int offset = (total_steps - 1) * U_SIZE;
	for(int i = 0; i < num; i++)
		memcpy(&final_p[3 * i], &out_chunk[i * total_steps * U_SIZE + offset + 5], 3 * sizeof(double));
	
	fwrite(final_p, sizeof(double), 3 * num, out_final_p);
	fclose(out_final_p);
	
	double max_p[3] = { 0.0, 0.0, 0.0 };
	for(int i = 0; i < num; i++) {
		for(int j = 0; j < 3; j++) {
			if(fabs(final_p[3 * i + j]) > max_p[j])
				max_p[j] = fabs(final_p[3 * i + j]);
		}
	}
	fwrite(max_p, sizeof(double), 3, out_max_p);
	fclose(out_max_p);
	free(final_p);
}