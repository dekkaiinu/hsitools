import numpy as np
import cv2

def hsi_blur(hsi: np.array, kernel_size: int=5):
    '''
    Apply blurring to an HSI image.

    Parameters:
        hsi (np.array): Input HSI image.
        kernel_size (int): Size of the Gaussian kernel. Default is 5.

    Returns:
        np.array: Smoothed HSI image.
    '''
    blur_func = cv2.blur
    smooth_hsi = integration_smooth_images_for_blur(hsi, blur_func, kernel_size)

    return smooth_hsi


def hsi_gaussian_blur(hsi: np.array, kernel_size: int=5):
    '''
    Apply Gaussian blurring to an HSI image.

    Parameters:
        hsi (np.array): Input HSI image.
        kernel_size (int): Size of the Gaussian kernel. Default is 5.

    Returns:
        np.array: Smoothed HSI image.
    '''
    blur_func = cv2.GaussianBlur
    smooth_hsi = integration_smooth_images_for_blur(hsi, blur_func, kernel_size)
    return smooth_hsi


def integration_smooth_images_for_blur(hsi, blur_func, kernel_size):
    band_size = hsi.shape[2]
    if band_size % 3 == 0:
        smooth_hsi = np.empty((hsi.shape[0], hsi.shape[1], 0))
    else:
        smooth_hsi = cv2.blur(hsi[:, :, 0], (kernel_size, kernel_size))
        hsi = hsi[:, :, 1:]

    for i in range(int(hsi.shape[2] / 3)):
        band = i * 3
        gizi_rgb = hsi[:,:,band:band+3]
        smooth_gizi_rgb = blur_func(gizi_rgb, (kernel_size, kernel_size))
        smooth_hsi = np.dstack([smooth_hsi, smooth_gizi_rgb])
    return smooth_hsi