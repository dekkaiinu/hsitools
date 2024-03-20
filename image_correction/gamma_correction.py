import numpy as np


def gamma_correction(img: np.array, gamma: float=2.2, max_value: int=65535, base_max_value: int=255):
    
    img = img.astype(np.float32) / max_value
    img = img ** (1.0 / gamma)
    img = img * base_max_value
    # img = img * max_pixel
    if base_max_value == 255:
        img = img.astype(np.uint8)
    elif base_max_value == 65535:
        img = img.astype(np.uint16)

    return img