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
    s = np.abs(c_hat) ** 2
    np.max(s) #calculate maximum of the structure factor to get the dominant wavenumber
    kx = np.fft.fftfreq(concentration.shape[0]) * 2 * np.pi
    ky = np.fft.fftfreq(concentration.shape[1]) * 2 * np.pi
    kmax = np.hypot(kx[:, None], ky[None, :])
    k_bins = np.linspace(0, kmax.max(), 100)
 

def dominant_wavenumber(concentration):
    """Return the wavenumber with maximal structure factor amplitude."""
    ks, s = structure_factor(concentration)
    if ks.size == 0:
        return 0.0
    return ks[np.argmax(s)]


def characteristic_length(concentration):
    """Estimate the characteristic length scale from the Fourier peak."""
    k_peak = dominant_wavenumber(concentration)
    if k_peak <= 0:
        return np.inf
    return 2 * np.pi / k_peak #calculating characteristic length 


# initialize concentration and run the simulation
concentration = cc.create_concfield(cc.N)
