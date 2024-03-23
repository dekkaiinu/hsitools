import numpy as np


def nh9_to_array(file_path: str, height=1080, width=2048, spectral_dimension=151) -> np.array:
    '''
    Parameters:
        file_path (str): Path to the hyperspectral image file.
        height (int): Height of the image.
        width (int): Width of the image.
        spectral_dimension (int): Number of spectral dimensions.

    Returns:
        np.array: NumPy array representing the hyperspectral image data.
    '''
    with open(file_path, 'rb') as f:
        hs_array = np.fromfile(f, np.uint16, -1)
        hsi_np_array = np.reshape(hs_array, (height, spectral_dimension, width))
        hsi_np_array = np.transpose(hsi_np_array, (0, 2, 1))
        
    return hsi_np_array