import os
import numpy as np

def hs2rgb(hsi: np.array, lower_limit_wavelength: int=350, upper_limit_wavelength: int=1100, spectrum_stepsize: int=5, color_matching_function: np.array = None):
    '''
    Parameters:
        hsi (np.array): hyperspectral image (height, width, band)
        lower_limit_wavelength (int): lower limit wavelength of hsi
        upper_limit_wavelength (int): upper_limit_wavelength of hsi
        spectrum_stemsize (int): wavelength range between hsi channels
        color_matching_function (np.array): color matching function

    Returns:
        np.array: NumPy array of RGB images converted from hyperspectral images
    '''

    hsi = hsi.astype(np.float32)
    height, width = hsi.shape[0], hsi.shape[1]

    if not color_matching_function:
        color_function_path=os.path.join(os.path.dirname(__file__), 'cie_functions', '10-deg-XYZ-CMFs.csv')
        color_matching_function = np.loadtxt(color_function_path, delimiter=",")
        color_matching_function = color_matching_function[::spectrum_stepsize] 

    wave_length = np.arange(lower_limit_wavelength, upper_limit_wavelength + 1, spectrum_stepsize)

    index_low, index_hight = int(np.where(wave_length == color_matching_function[0, 0])[0]), int(np.where(wave_length == color_matching_function[-1, 0])[0]) + 1

    hsi_cie_range = hsi[:, :, index_low : index_hight]

    img_xyz = np.zeros((height, width, 3))
    img_rgb = np.zeros((height, width, 3))

    M = np.array([[0.41844, -0.15866, -0.08283],
                  [-0.09117, 0.25242, 0.01570],
                  [0.00092, -0.00255, 0.17858]])
    
    intensity = hsi_cie_range.reshape(-1, index_hight - index_low)
    
    xyz = np.dot(intensity, color_matching_function[:, 1:])

    img_xyz = xyz.reshape(height, width, 3)

    img_rgb = np.dot(img_xyz, M.T)

    img_rgb = ((img_rgb - np.min(img_rgb)) / (np.max(img_rgb) - np.min(img_rgb)) * 255).astype(np.uint8)

    img_rgb_gamma  = gamma_correction(img_rgb, gamma=1.9, max_value=255)
    return img_rgb_gamma

def gamma_correction(img: np.array, gamma: float=2.2, max_value: int=65535, base_max_value: int=255):
    
    img = img.astype(np.float32) / max_value
    img = img ** (1.0 / gamma)
    img = img * base_max_value
    if base_max_value == 255:
        img = img.astype(np.uint8)
    elif base_max_value == 65535:
        img = img.astype(np.uint16)

    return img