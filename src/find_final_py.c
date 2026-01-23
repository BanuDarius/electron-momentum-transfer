#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
	FILE *in = fopen(argv[1], "rb");
	FILE *out_final_py = fopen(argv[4], "wb"), *out_final_py_all = fopen(argv[5], "ab");
	
	int num = atoi(argv[2]), steps = atoi(argv[3]);
	double t[8];
	
	for(int i = 0; i < num; i++) {
		for(int j = 0; j < steps; j++) {
			fread(t, sizeof(double), 8, in);
			if(j == 0) {
				double pos = t[2];
				fwrite(&pos, sizeof(double), 1, out_final_py);
				fwrite(&pos, sizeof(double), 1, out_final_py_all);
			}
			if(j == steps - 1) {
				double py = t[6];
				fwrite(&py, sizeof(double), 1, out_final_py);
				fwrite(&py, sizeof(double), 1, out_final_py_all);
			}
		}
	}
	
	fclose(out_final_py_all); fclose(out_final_py); fclose(in);
	printf("Ended calculating final py.\n");
	return 0;
}