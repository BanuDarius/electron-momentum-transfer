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
	int num = atoi(argv[1]), index = atoi(argv[2]);
	FILE *in_a = fopen(argv[3], "rb"), *in_b = fopen(argv[4], "rb");
	FILE *out = fopen(argv[5], "wb"), *out_average = fopen(argv[6], "ab");
	double sum = 0.0;
	
	for(int i = 0; i < num; i++) {
		double data[4];
		int x = fread(&data[0], sizeof(double), 2, in_a);
		int y = fread(&data[2], sizeof(double), 2, in_b);
		double error = fabs(data[3] - data[1]);
		fwrite(&error, sizeof(double), 1, out);
		sum += error;
	}
	
	double average = sum / ((double) num);
	fwrite(&average, sizeof(double), 1, out_average);
	
	printf("Ended convergence calculation.\n");
	fclose(in_a); fclose(in_b); fclose(out);
	fclose(out_average);
	return 0;
}