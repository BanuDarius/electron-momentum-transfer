#ifndef HC_FUNC
#define HC_FUNC

//Declarations for functions needed for the Higuera-Cary push

double hc_s_factor(double *t_rot);
void hc_beta(double *beta, double *B, double dt);
void hc_epsilon(double *epsilon, double *E, double dt);
void hc_t_rot(double *t_rot, double *beta, double gamma_new);
void hc_u_minus(double *u_minus, double *u_i, double *epsilon);
void hc_u_prime(double *u_prime, double *u_minus, double *t_rot);
double hc_gamma_new(double *u_minus, double *beta, double gamma_minus);
void hc_u_plus(double *u_plus, double *u_minus, double *u_prime, double s_factor, double *t_rot);

#endif