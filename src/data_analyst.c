#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
	FILE *in = fopen(argv[1], "rb");
	FILE *out = fopen("./output/out-stats.bin", "wb");
	FILE *out_deriv = fopen("./output/out-deriv.bin", "ab");
	FILE *out_max_p= fopen("./output/out-max-py.bin", "ab");

	int size = 4096;
	int num = atoi(argv[2]), output_max_p = atoi(argv[5]);
	double wave_count = atoi(argv[3]);
	double a0 = atof(argv[4]);
	double wavelength = 2 * 3.141592 * 137.036 / 0.057;
	double *data = malloc(2 * num * sizeof(double));
	double *final_data = malloc(2 * size * sizeof(double));
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

	double full_space_size = wavelength * wave_count;
	for(int i = 0; i < size; i++) {
		int c = 0;
		double y = 0.0;
		double x0 = 2.0 * (double) i * full_space_size / size - full_space_size;
		double x1 = x0 + 2.0 * full_space_size / size;
		for(int j = 0; j < num; j++) {
			double current = data[j];
			if(current > x0 && current < x1) {
				c++;
				y += data[num + j];
			}
		}
		final_data[i] = x0;
		if(c != 0)
			final_data[size + i] = y / (double)c;
		else if(i != 0)
			final_data[size + i] = final_data[size + i - 1];
		else
			final_data[size + i] = 0.0;
	}

	if(output_max_p == 1) {
		double max_p = -INFINITY;
		for(int i = 0; i < num; i++) {
			double py = data[num + i];
			if(fabs(py) > max_p)
				max_p = fabs(py);
		}
		double v[2] = {a0, max_p};
		fwrite(v, sizeof(double), 2, out_max_p);
	}

	for(int i = 0; i < size; i++) {
		fwrite(&final_data[i], sizeof(double), 1, out);
		fwrite(&final_data[size + i], sizeof(double), 1, out);
	}

	/*int centerIndex = size / 2 + size / (8 * wave_count);
	fprintf(outDeriv, "%e ", a0);
	for(int i = 0; i < 2 * wave_count; i++) {
		int offset = 2;
		double left = final_data[size + centerIndex - offset];
		double right = final_data[size + centerIndex + offset];
		double slope = (right - left) / (2 * offset);
		fprintf(outDeriv, "%e ", slope);
		centerIndex += 2 * size / (8 * wave_count);
	}
	fprintf(outDeriv, "\n");*/

	free(final_data); free(data);
	fclose(out_deriv); fclose(out); fclose(in);
	printf("Ended data analysis.\n");
	return 0;
}