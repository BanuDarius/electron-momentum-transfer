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
	FILE *out_max_p = fopen(argv[4], "ab");
	
	int num = atoi(argv[2]), steps = atoi(argv[3]);
	double data[num], t[2];
	
	for(int i = 0; i < num; i++) {
		int x = fread(t, sizeof(double), 2, in);
		data[i] = t[1];
	}
	
	double max_p = -INFINITY;
	for(int i = 0; i < num; i++) {
		double p = data[i];
		if(fabs(p) > max_p)
			max_p = fabs(p);
	}
	
	fwrite(&max_p, sizeof(double), 1, out_max_p);
	
	fclose(out_max_p); fclose(in);
	printf("Ended calculating max(p).\n");
	return 0;
}