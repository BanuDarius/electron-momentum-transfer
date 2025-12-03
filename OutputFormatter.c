#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
	FILE *out = fopen("out-file.txt", "w");
	FILE *in = fopen(argv[1], "r");
	int steps = 2048;
	int num = atoi(argv[2]);
	double wavelength = atof(argv[3]);
	double *data = malloc(2 * num * sizeof(double));
	double *finalData = malloc(2 * steps * sizeof(double));
	double t;

	for(int i = 0; i < num; i++) {
		for(int j = 0; j < 16; j++) {
			fread(&t, sizeof(double), 1, in);
			if(j == 2)
				data[i] = t;
			else if(j == 14)
				data[num + i] = t;
		}
	}

	for(int i = 0; i < steps; i++) {
		int c = 0;
		double y = 0.0;
		double x0 = 2.0 * (double) i * wavelength / steps - wavelength;
		double x1 = x0 + 2.0 * wavelength / steps;
		for(int j = 0; j < num; j++) {
			double current = data[j];
			if(current >= x0 && current < x1) {
				c++;
				y += data[num + j];
			}
		}
		finalData[i] = x0;
		if(c != 0)
			finalData[steps + i] = y / c;
		else if(i != 0)
			finalData[steps + i] = finalData[steps + i - 1];
		else
			finalData[steps + i] = 0.0;
	}

	for(int i = 0; i < steps; i++)
		fprintf(out, "%e %e\n", finalData[i], finalData[steps + i]);

	free(finalData); free(data);
	fclose(out); fclose(in);
	printf("Ended data analysis.\n");
	return 0;
}