import numpy as np

def extract_pixels_from_hsi(hsi: np.array, area: np.array):
    '''
    Extract pixels from a hyperspectral image (HSI) within the specified area.

    Parameters:
        hsi (np.array): Input hyperspectral image.
        area (np.array): Array specifying the area of interest in the image.
            Format: [start_row, start_column, end_row, end_column]

    Returns:
        np.array: Extracted pixels within the specified area.
    '''
    return hsi[area[0]:area[2], area[1]:area[3], :].reshape(-1, hsi.shape[2])

def extract_pixels_from_hsi_mask(hsi: np.array, mask_img: np.array):
    '''
    Extract pixels from a hyperspectral image (HSI) using a binary mask.

    Parameters:
        hsi (np.array): Input hyperspectral image.
        mask_img (np.array): Binary mask image where 255 indicates regions of interest.

    Returns:
        np.array: Extracted pixels from the HSI corresponding to the regions specified by the mask.
    '''
    return hsi[mask_img == 255]
