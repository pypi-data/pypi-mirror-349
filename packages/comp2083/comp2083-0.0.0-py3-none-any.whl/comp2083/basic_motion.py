from random import random

GRAVITY_ACC = 9.81


def generate_positions(time_grid,
                       x_0=0.0, v_0=0.0, a_0=0.0,
                       motion_type="constant velocity",
                       is_experimental=False):
    rand = lambda : 2 * random() - 1
    if motion_type=="constant velocity":
        acc = 0.0
        vel = v_0 if v_0 != 0 else rand() * GRAVITY_ACC
    elif motion_type=="constant acceleration":
        acc = a_0 if a_0 != 0 else rand() * GRAVITY_ACC
        vel = v_0 if v_0 != 0 else rand() * GRAVITY_ACC
    elif motion_type == "free fall":
        acc = GRAVITY_ACC
        vel = v_0

    positions = []
    for t in time_grid:
        pos = x_0 + vel * t + 0.5 * acc * t ** 2
        positions.append(pos)
    if is_experimental:
        pos_const = (0.01*max(positions) - min(positions)) / 200
        for i in range(len(positions)):
            positions[i] += rand() * pos_const

    return positions


def charge_density():
    pass
