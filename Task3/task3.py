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


N=256

# initialize concentration and run the simulation
concentration = cc.create_concfield(N)

start_step = cc.nsteps
end_step = 10 * cc.nsteps       # 100,000 Schritte insgesamt
sample_every = 500

time = []
length_scale = []

print("Starte Simulation für Task 3...")

for step in range(1, end_step + 1):
    concentration = cc.advance(concentration)

    if step >= start_step and (step - start_step) % sample_every == 0:
        time.append(step * cc.deltat)
        length_scale.append(characteristic_length(concentration))



#fitting the data to a power law to find the growth exponent alpha and prefactor A
#using log(L) = log(A) + alpha * log(t)

time_array = np.asarray(time)
length_array = np.asarray(length_scale)

fit_mask = (
    (time_array > 100)
    & np.isfinite(length_array)
    & (length_array > 0)
)

alpha, log_A = np.polyfit(
    np.log(time_array[fit_mask]),
    np.log(length_array[fit_mask]),
    1,
)
A = np.exp(log_A)

fit_time = np.geomspace(time_array[fit_mask].min(), time_array[fit_mask].max(), 200)
fit_length = A * fit_time**alpha

print(f"Growth exponent alpha = {alpha:.4f}")
print(f"Prefactor A = {A:.4f}")


plt.figure(figsize=(8, 6))
#plt.loglog(time, length_scale, label="Characteristic Length Scale")
plt.loglog(time_array, length_array, "o", markersize=3, label="Measured L(t)")
plt.loglog(fit_time, fit_length, "-", label=f"Fit: L = {A:.3g} t^{alpha:.3f}")
plt.xlabel("Time")
plt.ylabel("Characteristic Length Scale")
plt.title("Characteristic Length Scale vs Time")
plt.legend()
plt.grid()
plt.savefig("Images/characteristic_length_vs_time.png")
plt.show()
