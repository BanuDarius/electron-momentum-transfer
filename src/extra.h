double m = 1;
double q = -1;
double c = 137.036;
double e = 2.7182818284;
double pi = 3.1415926535;

#define U_SIZE 8
#define CORE_NUM 4
#define NUM_LASERS 2
#define CHUNK_SIZE 100
#define PONDEROMOTIVE_STEPS 4
#define DEG_TO_RAD (pi / 180.0)

pthread_barrier_t barrier_sync, barrier_compute;

double rand_val(double min, double max) {
	double s = rand() / (double)RAND_MAX;
	return min + s * (max - min);
}

void print_chunk(FILE *out, double *chunk) {
	fwrite(chunk, sizeof(double), 2 * U_SIZE * CHUNK_SIZE * CORE_NUM, out);
}

void copy_initial(double *ch, double *u, int k, int id) {
	int index = id * 2 * U_SIZE * CHUNK_SIZE + 2 * U_SIZE * k;
	for(int i = index; i < index + U_SIZE; i++) {
		ch[i] = u[i - index];
	}
}

void set_chunk(double *out_chunk, double *chunk, int init, int fin) {
	for(int i = init; i < fin; i++) {
		out_chunk[i] = chunk[i-init];
	}
}

void set_vec(double *u1, double *u2, int n) {
	for (int i = 0; i < n; i++)
		u1[i] = u2[i];
}

double *new_vec(int n) {
	double *u = (double *)malloc(n * sizeof(double));
	return u;
}

void set_zero(double *u) {
	for(int i = 0; i < 3; i++)
		u[i] = 0;
}

void set_zero_n(double *u, int n) {
	for(int i = 0; i < n; i++)
		u[i] = 0;
}

void mult_vec(double *u, double a) {
	for(int i = 0; i < 3; i++)
		u[i] *= a;
}

void mult_vec4(double *u, double a) {
	for(int i = 0; i < 4; i++)
		u[i] *= a;
}

void add_vec(double *u, double *v) {
	for(int i = 0; i < 3; i++)
		u[i] += v[i];
}

void add_vec4(double *u, double *v) {
	for(int i = 0; i < 4; i++)
		u[i] += v[i];
}

void sub_vec(double *x, double *u, double *v) {
	for(int i = 0; i < 3; i++)
		x[i] = u[i] - v[i];
}

void cross(double *a, double *b, double *u) {
	u[0] = a[1] * b[2] - a[2] * b[1];
	u[1] = a[2] * b[0] - a[0] * b[2];
	u[2] = a[0] * b[1] - a[1] * b[0];
}

double dot(double *a, double *b) {
	double x = a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
	return x;
}

double dot4(double *u, double *v) {
	double x = u[0] * v[0] - u[1] * v[1] - u[2] * v[2] - u[3] * v[3];
	return x;
}

double magnitude(double *a) {
	double x = sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);
	return x;
}

double compute_gamma(double *v) {
	double gamma = 1 / sqrt(1 - pow(magnitude(v), 2) / (c * c));
	return gamma;
}

double env(double xi, double xif) {
	double sigma = 2.0 * pi;
	if(xi > -xif && xi < xif)
		return 1.0;
	else if(xi >= xif)
		return exp(-(xi - xif) * (xi - xif) / (sigma * sigma));
	else
		return exp(-(xi + xif) * (xi + xif) / (sigma * sigma));
}

double env_prime(double xi, double xif) {
	double sigma = 2.0 * pi;
	if(xi > -xif && xi < xif)
		return 0.0;
	else if(xi >= xif)
		return - 2.0 * (xi - xif) / (sigma * sigma) * exp(-(xi - xif) * (xi - xif) / (sigma * sigma));
	else
		return - 2.0 * (xi + xif) / (sigma * sigma) * exp(-(xi + xif) * (xi + xif) / (sigma * sigma));
}

int initial_index(int n, unsigned int thread_num) {
	int index = n * thread_num / CORE_NUM;
	return index;
}

int final_index(int n, unsigned int thread_num) {
	int index = n * (thread_num + 1) / CORE_NUM;
	return index;
}