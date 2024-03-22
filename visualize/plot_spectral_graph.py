from typing import Union
import numpy as np
import matplotlib.pyplot as plt

def plot_spectral_graph(hs_pixels: np.array, ax: plt.Axes, plot_color: Union[str, tuple] = None, plot_std: bool = False):
    '''
    Plot a spectral graph based on hyperspectral pixel data.

    Parameters:
        hs_pixels (np.array): Hyperspectral pixel data to plot. Each row represents a pixel, and each column represents a spectral band.
        ax (matplotlib.axes.Axes): Axes object to plot the graph on.
        plot_color (str or tuple, optional): Color of the plot. If not specified, default color will be used.
        plot_std (bool, optional): Whether to plot the standard deviation as a shaded region around the average curve. Default is False.

    Returns:
        matplotlib.axes.Axes: The same Axes object after plotting the graph.
    '''
    avg = np.average(hs_pixels, axis=0)
    std = np.std(hs_pixels, axis=0)

    ax.plot(avg, color=plot_color)
    if plot_std:
        ax.fill_between(np.arange(0, len(avg), 1), (avg + std), (avg - std), color=plot_color, alpha=0.3)

    return ax