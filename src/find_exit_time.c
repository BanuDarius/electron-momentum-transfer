#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char **argv) {
	FILE *in = fopen(argv[1], "rb");
	FILE *out = fopen("./output/out-exit-time.bin", "wb");
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
		double lastVelocity = velocityData[steps - 1];
		bool foundLast = false;
		for(int j = steps; j > 0; j--) {
			double currentVelocity = velocityData[j];
			//fwrite(&velocityData[j], sizeof(double), 1, out);
			if(fabs(currentVelocity - lastVelocity) > 1e-16) {
				fwrite(&initialPosition, sizeof(double), 1, out);
				fwrite(&timeData[j], sizeof(double), 1, out);
				foundLast = true;
				break;
			}
		}
		/*if(!foundLast) {
			fwrite(&initialPosition, sizeof(double), 1, out);
			fwrite(&timeData[steps-1], sizeof(double), 1, out);
		}*/
	}
	printf("Calculated particle exit times.\n");
	fclose(in); fclose(out);
	return 0;
}