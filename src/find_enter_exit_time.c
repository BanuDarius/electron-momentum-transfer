#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char **argv) {
	FILE *in = fopen(argv[1], "rb");
	FILE *out = fopen(argv[4], "wb");
	int num = atoi(argv[2]), steps = atoi(argv[3]);
	
	double velocity_data[steps], time_data[steps], initial_position;
	
	for(int i = 0; i < num; i++) {
		for(int j = 0; j < steps; j++) {
			double t[8];
			int x = fread(t, sizeof(double), 8, in);
			if(j == 0)
				initial_position= t[2];
			time_data[j] = t[0];
			velocity_data[j] = t[7];
		}
	
		fwrite(&initial_position, sizeof(double), 1, out);
		double firstVelocity = velocity_data[0];
		for(int j = 0; j < steps; j++) {
			double current_velocity = velocity_data[j];
			if(fabs(current_velocity - firstVelocity) > 1e-14) {
				fwrite(&time_data[j], sizeof(double), 1, out);
				break;
			}
		}
	
		double lastVelocity = velocity_data[steps - 1];
		for(int j = steps - 1; j > 0; j--) {
			double current_velocity = velocity_data[j];
			if(fabs(current_velocity - lastVelocity) > 1e-14) {
				fwrite(&time_data[j], sizeof(double), 1, out);
				double lastStep = (double) j;
				fwrite(&lastStep, sizeof(double), 1, out);
				break;
			}
		}
	}
	
	printf("Calculated particle exit times.\n");
	fclose(in); fclose(out);
	return 0;
}