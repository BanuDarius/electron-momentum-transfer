# ----------------------------------------------------------------------- #

class SimParameters:
    def __init__(self, i, r, num, tf, steps, divider, substeps, core_num, output_mode, wave_count, rotate_angle, sweep_steps, full_trajectory):
        self.i = i
        self.r = r
        self.tf = tf
        self.num = num
        self.steps = steps
        self.divider = divider
        self.substeps = substeps
        self.core_num = core_num
        self.wave_count = wave_count
        self.output_mode = output_mode
        self.sweep_steps = sweep_steps
        self.rotate_angle = rotate_angle
        self.full_trajectory = full_trajectory

# ------------------------------------------------------- #

class LaserParameters:
    def __init__(self, a0, sigma, omega, xif, zetax, zetay, phi, theta, psi, pond_integrate_steps):
        self.a0 = a0
        self.xif = xif
        self.phi = phi
        self.psi = psi
        self.sigma = sigma
        self.zetax = zetax
        self.zetay = zetay
        self.omega = omega
        self.theta = theta
        self.pond_integrate_steps = pond_integrate_steps

# ------------------------------------------------------- #