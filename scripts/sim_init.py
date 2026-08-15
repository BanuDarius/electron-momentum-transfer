'''MIT License

Copyright (c) 2026 Banu Darius-Matei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"
filename_out = f"{OUTPUT_DIR}/out-data.bin"

# ----------------------------------------------------------------------- #

class SimParameters:
    def __init__(self, i, r_min, r_max, num, tf, steps, divider, substeps, v0_mag, phi_v0, theta_v0, thread_num, output_mode, rotate_angle, sweep_steps, full_trajectory, wavelength, c_value):
        self.i = i
        self.tf = tf
        self.mode = 0
        self.num = num
        self.steps = steps
        self.r_min = r_min
        self.r_max = r_max
        self.v0_mag = v0_mag
        self.phi_v0 = phi_v0
        self.square_size = 1
        self.divider = divider
        self.c_value = c_value
        self.theta_v0 = theta_v0
        self.substeps = substeps
        self.thread_num = thread_num
        self.wavelength = wavelength
        self.output_final_pos = False
        self.check_convergence = False
        self.check_polarization = False
        self.output_mode = output_mode
        self.sweep_steps = sweep_steps
        self.filename_out = filename_out
        self.rotate_angle = rotate_angle
        self.full_trajectory = full_trajectory
        self.filename_out = OUTPUT_DIR / "out-data.bin"
        self.filename_lasers = f"{INPUT_DIR}/lasers.txt"
        self.filename_parameters = f"{INPUT_DIR}/input.txt"

# ------------------------------------------------------- #

class LaserParameters:
    def __init__(self, a0, sigma, omega, etaf, zetax, zetay, alpha, phi, theta, psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss):
        self.a0 = a0
        self.etaf = etaf
        self.phi = phi
        self.psi = psi
        self.sigma = sigma
        self.zetax = zetax
        self.zetay = zetay
        self.alpha = alpha
        self.omega = omega
        self.theta = theta
        self.pond_integrate_steps = pond_integrate_steps
        
        self.use_gaussian = use_gaussian
        self.w0 = w0
        self.zeta_x_gauss = zeta_x_gauss
        self.zeta_y_gauss = zeta_y_gauss

# ------------------------------------------------------- #