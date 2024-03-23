from typing import Union
import numpy as np
import matplotlib.pyplot as plt

def plot_spectral_graph(hs_pixels: np.array, ax: plt.Axes, plot_color: Union[str, tuple] = None, label: str=None, plot_std: bool = False):
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
    if plot_std:
        std = np.std(hs_pixels, axis=0)
        ax.fill_between(np.arange(0, len(avg), 1), (avg + std), (avg - std), color=plot_color, alpha=0.3)
    
    if label:
        ax.plot(avg, color=plot_color, label=label)
        ax.legend()
    else:
        ax.plot(avg, color=plot_color)

    return ax

def plot_spectrals_graph(hs_pixels_list: list, ax: plt.Axes, plot_color_list: list=[], label_list: list=[], plot_std: bool=False):
    '''
    Plot spectral graphs for multiple sets of hyperspectral pixel data.

    Parameters:
        hs_pixels_list (list of np.array): List of hyperspectral pixel data arrays to plot. Each array represents a set of pixels, where each row represents a pixel and each column represents a spectral band.
        ax (matplotlib.axes.Axes): Axes object to plot the graph on.
        plot_color_list (list of str or tuple): List of colors for each plotted curve. Each color can be specified as a string or a tuple.
        label_list (list of str, optional): List of labels for the plotted curves. If provided, each label will be associated with the corresponding set of pixels.
        plot_std (bool, optional): Whether to plot the standard deviation as a shaded region around the average curve for each set of pixels. Default is False.

    Returns:
        matplotlib.axes.Axes: The same Axes object after plotting the graph.
    '''
    if len(plot_color_list) == 0 & len(label_list) > 0:
        for hs_pixels, label in zip(hs_pixels_list, label_list):
            ax = plot_spectral_graph(hs_pixels, ax, label=label, plot_std=plot_std)
    elif len(label_list) == 0 & len(plot_color_list) > 0:
        for hs_pixels, plot_color in zip(hs_pixels_list, plot_color_list):
            ax = plot_spectral_graph(hs_pixels, ax, plot_color=plot_color,  plot_std=plot_std)
    elif len(plot_color_list) == 0 & len(label_list) == 0:
        for hs_pixels in hs_pixels_list:
            ax = plot_spectral_graph(hs_pixels, ax, plot_std=plot_std)
    else:
        for hs_pixels, plot_color, label in zip(hs_pixels_list, plot_color_list, label_list):
            ax = plot_spectral_graph(hs_pixels, ax, plot_color=plot_color, label=label, plot_std=plot_std)
    return ax

def set_grath_spectralscale(ax, marks_number: int=8, spectral_start_end: np.array=np.array((350, 1150)), band_num: int=151):    
    spectral_range = spectral_start_end[1] - spectral_start_end[0]
    spectral_interval = int(spectral_range / marks_number)
    band_interval = int(band_num / marks_number)

    new_labels = []
    new_values = []
    wavelength = spectral_start_end[0]

    for i in range(marks_number + 1):
        new_labels.append(wavelength)
        new_values.append(i * band_interval)
        wavelength = wavelength + spectral_interval

    ax.set_xticks(new_values)
    ax.set_xticklabels(new_labels)

    return ax