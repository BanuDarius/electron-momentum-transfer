#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
	FILE *in = fopen(argv[1], "rb");
	FILE *out = fopen("out-file.txt", "w");
	FILE *outDeriv = fopen("out-deriv.txt", "a");

	int steps = 4096;
	int num = atoi(argv[2]);
	double waveCount = atoi(argv[3]);
	double a0 = atof(argv[4]);
	double wavelength = 2 * 3.141592 * 137.036 / 0.057;
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
	double fullSpaceSize = wavelength * waveCount;
	for(int i = 0; i < steps; i++) {
		int c = 0;
		double y = 0.0;
		double x0 = 2.0 * (double) i * fullSpaceSize / steps - fullSpaceSize;
		double x1 = x0 + 2.0 * fullSpaceSize / steps;
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
	int centerIndex = steps / 2 + steps / (8 * waveCount);
	fprintf(outDeriv, "%e ", a0);
	for(int i = 0; i < 2 * waveCount; i++) {
		int offset = 2;
		double left = finalData[steps + centerIndex - offset];
		double right = finalData[steps + centerIndex + offset];
		double slope = (right - left) / (2 * offset);
		fprintf(outDeriv, "%e ", slope);
		centerIndex += 2 * steps / (8 * waveCount);
	}
	fprintf(outDeriv, "\n");
	for(int i = 0; i < steps; i++)
		fprintf(out, "%e %e\n", finalData[i], finalData[steps + i]);

	free(finalData); free(data);
	fclose(outDeriv); fclose(out); fclose(in);
	printf("Ended data analysis.\n");
	return 0;
}