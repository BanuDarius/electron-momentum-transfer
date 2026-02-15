# ----------------------------------------------------------------------- #

def get_axis_text(axis):
    if(axis == 0):
        axis_text = "X"
    elif(axis == 1):
        axis_text = "Y"
    else:
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