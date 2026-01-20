#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
	int num = atoi(argv[1]);
	FILE *in_a = fopen("./output/out-final-py-electromag.bin", "rb"), *in_b = fopen("./output/out-final-py-pond.bin", "rb");
	FILE *out = fopen("./output/out-error.bin", "wb"), *out_average_error = fopen("./output/out-average-error.bin", "ab");
	double sum = 0.0, a0 = atof(argv[2]);
	
	for(int i = 0; i < num; i++) {
		double data[4];
		fread(&data[0], sizeof(double), 2, in_a);
		fread(&data[2], sizeof(double), 2, in_b);
		double error = fabs(data[3] - data[1]);
		fwrite(&data[0], sizeof(double), 1, out);
		fwrite(&error, sizeof(double), 1, out);
		sum += error;
	}
	
	double average = sum / ((double) num);
	fwrite(&a0, sizeof(double), 1, out_average_error);
	fwrite(&average, sizeof(double), 1, out_average_error);
	
	printf("Ended error calculation.\n");
	fclose(out_average_error);
	fclose(in_a); fclose(in_b); fclose(out);
	return 0;
}