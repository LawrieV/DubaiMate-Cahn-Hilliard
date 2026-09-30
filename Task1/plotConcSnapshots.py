import numpy as np
import matplotlib.pyplot as plt
import calculateConc as cc

for step, conc in cc.snapshots:
    plt.imshow(conc, cmap="RdBu", vmin=-1, vmax=1)
    plt.title(f"Concentration at step {step}")
    plt.colorbar(label="Concentration (c)")
    plt.savefig(f"Snapshots/conc_snapshot_{step}.png")
    plt.show()
    plt.close()