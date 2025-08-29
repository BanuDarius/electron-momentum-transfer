double m = 1;
double q = -1;
double c = 137.036;
double e = 2.7182818284;
double pi = 3.1415926535;

#define U_SIZE 8
#define CORE_NUM 8
#define CHUNK_SIZE 100
#define DEG_TO_RAD (pi / 180.0)

pthread_barrier_t barrierSync, barrierCompute;

struct Particle {
	double u[8];
};

struct Laser {
	double E0, omega, xif, zetax, zetay, psi;
	double epsilon1[3], epsilon2[3], n[3];
};
struct Laser *l;

struct SharedData {
	FILE *out;
	double dtau;
	double *ochunk;
	struct Laser *l;
	struct Particle *e;
	int initIndex, finalIndex, steps, id;
	void (*fc)(double*, double*, double);
};

double RandVal(double min, double max) {
	double s = rand() / (double)RAND_MAX;
	return min + s * (max - min);
}

void PrintChunk(FILE *out, double *chunk) {
	for(int i = 0; i < CORE_NUM * CHUNK_SIZE; i++) {
		for(int j = 0; j < 2 * U_SIZE; j++) {
			fprintf(out, "%e ", chunk[2 * U_SIZE * i + j]);
			//fwrite(&chunk[2 * U_SIZE * i + j], sizeof(double), 1, out);
		}
		fprintf(out, "\n");
	}
}

void CopyInitial(double *ch, double *u, int k, int id) {
    int index = id * 2 * U_SIZE * CHUNK_SIZE + 2 * U_SIZE * k;
    for(int i = index; i < index + U_SIZE; i++) {
		ch[i] = u[i - index];
    }
}

void SetChunk(double *ochunk, double *chunk, int init, int fin) {
	for(int i = init; i < fin; i++) {
		ochunk[i] = chunk[i-init];
	}
}

void SetVec(double *u1, double *u2, int n) {
	for (int i = 0; i < n; i++)
		u1[i] = u2[i];
}

double *NewVec(int n) {
	double *u = (double *)malloc(n * sizeof(double));
	return u;
}

void SetZero(double *u) {
	for(int i = 0; i < 3; i++)
		u[i] = 0;
}

void SetZeroN(double *u, int n) {
	for(int i = 0; i < n; i++)
		u[i] = 0;
}

void MultVec(double *u, double a) {
	for(int i = 0; i < 3; i++)
		u[i] *= a;
}

void MultVec4(double *u, double a) {
	for(int i = 0; i < 4; i++)
		u[i] *= a;
}

void AddVec(double *u, double *v) {
	for(int i = 0; i < 3; i++)
		u[i] += v[i];
}
void AddVec4(double *u, double *v) {
	for(int i = 0; i < 4; i++)
		u[i] += v[i];
}

void SubVec(double *x, double *u, double *v) {
	for(int i = 0; i < 3; i++)
		x[i] = u[i] - v[i];
}

void Cross(double *a, double *b, double *u) {
	u[0] = a[1] * b[2] - a[2] * b[1];
	u[1] = a[2] * b[0] - a[0] * b[2];
	u[2] = a[0] * b[1] - a[1] * b[0];
}

double Dot(double *a, double *b) {
	double x = a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
	return x;
}

double Dot4Rel(double *u, double *v) {
	double x = u[0] * v[0] - u[1] * v[1] - u[2] * v[2] - u[3] * v[3];
	return x;
}

double Magnitude(double *a) {
	double x = sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);
	return x;
}

double Gamma(double *v) {
	double gamma = 1 / sqrt(1 - pow(Magnitude(v), 2) / (c * c));
	return gamma;
}

double Env(double xi, double xif) {
	double sigma = 6 * pi;
	if(xi > -xif && xi < xif)
		return 1.0;
	else if(xi >= xif)
		return exp(-(xi - xif) * (xi - xif) / (sigma * sigma));
	else if(xi <= -xif)
		return exp(-(xi + xif) * (xi + xif) / (sigma * sigma));
}

double EnvPrime(double xi, double xif) {
	double sigma = 6 * pi;
	if(xi > -xif && xi < xif)
		return 0.0;
	else if(xi >= xif)
		return (-2.0) * (xi - xif) / (sigma * sigma) * exp(-(xi - xif) * (xi - xif) / (sigma * sigma));
	else if(xi <= -xif)
		return (-2.0) * (xi + xif) / (sigma * sigma) * exp(-(xi + xif) * (xi + xif) / (sigma * sigma));
}

void CalcE(double *E, double *u, struct Laser *l, int i) {
	double k = l[i].omega / c;
	double t = u[0] / c;
	double xif = l[i].xif;
	double alpha = l[i].omega * t - k * Dot(l[i].n, &u[1]);
	double Ec = Env(alpha + l[i].psi, xif) * l[i].E0;
	for(int j = 0; j < 3; j++)
		E[j] = l[i].epsilon1[j] * l[i].zetax * cos(alpha) + l[i].epsilon2[j] * l[i].zetay * sin(alpha);
	MultVec(E, Ec);
}

void CalcB(double *B, double *E, double *u, struct Laser *l, int i) {
	Cross(l[i].n, E, B);
	MultVec(B, 1/c);
}

void ComputeEB(double *E, double *B, double *u) {
	double Et[3], Bt[3];
	for(int i = 0; i < 2; i++) {
		SetZero(Et);
		SetZero(Bt);
		CalcE(Et, u, l, i);
		CalcB(Bt, Et, u, l, i);
		AddVec(E, Et);
		AddVec(B, Bt);
	}
}

void f(double *u, double *up, const double t) {
	double E[3], B[3];
	SetZero(E); SetZero(B);
	ComputeEB(E, B, u);

	up[0] = u[4];
	up[1] = u[5];
	up[2] = u[6];
	up[3] = u[7];
	up[4] = E[0] * u[5] + E[1] * u[6] + E[2] * u[7];
	up[5] = E[0] * u[4] + B[2] * c * u[6] - B[1] * c * u[7];
	up[6] = E[1] * u[4] - B[2] * c * u[5] + B[0] * c * u[7];
	up[7] = E[2] * u[4] + B[1] * c * u[5] - B[0] * c * u[6];
	MultVec4(&up[4], q / (m * c));
}

#include "PondG.h"

void fP2G(double *u, double *up, const double t) {
	double a = ComputeA(u, l);
	double mass = m * sqrt(1 + a);
	double dmdx[4];
	for(int i = 0; i < 4; i++)
		dmdx[i] = 0.5 * DerivativeA(u, l, i) * m / sqrt(1 + a);
	up[0] = u[4];
	up[1] = u[5];
	up[2] = u[6];
	up[3] = u[7];
	up[4] = - u[4] * u[4] * dmdx[0] / c + c * dmdx[0] - u[4] * u[5] * dmdx[1] - u[4] * u[6] * dmdx[2] - u[4] * u[7] * dmdx[3];
	up[5] = - u[5] * u[4] * dmdx[0] / c - (c * c) * dmdx[1] - u[5] * u[5] * dmdx[1] - u[5] * u[6] * dmdx[2] - u[5] * u[7] * dmdx[3];
	up[6] = - u[6] * u[4] * dmdx[0] / c - u[6] * u[5] * dmdx[1] - (c * c) * dmdx[2] - u[6] * u[6] * dmdx[2] - u[6] * u[7] * dmdx[3];
	up[7] = - u[7] * u[4] * dmdx[0] / c - u[7] * u[5] * dmdx[1] - u[7] * u[6] * dmdx[2] - (c * c) * dmdx[3] - u[7] * u[7] * dmdx[3];
	MultVec4(&up[4], 1.0 / mass);
}

void SetPosition(struct Particle *p, double r, double h, double z) {
	double x[3];
	x[0] = RandVal(-r, r);
	x[1] = RandVal(-r, r);
	double dist = sqrt(x[0] * x[0] + x[1] * x[1]);
	if (dist <= r) {
		p->u[1] = x[0];
		p->u[2] = x[1];
		p->u[3] = RandVal(h - z, h + z);
	} else
		SetPosition(p, r, h, z);
}

void Rotate(double *u, double phi, double theta) {
	double x, y, z;
	y = u[1];
	z = u[2];
	u[1] = y * cos(phi) - z * sin(phi);
	u[2] = y * sin(phi) + z * cos(phi);
	x = u[0];
	y = u[1];
	u[0] = x * cos(theta) - y * sin(theta);
	u[1] = x * sin(theta) + y * cos(theta);
}

double *DirectionVec(double phiL, double thetaL) {
	double *u = NewVec(3);
	u[0] = 0;
	u[1] = 0;
	u[2] = 1;
	Rotate(u, phiL, thetaL);
	return u;
}

void Epsilon(double *u, double *w) {
	double *v = NewVec(3);
	v[0] = 1;
	v[1] = 0;
	v[2] = 0;
	Cross(u, v, w);
	double mag = Magnitude(w);
	double scale = Magnitude(u);
	for (int i = 0; i < 3; i++)
		w[i] = scale * w[i] / mag;
	free(v);
}

int InitialIndex(int n, unsigned int threadNum) {
	int index = n * threadNum / CORE_NUM;
	return index;
}

int FinalIndex(int n, unsigned int threadNum) {
	int index = n * (threadNum + 1) / CORE_NUM;
	return index;
}

void SetInitialVel(double *vi, double m, double phi, double theta) {
	SetVec(vi, DirectionVec(phi, theta), 3);
	MultVec(vi, m);
}

void SetLaser(struct Laser *l, double E0, double phi, double theta, double xif, double psi) {
	l->E0 = E0;
	l->zetax = 0;
	l->zetay = 1;
	l->psi = psi;
	l->xif = xif;
	l->omega = 0.057;
	double *nv = DirectionVec(phi, theta);
	double epsilon1[3];
	double epsilon2[3];
	Epsilon(nv, epsilon1);
	Cross(nv, epsilon1, epsilon2);
	SetVec(l->n, nv, 3);
	SetVec(l->epsilon1, epsilon1, 3);
	SetVec(l->epsilon2, epsilon2, 3);
	free(nv);
}

void SetParticles(struct Particle *p, int num, double r, double h, double z, double phi, double theta, double *vi) {
	for(int i = 0; i < num; i++) {
		p[i].u[0] = 0;
		SetPosition(&p[i], r, h, z);
		Rotate(&p[i].u[1], phi, theta);
		double gamma = Gamma(vi);
		p[i].u[4] = m * c * gamma;
		p[i].u[5] = m * vi[0] * gamma;
		p[i].u[6] = m * vi[1] * gamma;
		p[i].u[7] = m * vi[2] * gamma;
	}
}

void SetSharedData(struct SharedData *sdata, struct Particle *e, struct Laser *l, FILE *out, double *ochunk,
int num, int steps, double dtau, void (*fc)(double*, double*, double)) {
	for(int i = 0; i < CORE_NUM; i++) {
		sdata[i].l = l;
		sdata[i].e = e;
		sdata[i].id = i;
		sdata[i].fc = fc;
		sdata[i].out = out;
		sdata[i].dtau = dtau;
		sdata[i].steps = steps;
		sdata[i].ochunk = ochunk;
		sdata[i].finalIndex = FinalIndex(num, i);
		sdata[i].initIndex = InitialIndex(num, i);
	}
}

char *SetFilename(char *s) {
	char *name = (char *)malloc(30 * sizeof(char));
	sprintf(name, "out-%s.txt", s);
	return name;
}

void CheckErrors(void *out, void *sdata) {
	if(sdata == NULL) {
		perror("Shared data cannot be created");
		abort();
	}
	if(out == NULL) {
		perror("Cannot open file");
		abort();
	}
}