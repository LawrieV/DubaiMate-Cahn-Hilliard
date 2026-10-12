import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib.pyplot as plt
import numpy as np

import Task1.calculateConc as cc


def structure_factor(concentration):
    """Compute the isotropic structure factor S(k) of a concentration field."""
    concentration = concentration - concentration.mean()
    c_hat = np.fft.fft2(concentration) #fourier transform of the concentration field
    kx = np.fft.fftfreq(concentration.shape[0]) * 2 * np.pi
    ky = np.fft.fftfreq(concentration.shape[1]) * 2 * np.pi
    r = np.hypot(kx[:, None], ky[None, :]) #calculating the radius that we use in K-space
    #calculate the structure factor
    s = np.abs(c_hat) ** 2 / concentration.size
    #bin the structure factor into radial bins
    k_bins = np.linspace(0, r.max(), 100)
    s_radial = np.histogram(r, bins=k_bins, weights=s)[0] / np.histogram(r, bins=k_bins)[0]
    ks = (k_bins[:-1] + k_bins[1:]) / 2

    return ks, s_radial

 

def dominant_wavenumber(concentration):
    """Return the wavenumber with maximal structure factor amplitude."""
    ks, s_radial = structure_factor(concentration)
    if ks.size == 0:
        return 0.0
    return ks[np.argmax(s_radial)]


def characteristic_length(concentration):
    """Estimate the characteristic length scale from the Fourier peak."""
    k_max = dominant_wavenumber(concentration)
    if k_max <= 0:
        return np.inf
    return 2 * np.pi / k_max #calculating characteristic length 


# initialize concentration and run the simulation
concentration = cc.create_concfield(cc.N)

#Now do it over every time step and store the data
time = []
length_scale = []


print("Starte Simulation für Task 3...")

# Hauptschleife: Nutzt cc.advance() für den Zeitschritt
for step in range(cc.nsteps, 10*cc.nsteps): #from 10'000 to 100'000 steps
    t = step * cc.deltat
    time.append(t)
    length_scale.append(characteristic_length(concentration))


    if step < cc.nsteps:
        concentration = cc.advance(concentration)


plt.figure(figsize=(8, 6))
plt.loglog(time, length_scale, label="Characteristic Length Scale")
plt.xlabel("Time")
plt.ylabel("Characteristic Length Scale")
plt.title("Characteristic Length Scale vs Time")
plt.legend()
plt.grid()
plt.savefig("Task3/characteristic_length_vs_time.png")
plt.show()
