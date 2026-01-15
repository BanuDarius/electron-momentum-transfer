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
	int initIndex, finalIndex, steps, outputMode, num, id;
	void (*fc)(double*, double*, double);
};

void CalcE(double *E, double *u, struct Laser *l, int i) {
	double k = l[i].omega / c;
	double t = u[0] / c;
	double xif = l[i].xif;
	double alpha = l[i].omega * t - k * Dot(l[i].n, &u[1]);
	double Ec1 = Env(alpha + l[i].psi, xif);
	double Ec2 = EnvPrime(alpha + l[i].psi, xif);
	double E1[3], E2[3];
	for(int j = 0; j < 3; j++)
		E1[j] = l[i].epsilon1[j] * l[i].zetax * cos(alpha) + l[i].epsilon2[j] * l[i].zetay * sin(alpha);
	for(int j = 0; j < 3; j++)
		E2[j] = l[i].epsilon1[j] * l[i].zetax * sin(alpha) + l[i].epsilon2[j] * l[i].zetay * (-cos(alpha));
	MultVec(E1, Ec1);
	MultVec(E2, Ec2);
	SetVec(E, E1, 3);
	AddVec(E, E2);
	MultVec(E, l[i].E0);
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

void electromag(double *u, double *up, const double t) {
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

void SetPosition(struct Particle *p, double r, double h, double z, int i, int num, int outputMode) {
	double wavelength = 2.0 * pi * c / 0.057;
	if(outputMode == 0) {
		p->u[1] = - r + 2.0 * i * r / num + 50.0;
		p->u[2] = 0.0;
	}
	else {
		p->u[1] = RandVal(h - r, h + r);
		p->u[2] = RandVal(h - r, h + r);
	}
	p->u[3] = RandVal(h - z, h + z);
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
	u[0] = 0.0;
	u[1] = 0.0;
	u[2] = 1.0;
	Rotate(u, phiL, thetaL);
	return u;
}

void Epsilon(double *u, double *w) {
	double v[3];
	v[0] = 1.0;
	v[1] = 0.0;
	v[2] = 0.0;
	Cross(u, v, w);
	double mag = Magnitude(w);
	double scale = Magnitude(u);
	for (int i = 0; i < 3; i++)
		w[i] = scale * w[i] / mag;
}

void SetInitialVel(double *vi, double m, double phi, double theta) {
	SetVec(vi, DirectionVec(phi, theta), 3);
	MultVec(vi, m);
}

void SetLaser(struct Laser *l, double E0, double phi, double theta, double xif, double omega, double psi) {
	l->E0 = E0;
	l->psi = psi;
	l->xif = xif;
	l->zetax = 0.0;
	l->zetay = 1.0;
	l->omega = omega;
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

void SetParticles(struct Particle *p, int num, double r, double h, double z, double phi, double theta, double *vi, int outputMode) {
	for(int i = 0; i < num; i++) {
		p[i].u[0] = 0;
		SetPosition(&p[i], r, h, z, i, num, outputMode);
		Rotate(&p[i].u[1], phi, theta);
		double gamma = Gamma(vi);
		p[i].u[4] = m * c * gamma;
		p[i].u[5] = m * vi[0] * gamma;
		p[i].u[6] = m * vi[1] * gamma;
		p[i].u[7] = m * vi[2] * gamma;
	}
}

void SetSharedData(struct SharedData *sdata, struct Particle *e, struct Laser *l, FILE *out, double *ochunk,
int num, int steps, double dtau, int outputMode, void (*fc)(double*, double*, double)) {
	for(int i = 0; i < CORE_NUM; i++) {
		sdata[i].l = l;
		sdata[i].e = e;
		sdata[i].id = i;
		sdata[i].fc = fc;
		sdata[i].out = out;
		sdata[i].num = num;
		sdata[i].dtau = dtau;
		sdata[i].steps = steps;
		sdata[i].ochunk = ochunk;
		sdata[i].outputMode = outputMode;
		sdata[i].finalIndex = FinalIndex(num, i);
		sdata[i].initIndex = InitialIndex(num, i);
	}
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