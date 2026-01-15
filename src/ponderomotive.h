void PotentialDerivA(double *a, double *u, struct Laser *l, int index, int n) {
	double potentialA0 = l[n].E0 * m / (l[n].omega * fabs(q));
	double epsilon4[4], kVec4[4];

	kVec4[0] = 1.0;
	epsilon4[0] = 0.0;
	SetVec(&kVec4[1], l[n].n, 3);
	MultVec4(kVec4, l[n].omega / c);

	double phi = Dot4Rel(kVec4, u) + l[n].psi;
	a[0] = 0.0;
	double sign = (index > 0) ? -1.0 : +1.0;
	for(int i = 0; i < 3; i++) {
		double t1 = l[n].epsilon1[i] * l[n].zetax * (-sin(phi)) + l[n].epsilon2[i] * l[n].zetay * cos(phi);
		double t2 = l[n].epsilon1[i] * l[n].zetax * (-cos(phi)) + l[n].epsilon2[i] * l[n].zetay * (-sin(phi));
		a[i+1] = sign * potentialA0 * kVec4[index] * (Env(phi, l[n].xif) * t2 + EnvPrime(phi, l[n].xif) * t1);
	}
}

void PotentialA(double *a, double *u, struct Laser *l, int n) {
	double potentialA0 = l[n].E0 * m / (l[n].omega * fabs(q));
	double epsilon4[4], kVec4[4];

	kVec4[0] = 1.0;
	epsilon4[0] = 0.0;
	SetVec(&kVec4[1], l[n].n, 3);
	MultVec4(kVec4, l[n].omega / c);

	double phi = Dot4Rel(kVec4, u) + l[n].psi;
	double A0mult = Env(phi, l[n].xif) * potentialA0;
	a[0] = 0.0;
	for(int i = 0; i < 3; i++)
		a[i+1] = (l[n].epsilon1[i] * l[n].zetax * (-sin(phi)) + l[n].epsilon2[i] * l[n].zetay * cos(phi));
	MultVec(&a[1], A0mult);
}

double Integrate(double *u, struct Laser *l) {
	double integral = 0.0;
	double a1[4], a1temp[4], utemp[4];
	double lambda = 2.0 * pi * c / l[0].omega, dh = lambda / (double) PONDEROMOTIVE_STEPS;
	
	SetVec(utemp, u, 4);
	utemp[0] -= lambda / 2.0;

	for(int i = 0; i < PONDEROMOTIVE_STEPS; i++) {
		SetZeroN(a1, 4);
		for(int j = 0; j < 2; j++) {
			PotentialA(a1temp, utemp, l, j);
			AddVec4(a1, a1temp);
		}
		integral += dh * Dot4Rel(a1, a1);
		utemp[0] += dh;
	}
	return integral;
}

double IntegrateDMUDA(double *u, struct Laser *l, int index) {
	double integral = 0.0;
	double a1[4], a2[4], a1temp[4], a2temp[4], utemp[4];
	double lambda = 2.0 * pi * c / l[0].omega, dh = lambda / (double) PONDEROMOTIVE_STEPS;

	SetVec(utemp, u, 4);
	utemp[0] -= lambda / 2.0;

	for(int i = 0; i < PONDEROMOTIVE_STEPS; i++) {
		SetZeroN(a1, 4); SetZeroN(a2, 4);
		for(int j = 0; j < 2; j++) {
			PotentialA(a1temp, utemp, l, j);
			PotentialDerivA(a2temp, utemp, l, index, j);
			AddVec4(a1, a1temp);
			AddVec4(a2, a2temp);
		}
		integral += dh * Dot4Rel(a1, a2);
		utemp[0] += dh;
	}
	return integral;
}

double ComputeA(double *u, struct Laser *l) {
	double lambda = 2.0 * pi * c / l[0].omega;
	double a = - (q * q) / (m * m * c * c) * (1.0 / lambda);
	a *= Integrate(u, l);
	return a;
}

double DerivativeA(double *u, struct Laser *l, int index) {
	double lambda = 2.0 * pi * c / l[0].omega;
	double dmuda = - 2.0 * (q * q) / (m * m * c * c ) * (1.0 / lambda);
	dmuda *= IntegrateDMUDA(u, l, index);
	return dmuda;
}

void ponderomotive(double *u, double *up, const double t) {
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

void SetMode(void (**computeFunction)(double *, double *, double), int mode) {
	if(mode == 0)
		*computeFunction = electromag;
	else if(mode == 1)
		*computeFunction = ponderomotive;
}