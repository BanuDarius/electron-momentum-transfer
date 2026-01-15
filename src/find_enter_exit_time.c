#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char **argv) {
	FILE *in = fopen(argv[1], "rb");
	FILE *out = fopen("./output/out-enter-exit-time.bin", "wb");
	int num = atoi(argv[2]), steps = atoi(argv[3]);

	double velocityData[steps], timeData[steps], initialPosition;

	for(int i = 0; i < num; i++) {
		for(int j = 0; j < steps; j++) {
			double t[8];
			fread(t, sizeof(double), 8, in);
			if(j == 0)
				initialPosition= t[2];
			timeData[j] = t[0];
			velocityData[j] = t[7];
		}

		fwrite(&initialPosition, sizeof(double), 1, out);
		double firstVelocity = velocityData[0];
		for(int j = 0; j < steps; j++) {
			double currentVelocity = velocityData[j];
			if(fabs(currentVelocity - firstVelocity) > 1e-16) {
				fwrite(&timeData[j], sizeof(double), 1, out);
				break;
			}
		}

		double lastVelocity = velocityData[steps - 1];
		for(int j = steps - 1; j > 0; j--) {
			double currentVelocity = velocityData[j];
			if(fabs(currentVelocity - lastVelocity) > 1e-16) {
				fwrite(&timeData[j], sizeof(double), 1, out);
				break;
			}
		}
	}

	printf("Calculated particle exit times.\n");
	fclose(in); fclose(out);
	return 0;
}