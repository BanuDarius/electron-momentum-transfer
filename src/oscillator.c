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

#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

const double c = 137.036;
const double omega = 0.057;
const double k = omega / c;
const double pi = 3.1415926535;
const double wavelength = 2.0 * pi * c / omega;

int main(int argc, char **argv) {
	clock_t ti = clock();
	FILE *out = fopen("./output/out-oscillator.bin", "wb");
	int steps = 4096, num = atoi(argv[2]);
	double a0 = atof(argv[1]);
	double A0 = a0 * c;
	double alpha = 2.0 * k * A0 * A0 * (1.0 + sin(pi * omega) / (pi * omega));
	double v, y, beta;
	double tf = 1500.0;
	double t, vh, dt = tf / steps;

	for(int j = 0; j < num; j++) {
		v = 0.0;
		y = 2.0 * j / num * wavelength - wavelength;
		beta = alpha * sin(2.0 * k * y);

		for(int i = 0; i < steps; i++) {
			vh = v + 0.5 * beta * dt;
			y += vh * dt;
			beta = alpha * sin(2.0 * k * y);
			v = vh + 0.5 * beta * dt;
			t = i * dt;
			double f[3] = {t, y, v};
			fwrite(f, sizeof(double), 3, out);
		}
	}

	printf("Completed oscillator simulation.\n");
	printf("Time taken: %0.3fs.\n", (double)(clock() - ti) / (CLOCKS_PER_SEC));
	fclose(out);
	return 0;
}