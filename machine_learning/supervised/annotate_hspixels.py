import numpy as np

def annotate_hspixels(hs_pixels: np.array, label: int):
    '''
    Annotate hyperspectral pixels with the specified label

    Parameters:
        hs_pixels (np.array): Input hyperspectral pixels. shape=(number of data, band)
        label (int): Annotation label

    Returns:
        np.array: Labels corresponding to pixels
    '''
    return np.array([label] * hs_pixels.shape[0])

def annotate_hspixels_list(hs_pixels_list, label_list):
    '''
    Annotate the list of hyperspectral pixels with their respective specified labels

    Parameters:
        hs_pixels (list): Input hyperspectral pixels. shape=(number of data, band)
        label (list): Annotation label

    Returns:
        np.array: Labels corresponding to pixels
    '''
    labels_list = []
    for hs_pixels, label in zip(hs_pixels_list, label_list):
        labels_list.append(annotate_hspixels(hs_pixels, label))
    return labels_list