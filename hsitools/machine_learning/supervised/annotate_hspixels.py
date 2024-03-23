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
    Annotate lists of hyperspectral pixels with corresponding labels.

    Parameters:
        hs_pixels_list (list of np.array): List of input hyperspectral pixel arrays.
            Each array should have shape (number of data, band).
        label_list (list of int): List of annotation labels corresponding to each set of pixels.

    Returns:
        list of np.array: List of labels corresponding to each set of pixels.
    '''
    labels_list = []
    for hs_pixels, label in zip(hs_pixels_list, label_list):
        labels_list.append(annotate_hspixels(hs_pixels, label))
    return labels_list