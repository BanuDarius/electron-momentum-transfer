#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
	int steps = 8192;
	FILE *inA = fopen("out-stats-1.bin", "rb"), *inB = fopen("out-stats-2.bin", "rb");
	FILE *out = fopen("out-error.bin", "wb");
	
	for(int i = 0; i < steps; i++) {
		double data[4];
		fread(&data[0], sizeof(double), 2, inA);
		fread(&data[2], sizeof(double), 2, inB);
		double error = fabs(data[3] - data[1]);
		fwrite(&data[0], sizeof(double), 1, out);
		fwrite(&error, sizeof(double), 1, out);
	}
	printf("Ended error calculation.\n");
	fclose(inA); fclose(inB); fclose(out);
	return 0;
}