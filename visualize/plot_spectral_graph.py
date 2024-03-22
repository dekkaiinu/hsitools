import numpy as np
import matplotlib.pyplot as plt

def plot_spectral_graph(hs_pixels, ax, plot_color=None, plot_std=False):
    avg = np.average(hs_pixels, axis=0)
    std = np.std(hs_pixels, axis=0)

    ax.plot(avg, color=plot_color)
    if plot_std:
        ax.fill_between(np.arange(0, len(avg), 1), (avg + std), (avg - std), color=plot_color, alpha=0.3)

    return ax