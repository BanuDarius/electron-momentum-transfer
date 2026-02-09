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
	FILE *in = fopen(argv[1], "rb");
	//FILE *out = fopen("./output/out-stats.bin", "wb");
	//FILE *out_deriv = fopen("./output/out-deriv.bin", "ab");
	FILE *out_max_py= fopen(argv[5], "ab");
	
	int num = atoi(argv[2]), steps = atoi(argv[3]);
	double a0 = atof(argv[4]);
	double data[num];
	double t[2];
	
	for(int i = 0; i < num; i++) {
		int x = fread(t, sizeof(double), 2, in);
		data[i] = t[1];
	}
	
	double max_py = -INFINITY;
	for(int i = 0; i < num; i++) {
		double py = data[i];
		if(fabs(py) > max_py)
			max_py = fabs(py);
	}
	double v[2] = {a0, max_py};
	fwrite(v, sizeof(double), 2, out_max_py);
	
	/*int centerIndex = size / 2 + size / (8 * wave_count);
	fprintf(outDeriv, "%e ", a0);
	for(int i = 0; i < 2 * wave_count; i++) {
		int offset = 2;
		double left = final_data[size + centerIndex - offset];
		double right = final_data[size + centerIndex + offset];
		double slope = (right - left) / (2 * offset);
		fprintf(outDeriv, "%e ", slope);
		centerIndex += 2 * size / (8 * wave_count);
	}
	fprintf(outDeriv, "\n");*/
	
	fclose(out_max_py); fclose(in);
	printf("Ended calculating max(py).\n");
	return 0;
}