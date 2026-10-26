from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

N = 128
deltat = 0.01
mobility = 1.0
kappa = 1.0
alpha = 1.0

deltax = 1.0
nsteps = 10000


def laplacian(field):
    """Five-point Laplacian with periodic boundary conditions."""
    return (
        (np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        - 4 * field)/(deltax**2)
    )





def advance(concentration, alpha):
    """Calculate the concentration field one time step later."""
    chemical_potential = (
        concentration**3 - concentration - alpha
        - kappa * laplacian(concentration)
    )
    return concentration + deltat * mobility * laplacian(chemical_potential)


def create_concfield(n):
    rng = np.random.default_rng(0)
    concentration = rng.uniform(-1, 1, size=(n, n))
    return concentration

def run_simulation(alpha):
    concentration = create_concfield(N)
    snapshots = [(0, concentration.copy())]

    for step in range(1, nsteps + 1):
        concentration = advance(concentration, alpha)

        if step % 500 == 0:
            snapshots.append((step, concentration.copy()))

    return snapshots


def save_initial_and_final_snapshots(alpha, snapshots):
    output_dir = (
        Path(__file__).parent
        / "Snapshots"
        / "NonConvex"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    for step, concentration in (snapshots[0], snapshots[-1]):
        plt.figure()
        plt.imshow(concentration, cmap="RdBu", vmin=-1, vmax=1)
        plt.title(f"Concentration at step {step} (alpha={alpha:g})")
        plt.colorbar(label="Concentration (c)")
        plt.savefig(output_dir / f"conc_snapshot_{step}.png", bbox_inches="tight")
        plt.close()


if __name__ == "__main__":
    save_initial_and_final_snapshots(alpha, run_simulation(alpha))