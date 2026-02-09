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
	FILE *out_final_py = fopen(argv[4], "wb"), *out_final_py_all = fopen(argv[5], "ab");
	
	int num = atoi(argv[2]), steps = atoi(argv[3]);
	double t[8];
	
	for(int i = 0; i < num; i++) {
		for(int j = 0; j < steps; j++) {
			int x = fread(t, sizeof(double), 8, in);
			if(j == 0) {
				double pos = t[2];
				fwrite(&pos, sizeof(double), 1, out_final_py);
				fwrite(&pos, sizeof(double), 1, out_final_py_all);
			}
			if(j == steps - 1) {
				double py = t[6];
				fwrite(&py, sizeof(double), 1, out_final_py);
				fwrite(&py, sizeof(double), 1, out_final_py_all);
			}
		}
	}
	
	fclose(out_final_py_all); fclose(out_final_py); fclose(in);
	printf("Ended calculating final py.\n");
	return 0;
}