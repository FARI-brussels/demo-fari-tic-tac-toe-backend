"""
Potential Field based path planner

author: Atsushi Sakai (@Atsushi_twi)

Ref:
https://www.cs.cmu.edu/~motionplanning/lecture/Chap4-Potential-Field_howie.pdf

Adapted for SE3 matrices and 3D space.
"""

from collections import deque
import numpy as np
import matplotlib.pyplot as plt

# Parameters
KP = 5.0  # attractive potential gain
ETA = 100.0  # repulsive potential gain
AREA_WIDTH = 30.0  # potential area width [m]
# the number of previous positions used to check oscillations
OSCILLATIONS_DETECTION_LENGTH = 3

show_animation = True

def calc_potential_field(gx, gy, gz, reso, rr, sx, sy, sz):
    minx = min(sx, gx) - AREA_WIDTH / 2.0
    miny = min(sy, gy) - AREA_WIDTH / 2.0
    minz = min(sz, gz) - AREA_WIDTH / 2.0
    maxx = max(sx, gx) + AREA_WIDTH / 2.0
    maxy = max(sy, gy) + AREA_WIDTH / 2.0
    maxz = max(sz, gz) + AREA_WIDTH / 2.0
    xw = int(round((maxx - minx) / reso))
    yw = int(round((maxy - miny) / reso))
    zw = int(round((maxz - minz) / reso))

    # calc each potential
    pmap = [[[0.0 for _ in range(zw)] for _ in range(yw)] for _ in range(xw)]

    for ix in range(xw):
        x = ix * reso + minx

        for iy in range(yw):
            y = iy * reso + miny

            for iz in range(zw):
                z = iz * reso + minz
                ug = calc_attractive_potential(x, y, z, gx, gy, gz)
                uo = calc_repulsive_potential(x, y, z, rr)
                uf = ug + uo
                pmap[ix][iy][iz] = uf

    return pmap, minx, miny, minz

def calc_attractive_potential(x, y, z, gx, gy, gz):
    return 0.5 * KP * np.hypot(np.hypot(x - gx, y - gy), z - gz)

def calc_repulsive_potential(x, y, z, rr):
    # Obstacle plane at z = a
    a = 5.0  # Replace with the desired z limit

    # Distance to the obstacle plane
    dq = abs(z - a)

    if dq <= rr:
        if dq <= 0.1:
            dq = 0.1
        return 0.5 * ETA * (1.0 / dq - 1.0 / rr) ** 2
    else:
        return 0.0

def get_motion_model():
    # dx, dy, dz
    motion = [
        [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1],
        [1, 1, 0], [1, -1, 0], [-1, 1, 0], [-1, -1, 0],
        [1, 0, 1], [1, 0, -1], [-1, 0, 1], [-1, 0, -1],
        [0, 1, 1], [0, 1, -1], [0, -1, 1], [0, -1, -1]
    ]

    return motion

def oscillations_detection(previous_ids, ix, iy, iz):
    previous_ids.append((ix, iy, iz))

    if len(previous_ids) > OSCILLATIONS_DETECTION_LENGTH:
        previous_ids.popleft()

    # check if contains any duplicates by copying into a set
    previous_ids_set = set()
    for index in previous_ids:
        if index in previous_ids_set:
            return True
        else:
            previous_ids_set.add(index)
    return False

def potential_field_planning(sx, sy, sz, gx, gy, gz, reso, rr):
    # calc potential field
    pmap, minx, miny, minz = calc_potential_field(gx, gy, gz, reso, rr, sx, sy, sz)

    # search path
    d = np.hypot(np.hypot(sx - gx, sy - gy), sz - gz)
    ix = round((sx - minx) / reso)
    iy = round((sy - miny) / reso)
    iz = round((sz - minz) / reso)
    gix = round((gx - minx) / reso)
    giy = round((gy - miny) / reso)
    giz = round((gz - minz) / reso)

    if show_animation:
        #draw_heatmap(pmap)
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect('key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
        plt.plot(ix, iy, iz, "*k")
        plt.plot(gix, giy, giz, "*m")

    rx, ry, rz = [sx], [sy], [sz]
    motion = get_motion_model()
    previous_ids = deque()

    while d >= reso:
        minp = float("inf")
        minix, miniy, miniz = -1, -1, -1
        for i, _ in enumerate(motion):
            inx = int(ix + motion[i][0])
            iny = int(iy + motion[i][1])
            inz = int(iz + motion[i][2])
            if inx >= len(pmap) or iny >= len(pmap[0]) or inz >= len(pmap[0][0]) or inx < 0 or iny < 0 or inz < 0:
                p = float("inf")  # outside area
                print("outside potential!")
            else:
                p = pmap[inx][iny][inz]
            if minp > p:
                minp = p
                minix = inx
                miniy = iny
                miniz = inz
        ix = minix
        iy = miniy
        iz = miniz
        xp = ix * reso + minx
        yp = iy * reso + miny
        zp = iz * reso + minz
        d = np.hypot(np.hypot(gx - xp, gy - yp), gz - zp)
        rx.append(xp)
        ry.append(yp)
        rz.append(zp)

        if oscillations_detection(previous_ids, ix, iy, iz):
            print("Oscillation detected at ({},{},{})!".format(ix, iy, iz))
            break

        if show_animation:
            plt.plot(ix, iy, iz, ".r")
            plt.pause(0.01)

    print("Goal!!")

    return rx, ry, rz

def draw_heatmap(data):
    data = np.array(data).T
    plt.pcolor(data, vmax=100.0, cmap=plt.cm.Blues)

def main():
    print("potential_field_planning start")

    start_SE3 = np.eye(4)
    goal_SE3 = np.eye(4)
    start_SE3[:3, 3] = [0.0, 10.0, 5.0]  # Start position [x, y, z]
    goal_SE3[:3, 3] = [30.0, 30.0, 5.0]  # Goal position [x, y, z]

    sx, sy, sz = start_SE3[:3, 3]
    gx, gy, gz = goal_SE3[:3, 3]
    grid_size = 0.5  # potential grid size [m]
    robot_radius = 5.0  # robot radius [m]

    if show_animation:
        plt.grid(True)
        plt.axis("equal")

    # path generation
    _, _, _ = potential_field_planning(sx, sy, sz, gx, gy, gz, grid_size, robot_radius)

    if show_animation:
        plt.show()

if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")
