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

int main(int argc, char **argv) {
	if(argc != 7) {
		printf("This is a program which calculates the difference between 2 data sets.\n"); 
		printf("Usage: %s <num> <sweep_steps> <filename_input_1> <filename_input_2> <filename_output> <filename_output_average>\n", argv[0]);
		printf("For more details visit: https://github.com/BanuDarius/electron-momentum-transfer.\n");
		return 1;
	}
	int num = atoi(argv[1]), steps = atoi(argv[2]);
	FILE *in_a = fopen(argv[3], "rb"), *in_b = fopen(argv[4], "rb");
	FILE *out_error = fopen(argv[5], "ab"), *out_error_average = fopen(argv[6], "ab");
	if(!in_a || !in_b || !out_error || !out_error_average) {
		fprintf(stderr, "Cannot open error file.\n"); return 1;
	}
	
	double *buffer_a = malloc(3 * steps * num * sizeof(double));
	double *buffer_b = malloc(3 * steps * num * sizeof(double));
	double *error = malloc(3 * steps * num * sizeof(double));
	double *sum_errors = calloc(3 * steps,  sizeof(double));
	if(!buffer_a || !buffer_b || !error || !sum_errors) {
		fprintf(stderr, "Cannot create memory buffer.\n"); return 1;
	}
	int status = 0;
	status += fread(buffer_a, sizeof(double), 3 * steps * num, in_a);
	status += fread(buffer_b, sizeof(double), 3 * steps * num, in_b);
	fclose(in_a); fclose(in_b);
	
	#pragma omp parallel for reduction(+:sum_errors[0 : 3 * steps])
	for(int i = 0; i < steps; i++) {
		for(int j = 0; j < 3 * num; j++) {
			int idx = i * 3 * num + j;
			error[idx] = fabs(buffer_a[idx] - buffer_b[idx]);
			int idx_err = i * 3 + j % 3;
			sum_errors[idx_err] += error[idx];
		}
	}
	free(buffer_a); free(buffer_b);
	fwrite(error, sizeof(double), 3 * steps * num, out_error);
	fclose(out_error);
	free(error);
	
	#pragma omp parallel for
	for(int i = 0; i < 3 * steps; i++)
		sum_errors[i] /= num;
	
	fwrite(sum_errors, sizeof(double), 3 * steps, out_error_average);
	fclose(out_error_average);
	free(sum_errors);
	return 0;
}