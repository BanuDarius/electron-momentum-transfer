double rk4 ( double t0, double u0, double dt, double f ( double t, double u ) );
void rk4vec ( double t0, int n, double u0[], double dt, struct Laser *l, double *u,
double *f ( double t, int n, double u[], struct Laser *l) );
void timestamp ( void );