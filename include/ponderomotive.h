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

#ifndef PONDEROMOTIVE_H
#define PONDEROMOTIVE_H

void potential_deriv_a(double *a, double *u, const struct laser *restrict l, int index, int n);
void potential_a(double *a, double *u, const struct laser *restrict l, int n);
double integrate(double *u, const struct laser *restrict l);
double integrate_dmuda(double *u, const struct laser *restrict l, int index);
double compute_a(double *u, const struct laser *restrict l);
double derivative_a(double *u, const struct laser *restrict l, int index);
void ponderomotive(double *restrict u, double *restrict up, const struct laser *restrict l);

#endif