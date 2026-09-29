import numpy as np
import matplotlib.pyplot as plt

N = 128
deltat = 0.01
mobility = 1.0
kappa = 1.0

deltax = 1.0


def laplacian(field):
    """Five-point Laplacian with periodic boundary conditions."""
    result = np.zeros_like(field, dtype=float)
    rows, columns = field.shape

    for x in range(rows):
        for y in range(columns):
            result[x, y] = (
                field[(x + 1) % rows, y]
                + field[(x - 1) % rows, y]
                + field[x, (y + 1) % columns]
                + field[x, (y - 1) % columns]
                - 4 * field[x, y]
            ) / (deltax**2)

    return result


def advance(concentration):
    """Calculate the concentration field one time step later."""
    chemical_potential = (
        concentration**3 - concentration
        - kappa * laplacian(concentration)
    )
    return concentration + deltat * mobility * laplacian(chemical_potential)

############################## SANITY CHECKS ##############################

constant_field = np.ones((N, N))
assert np.allclose(laplacian(constant_field), 0)

rng = np.random.default_rng(0)
concentration = rng.uniform(-0.1, 0.1, size=(N, N))
initial_mean = concentration.mean()

for i in range(10):
    concentration = advance(concentration)

print("Mean concentration change:", concentration.mean() - initial_mean)

############################## SANITY CHECKS ##############################