import os
import sys

# Fügt das Hauptverzeichnis automatisch zum Python-Suchpfad hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib.pyplot as plt
import numpy as np

import Task1.calculateConc as cc


def compute_mass(c):
    """Berechnet die Gesamtmasse m(t)."""
    return np.sum(c) * (cc.deltax**2)


def compute_energy(c):
    """Berechnet die freie Energie F(t)."""
    # 1. Lokale Energiedichte f(c)
    f_c = ((c**2 - 1) ** 2) / 4.0

    # 2. Gradienten via zentrale Differenzen
    grad_x = (np.roll(c, -1, axis=0) - np.roll(c, 1, axis=0)) / (2 * cc.deltax)
    grad_y = (np.roll(c, -1, axis=1) - np.roll(c, 1, axis=1)) / (2 * cc.deltax)
    grad_sq = grad_x**2 + grad_y**2

    # 3. Summe der Energie über das gesamte Gitter
    return np.sum(f_c + 0.5 * cc.kappa * grad_sq) * (cc.deltax**2)


# Initialisierung der Simulation mit euren Parametern aus Task 1
rng = np.random.default_rng(0)
concentration = rng.uniform(-1, 1, size=(cc.N, cc.N))

times = []
masses = []
energies = []

num_steps = 10001

print("Starte Simulation für Task 2...")

# Hauptschleife: Nutzt cc.advance() für den Zeitschritt
for step in range(num_steps + 1):
    t = step * cc.deltat
    times.append(t)
    masses.append(compute_mass(concentration))
    energies.append(compute_energy(concentration))

    if step < num_steps:
        concentration = cc.advance(concentration)

# Ordner für Plots erstellen und Diagramme speichern
os.makedirs("images", exist_ok=True)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Massenerhaltung
ax1.plot(times, masses, color="blue", linewidth=1.5)
ax1.set_xlabel("Zeit t")
ax1.set_ylabel("Gesamtmasse m(t)")
ax1.set_title("Massenerhaltung")
ax1.grid(True)

# Plot 2: Energiedissipation
ax2.plot(times, energies, color="red", linewidth=1.5)
ax2.set_xlabel("Zeit t")
ax2.set_ylabel("Freie Energie F(t)")
ax2.set_title("Energie-Dissipation")
ax2.grid(True)

plt.tight_layout()
plt.savefig("images/task2-mass-energy.png")
plt.show()

# Auswertung ausgeben
mass_dev = np.max(np.abs(np.array(masses) - masses[0]))
print("Fertig!")
print(f"Maximale Massenabweichung: {mass_dev:.2e}")
print("Plot wurde erfolgreich unter 'images/task2-mass-energy.png' gespeichert.")