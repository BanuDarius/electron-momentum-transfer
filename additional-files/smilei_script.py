import math

a0_target = 0.02
omega_au = 0.057 
tf_au = 1500.0

lambda_norm = 2.0 * math.pi
t_sim = tf_au * omega_au
t_delay = 2.5 * lambda_norm
grid_size = 4.0 * lambda_norm 

Main(geometry = "1Dcartesian", interpolation_order = 2, timestep = 0.95 * (grid_size / 4096), simulation_time = t_sim + t_delay,  cell_length = [grid_size / 4096], grid_length = [grid_size], number_of_patches = [32],  EM_boundary_conditions = [["silver-muller"]], print_every = 1000)

LaserPlanar1D(box_side = "xmin", a0 = a0_target, omega = 1.0, polarization_phi = 0.0, time_envelope = constant(1.0))
LaserPlanar1D(box_side = "xmax", a0 = a0_target, omega = 1.0, polarization_phi = math.pi, time_envelope = constant(1.0))

Species(name = "electron", position_initialization = 'regular', momentum_initialization = 'cold', particles_per_cell = 1024 / 1024, mass = 1.0, charge = -1.0, number_density = trapezoidal(1.0, xvacuum=1.5*lambda_norm, xplateau=lambda_norm), is_test = True, pusher = "higueracary", time_frozen = t_delay, boundary_conditions = [["remove", "remove"]])

DiagTrackParticles(species = "electron", every = 20)