import numpy as np
import matplotlib.pyplot as plt

N = 128
deltat = 0.01
mobility = 1.0
kappa = 1.0

deltax = 1.0
nsteps = 10000

############################## LAPLACIAN FUNCTION USED INITIALLY (TOO SLOW) ##############################

#def laplacian(field):
#    """Five-point Laplacian with periodic boundary conditions."""
#    result = np.zeros_like(field, dtype=float)
#    rows, columns = field.shape
#
#    for x in range(rows):
#        for y in range(columns):
#            result[x, y] = (
#                field[(x + 1) % rows, y]
#                + field[(x - 1) % rows, y]
#                + field[x, (y + 1) % columns]
#                + field[x, (y - 1) % columns]
#                - 4 * field[x, y]
#            ) / (deltax**2)
#
#    return result

##########################################################################################################


def laplacian(field):
    """Five-point Laplacian with periodic boundary conditions."""
    return (
        (np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        - 4 * field)/(deltax**2)
    )





def advance(concentration):
    """Calculate the concentration field one time step later."""
    chemical_potential = (
        concentration**3 - concentration
        - kappa * laplacian(concentration)
    )
    return concentration + deltat * mobility * laplacian(chemical_potential)


def create_concfield(n):
    rng = np.random.default_rng(0)
    concentration = rng.uniform(-1, 1, size=(n, n))
    return concentration

concentration = create_concfield(N)

initial_mean = concentration.mean()

############################## SANITY CHECKS ##############################

#constant_field = np.ones((N, N))
#assert np.allclose(laplacian(constant_field), 0)


#for i in range(10):
#    concentration = advance(concentration)

#print("Mean concentration change:", concentration.mean() - initial_mean)

############################## SANITY CHECKS ##############################

snapshots = [(0, concentration.copy())]

for step in range(1, nsteps + 1):
    concentration = advance(concentration)

    if step % 500 == 0:
        snapshots.append((step, concentration.copy()))