from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

N = 128
deltat = 0.01
mobility = 1.0
kappa = 1.0
chi = 2.5

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





def advance(concentration, chi):
    """Calculate the concentration field one time step later."""
    chemical_potential = (
        np.log(concentration) - np.log(1 - concentration) + chi*(1 - 2*concentration)
        - kappa * laplacian(concentration)
    )
    return concentration + deltat * mobility * laplacian(chemical_potential)


def create_concfield(n):
    rng = np.random.default_rng(0)
    concentration = rng.uniform(0.45, 0.55, size=(n, n))
    return concentration

def run_simulation(chi):
    concentration = create_concfield(N)
    snapshots = [(0, concentration.copy())]

    for step in range(1, nsteps + 1):
        concentration = advance(concentration, chi)

        if step % 500 == 0:
            snapshots.append((step, concentration.copy()))

    return snapshots


def save_initial_and_final_snapshots(chi, snapshots):
    output_dir = (
        Path(__file__).parent
        / "Snapshots"
        / "FloryHuggins"
        / f"chi_{chi:g}"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    for step, concentration in (snapshots[0], snapshots[-1]):
        plt.figure()
        plt.imshow(concentration, cmap="RdBu", vmin=0, vmax=1)
        plt.title(f"Concentration at step {step} (chi={chi:g})")
        plt.colorbar(label="Concentration (c)")
        plt.savefig(output_dir / f"conc_snapshot_{step}.png", bbox_inches="tight")
        plt.close()


if __name__ == "__main__":
    save_initial_and_final_snapshots(chi, run_simulation(chi))