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
	int num = atoi(argv[1]);
	FILE *in_a = fopen("./output/out-final-py-electromag.bin", "rb"), *in_b = fopen("./output/out-final-py-pond.bin", "rb");
	FILE *out = fopen("./output/out-error.bin", "wb"), *out_average_error = fopen("./output/out-average-error.bin", "ab");
	FILE *out_error_all = fopen("./output/out-error-all.bin", "ab");
	double sum = 0.0, a0 = atof(argv[2]);
	
	for(int i = 0; i < num; i++) {
		double data[4];
		int x = fread(&data[0], sizeof(double), 2, in_a);
		int y = fread(&data[2], sizeof(double), 2, in_b);
		double error = fabs(data[3] - data[1]);
		fwrite(&data[0], sizeof(double), 1, out);
		fwrite(&data[0], sizeof(double), 1, out_error_all);
		fwrite(&error, sizeof(double), 1, out);
		fwrite(&error, sizeof(double), 1, out_error_all);
		sum += error;
	}
	
	double average = sum / ((double) num);
	fwrite(&a0, sizeof(double), 1, out_average_error);
	fwrite(&average, sizeof(double), 1, out_average_error);
	
	printf("Ended error calculation.\n");
	fclose(out_average_error);
	fclose(in_a); fclose(in_b); fclose(out); fclose(out_error_all);
	return 0;
}