import numpy as np
import matplotlib.pyplot as plt



def draw_spectral_graphs_figure(fig: plt.Figure, hs_pixels_list: list, label_list: list, plot_color_list: list, 
                                plot_axes: np.array, subplot_graph_title_list: list = None, plot_std=True):
    for i, hs_pixels, color, label, subplot_grath_title in enumerate(zip(hs_pixels_list, plot_color_list, label_list, subplot_graph_title_list)):
        ax = fig.add_subplot(plot_axes[0], plot_axes[1], i)
        ax = plot_spectral_graph(hs_pixels, ax, plot_color=color, label=label, plot_std=plot_std)
        ax.set_title(subplot_grath_title)


    
    for i in range(8):
        new_labels.append(wavelength)
        new_values.append(i * 20)
        wavelength = wavelength + 100



def save_spectral_graphs_figure(hs_pixels_list: list, label_list: list, plot_color_list: list, 
                                plot_axes: np.array, subplot_graph_title_list: list = None, graph_title: str=None, std=True):
    # plt.rcParams.update({'font.size': 20})
    new_labels = []
    new_values = []
    wavelength = 350

    plt.xticks(new_values, new_labels)
    plt.xlabel('Wavelength(mm)', fontsize=14)
    plt.ylabel('Intensity', fontsize=14)
    plt.ylim(0, 2300)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=14)
    plt.savefig(save_name + '.png')
    return 0