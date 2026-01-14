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
	FILE *out = fopen("out.bin", "wb");
	int steps = 8192, n = atoi(argv[2]);
	double a0 = atof(argv[1]);
	double A0 = a0 * c;
	double alpha = 2.0 * k * A0 * A0 * (1.0 + sin(pi * omega) / (pi * omega));
	double v, y, beta;
	double tf = 4000.0;
	double t, vh, dt = tf / steps;
	
	for(int j = 0; j < n; j++) {
		v = 0.0;
		y = 2.0 * j / n * wavelength - wavelength;
		beta = alpha * sin(2.0 * k * y);

		for(int i = 0; i < steps; i++) {
			vh = v + 0.5 * beta * dt;
			y += vh * dt;
			beta = alpha * sin(2.0 * k * y);
			v = vh + 0.5 * beta * dt;
			t = i * dt;
			if(i % 2 == 0) {
				double f[3] = {t, y, v};
				fwrite(f, sizeof(double), 3, out);
			}
		}
	}
	printf("Completed simulation.\n");
	printf("Time taken: %0.3f\n", (double)(clock() - ti) / (CLOCKS_PER_SEC));
	fclose(out);
	return 0;
}