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

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

void set_zero(double *v) {
	for(int i = 0; i < 3; i++)
		v[i] = 0.0;
}

int main(int argc, char **argv) {
	FILE *in = fopen(argv[1], "rb");
	FILE *out = fopen(argv[6], "wb");
	int num = atoi(argv[2]), steps = atoi(argv[3]), axis_pos = atoi(argv[4]), axis_p = atoi(argv[5]);
	
	double velocity_data[steps], time_data[steps], initial_position;
	
	for(int i = 0; i < num; i++) {
		for(int j = 0; j < steps; j++) {
			double t[8];
			int x = fread(t, sizeof(double), 8, in);
			if(j == 0)
				initial_position = t[axis_pos + 1];
			time_data[j] = t[0];
			velocity_data[j] = t[axis_p + 5];
		}
		
		double v[4];
		v[0] = initial_position;
		double firstVelocity = velocity_data[0];
		double lastVelocity = velocity_data[steps - 1];
		
		for(int j = 1; j < steps; j++) {
			double current_velocity = velocity_data[j];
			if(fabs(current_velocity - firstVelocity) > 1e-2) {
				v[1] = time_data[j];
				break;
			}
		}
		
		for(int j = steps - 2; j > 0; j--) {
			double current_velocity = velocity_data[j];
			if(fabs(current_velocity - lastVelocity) > 1e-2) {
				double last_step = (double) j;
				v[2] = time_data[j];
				v[3] = last_step;
				break;
			}
		}
		
		for(int j = 1; j < 4; j++) {
			if(fabs(v[j]) < 1e-5)
				set_zero(&v[1]);
		}
		fwrite(v, sizeof(double), 4, out);
	}
	
	printf("Ended calculating enter exit times.\n");
	fclose(in); fclose(out);
	return 0;
}