# ----------------------------------------------------------------------- #

class SimParameters:
    def __init__(self, i, r, num, tauf, steps, divider, substeps, core_num, output_mode, wave_count, line_angle, sweep_steps, full_trajectory):
        self.i = i
        self.r = r
        self.num = num
        self.tauf = tauf
        self.steps = steps
        self.divider = divider
        self.substeps = substeps
        self.core_num = core_num
        self.wave_count = wave_count
        self.line_angle = line_angle
        self.output_mode = output_mode
        self.sweep_steps = sweep_steps
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