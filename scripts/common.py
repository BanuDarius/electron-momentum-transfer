# ----------------------------------------------------------------------- #

def get_axis_text(axis):
    if(axis == 0):
        axis_text = "X"
    elif(axis == 1):
        axis_text = "Y"
    elif(axis == 2):
        axis_text = "Z"
    return axis_text

# ----------------------------------------------------------------------- #

def interpolate(min_v, max_v, i, f):
    return min_v + (max_v - min_v) * i / f
    
def modulo_steps(s, substep):
    modulo = s % substep
    if(modulo != 0):
        s -= modulo
    return s

# ----------------------------------------------------------------------- #

def output_all_parameters(sim_parameters, lasers):
    filename_parameters = sim_parameters.filename_parameters
    filename_lasers = sim_parameters.filename_lasers
    
    mode = sim_parameters.mode
    output_mode = int(sim_parameters.output_mode == True)
    check_polarization = int(sim_parameters.check_polarization == True)
    
    with open(filename_parameters, "w") as file:
        file.write(f"r_min {sim_parameters.r_min}\n")
        file.write(f"r_max {sim_parameters.r_max}\n")
        file.write(f"num {sim_parameters.num}\n")
        file.write(f"tf {sim_parameters.tf}\n")
        file.write(f"steps {sim_parameters.steps}\n")
        file.write(f"substeps {sim_parameters.substeps}\n")
        file.write(f"thread_num {sim_parameters.thread_num}\n")
        file.write(f"output_mode {output_mode}\n")
        file.write(f"mode {mode}\n")
        file.write(f"check_polarization {check_polarization}\n")
        file.write(f"rotate_angle {sim_parameters.rotate_angle}\n")
        file.write(f"num_lasers {len(lasers)}\n")
        file.write(f"v0_mag {sim_parameters.v0_mag}")
        file.write(f"phi_v0 {sim_parameters.phi_v0}")
        file.write(f"theta_v0 {sim_parameters.theta_v0}")
    
    with open(filename_lasers, "w") as file:
        for i in range(len(lasers)):
            file.write(f"a0 {lasers[i].a0}\n")
            file.write(f"sigma {lasers[i].sigma}\n")
            file.write(f"omega {lasers[i].omega}\n")
            file.write(f"xif {lasers[i].xif}\n")
            file.write(f"zetax {lasers[i].zetax}\n")
            file.write(f"zetay {lasers[i].zetay}\n")
            file.write(f"phi {lasers[i].phi}\n")
            file.write(f"theta {lasers[i].theta}\n")
            file.write(f"psi {lasers[i].psi}\n")
            file.write(f"alpha {lasers[i].alpha}\n")
            file.write(f"pond_integrate_steps {lasers[i].pond_integrate_steps}\n")

# ----------------------------------------------------------------------- #