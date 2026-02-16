from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
filename_out = f"{OUTPUT_DIR}/out-data.bin"

# ----------------------------------------------------------------------- #

class SimParameters:
    def __init__(self, i, r_min, r_max, num, tf, steps, divider, substeps, core_num, output_mode, rotate_angle, sweep_steps, full_trajectory, wavelength, c_value):
        self.i = i
        self.tf = tf
        self.num = num
        self.steps = steps
        self.r_min = r_min
        self.r_max = r_max
        self.divider = divider
        self.c_value = c_value
        self.substeps = substeps
        self.core_num = core_num
        self.wavelength = wavelength
        self.check_convergence = False
        self.output_mode = output_mode
        self.sweep_steps = sweep_steps
        self.filename_out = filename_out
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