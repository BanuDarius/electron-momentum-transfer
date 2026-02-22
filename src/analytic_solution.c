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

#include <stdio.h>
#include <stdlib.h>

#include "init.h"
#include "tools.h"

int main(int argc, char **argv) {
	if(argc != 4) {
		printf("This is a program which simulates the trajectories of an electron interacting with a single laser, using an analytic solution.\n"); 
		printf("Usage: %s <filename_input> <filename_lasers> <filename_output>\n", argv[0]);
		printf("For more details visit: https://github.com/BanuDarius/electron-momentum-transfer.\n");
		return 1;
	}
	FILE *out = fopen(argv[3], "wb");
	if(!out) { perror("Cannot open output file."); return 1; }
	
	struct parameters *param = malloc(sizeof(struct parameters));
	set_parameters(param, argv[1]);
	
	struct laser *l = malloc(param->num_lasers * sizeof(struct laser));
	
	if(!l) { perror("Memory allocation error."); return 1; }
	
	set_lasers(l, param, argv[2]);
	
	printf("%lf BOOM!\n", l[0].sigma);
	return 0;
}