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


def hsi_gaussian_blur(hsi: np.array, kernel_size: int=5, sigmaX: float=1):
    '''
    Apply Gaussian blurring to an HSI image.

    Parameters:
        hsi (np.array): Input HSI image.
        kernel_size (int): Size of the Gaussian kernel. Default is 5.
        sigmaX (float): Standard deviation of the Gaussian kernel in the horizontal direction.
            A larger value results in more smoothing. If 0, it is calculated from the kernel size.

    Returns:
        np.array: Smoothed HSI image.
    '''
    blur_func = cv2.GaussianBlur
    smooth_hsi = integration_smooth_images_for_blur(hsi, blur_func, kernel_size, sigmaX)
    return smooth_hsi


def integration_smooth_images_for_blur(hsi, blur_func, kernel_size, sigmaX=None):
    band_size = hsi.shape[2]
    if band_size % 3 == 0:
        smooth_hsi = np.empty((hsi.shape[0], hsi.shape[1], 0))
    elif band_size % 3 == 1:
        if sigmaX:
            smooth_hsi = blur_func(hsi[:, :, 0], (kernel_size, kernel_size), sigmaX)
        else:
            smooth_hsi = blur_func(hsi[:, :, 0], (kernel_size, kernel_size))
        hsi = hsi[:, :, 1:]
    else:
        if sigmaX:
            smooth_hsi = blur_func(hsi[:, :, 0], (kernel_size, kernel_size), sigmaX)
            smooth_hsi = np.dstack([smooth_hsi, blur_func(hsi[:, :, 1], (kernel_size, kernel_size), sigmaX)])
        else:
            smooth_hsi = blur_func(hsi[:, :, 0], (kernel_size, kernel_size))
            smooth_hsi = np.dstack([smooth_hsi, blur_func(hsi[:, :, 1], (kernel_size, kernel_size))])
        hsi = hsi[:, :, 2:]


    for i in range(int(hsi.shape[2] / 3)):
        band = i * 3
        gizi_rgb = hsi[:,:,band:band+3]
        if sigmaX:
            smooth_gizi_rgb = blur_func(gizi_rgb, (kernel_size, kernel_size), sigmaX)
        else:
            smooth_gizi_rgb = blur_func(gizi_rgb, (kernel_size, kernel_size))
        smooth_hsi = np.dstack([smooth_hsi, smooth_gizi_rgb])
        
    return smooth_hsi