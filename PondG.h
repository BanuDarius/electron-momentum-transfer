void PotentialDerivA(double *a, double *u, struct Laser *l, int index, int n) {
	double potentialA0 = l[n].E0 * m / (l[n].omega * abs(q));
	double epsilon4[4], kVec4[4];
	kVec4[0] = 1.0;
	epsilon4[0] = 0.0;
	SetVec(&kVec4[1], l[n].n, 3);
	MultVec4(kVec4, l[n].omega / c);
	SetVec(&epsilon4[1], l[n].epsilon1, 3);
	double phi = Dot4Rel(kVec4, u) + l[n].psi;
	for(int i = 0; i < 4; i++) {
		a[i] = potentialA0 * kVec4[index] * creal(epsilon4[i] * cexp(I * phi) * (I * Env(phi, l[n].xif) + EnvPrime(phi, l[n].xif)));
	}
}

void PotentialA(double *a, double *u, struct Laser *l, int n) {
	double potentialA0 = l[n].E0 * m / (l[n].omega * abs(q));
	double epsilon4[4], kVec4[4];
	kVec4[0] = 1.0;
	epsilon4[0] = 0.0;
	SetVec(&kVec4[1], l[n].n, 3);
	MultVec4(kVec4, l[n].omega / c);
	SetVec(&epsilon4[1], l[n].epsilon1, 3);
	double phi = Dot4Rel(kVec4, u) + l[n].psi;
	for(int i = 0; i < 4; i++) {
		a[i] = potentialA0 * creal(epsilon4[i] * cexp(I * phi) * Env(phi, l[n].xif));
	}
}

double Integrate(double *u, struct Laser *l) {
	int steps = 20;
	double integral = 0.0;
	double a1[4], a1temp[4], utemp[4];
	double lambda = 2.0 * pi * c / l[0].omega, dh = lambda / (double) steps;
	
	SetVec(utemp, u, 4);
	utemp[0] -= lambda / 2.0;

	for(int i = 0; i <= steps; i++) {
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
	int steps = 20;
	double integral = 0.0;
	double a1[4], a2[4], a1temp[4], a2temp[4], utemp[4];
	double lambda = 2.0 * pi * c / l[0].omega, dh = lambda / (double) steps;

	SetVec(utemp, u, 4);
	utemp[0] -= lambda / 2.0;

	for(int i = 0; i <= steps; i++) {
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