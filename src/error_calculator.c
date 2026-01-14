#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
	int steps = 4096;
	FILE *inA = fopen("./output/out-stats-1.bin", "rb"), *inB = fopen("./output/out-stats-2.bin", "rb");
	FILE *out = fopen("./output/out-error.bin", "wb"), *outAverageError = fopen("./output/out-average-error.bin", "ab");
	double sum = 0.0, a0 = atof(argv[1]);

	for(int i = 0; i < steps; i++) {
		double data[4];
		fread(&data[0], sizeof(double), 2, inA);
		fread(&data[2], sizeof(double), 2, inB);
		double error = fabs(data[3] - data[1]);
		fwrite(&data[0], sizeof(double), 1, out);
		fwrite(&error, sizeof(double), 1, out);
		sum += error;
	}

	double average = sum / ((double) steps);
	fwrite(&a0, sizeof(double), 1, outAverageError);
	fwrite(&average, sizeof(double), 1, outAverageError);

	printf("Ended error calculation.\n");
	fclose(outAverageError);
	fclose(inA); fclose(inB); fclose(out);
	return 0;
}