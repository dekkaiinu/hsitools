import numpy as np

def min_max(X: np.array, X_train: np.array=None):
    '''
    Normalize the input hyperspectral pixels using min-max scaling.

    Parameters:
        X (np.array): Input array of hyperspectral pixels to be normalized.
        X_train (np.array, optional): If provided, the minimum and maximum values will be computed based on this array. Default is None.

    Returns:
        np.array: Normalized array.
    '''
    if X_train is not None:
        min_vals = np.min(X_train)
        max_vals = np.max(X_train)
    else:
        min_vals = np.min(X)
        max_vals = np.max(X)
    X = (X - min_vals) / (max_vals - min_vals)
    return X

def band_wise_min_max(X: np.array, X_train: np.array=None):
    '''
    Normalize the input hyperspectral pixels band-wise using min-max scaling.

    Parameters:
        X (np.array): Input array of hyperspectral pixels to be normalized.
        X_train (np.array, optional): If provided, the minimum and maximum values for each band will be computed based on this array. Default is None.

    Returns:
        np.array: Normalized array.
    '''
    if X_train is not None:
        min_vals = np.min(X_train, axis=0)
        max_vals = np.max(X_train, axis=0)
    else:
        min_vals = np.min(X, axis=0)
        max_vals = np.max(X, axis=0)
    X = (X - min_vals) / (max_vals - min_vals)
    return X

def std(X: np.array, X_train: np.array=None):
    '''
    Standardize the input hyperspectral pixels by subtracting the mean and dividing by the standard deviation.

    Parameters:
        X (np.array): Input array of hyperspectral pixels to be standardized.
        X_train (np.array, optional): If provided, the mean and standard deviation will be computed based on this array. Default is None.

    Returns:
        np.array: Standardized array.
    '''
    if X_train is not None:
        mean_vals = np.mean(X_train)
        std_vals = np.std(X_train)
    else:
        mean_vals = np.mean(X)
        std_vals = np.std(X)
    X = (X - mean_vals) / std_vals
    return X

def band_wise_std(X: np.array, X_train: np.array=None):
    '''
    Standardize the input hyperspectral pixels band-wise by subtracting the mean and dividing by the standard deviation of each band.

    Parameters:
        X (np.array): Input array of hyperspectral pixels to be standardized.
        X_train (np.array, optional): If provided, the mean and standard deviation for each band will be computed based on this array. Default is None.

    Returns:
        np.array: Standardized array.
    '''
    if X_train is not None:
        mean_vals = np.mean(X_train, axis=0)
        std_vals = np.std(X_train, axis=0)
    else:
        mean_vals = np.mean(X, axis=0)
        std_vals = np.std(X, axis=0)
    X = (X - mean_vals) / std_vals

def instance_norm(X: np.array):
    '''
    Normalize the input hyperspectral pixels instance-wise using instance normalization.

    Parameters:
        X (np.array): Input array of hyperspectral pixels to be normalized.

    Returns:
        np.array: Normalized array.
    '''
    mean_vals = np.mean(X, axis=1, keepdims=True)
    std_vals = np.std(X, axis=1, keepdims=True)
    X_norm = (X - mean_vals) / std_vals
    return X_norm

def instance_norm_min_max(X: np.array):
    '''
    Normalize the input hyperspectral pixels instance-wise using min-max scaling.

    Parameters:
        X (np.array): Input array of hyperspectral pixels to be normalized.

    Returns:
        np.array: Normalized array.
    '''
    min_vals = np.min(X, axis=1, keepdims=True)
    max_vals = np.max(X, axis=1, keepdims=True)
    X_norm = (X - min_vals) / (max_vals - min_vals)
    return X_norm

def zero_wavelength(X: np.array, chosen_band: int=60):
    '''
    Apply zero-wavelength correction to the input hyperspectral pixels.

    Parameters:
        X (np.array): Input array of hyperspectral pixels to be corrected.
        chosen_band (int, optional): Index of the band to be set to zero wavelength. Default is 60.

    Returns:
        np.array: Corrected array.
    '''
    chosen_X = X[: , chosen_band]
    exted_chosen_X = np.repeat(chosen_X[:, np.newaxis], 151, axis=1)
    
    X_norm = X - exted_chosen_X
    return X_norm

def residual_img(X: np.array, chosen_band: int=60):
    '''
    Apply residual image correction to the input hyperspectral pixels.

    This correction scales each spectrum by a constant such that the intensity of a selected band matches the maximum intensity across the entire scene. Then, the average intensity in each band over the entire scene is subtracted from the intensity in each channel.

    Parameters:
        X (np.array): Input array of hyperspectral pixels to be corrected.
        chosen_band (int, optional): Index of the band used for scaling. Default is 60.

    Returns:
        np.array: Corrected array.
    '''
    chosen_X = X[: , chosen_band]
    max_value = np.max(chosen_X)

    band_X = X[:, chosen_band]
    residual_band_X = max_value - band_X
    residual_X = X + np.repeat(residual_band_X[:, np.newaxis], 151, axis=1)

    channel_mean = np.mean(residual_X, axis=0)
    X_norm = residual_X - channel_mean
    return X_norm

def iarr(X: np.array, X_train: np.array):
    '''
    Apply Internal Average Relative reflectance (IARR) correction to the input hyperspectral pixels.

    This correction divides each spectrum by the average spectrum over the entire scene.

    Parameters:
        X (np.array): Input array of hyperspectral pixels to be corrected.
        X_train (np.array): Array of hyperspectral pixels representing the average spectrum over the entire scene.

    Returns:
        np.array: Corrected array.
    '''
    return X / np.mean(X_train)

def first_derivative(X: np.array):
    '''
    Calculate the first derivative of the input hyperspectral pixels.

    This correction computes the first derivative of each spectrum by taking the difference between consecutive spectral values.

    Parameters:
        X (np.array): Input array of hyperspectral pixels.

    Returns:
        np.array: Array containing the first derivative of each spectrum.
    '''
    X = X.astype(np.int32)
    X_first_derivative = []
    for index in range(X.shape[0]):
        x = X[index]
        x = x / 4096
        x_first_derivative = x[1:] - x[:len(x) - 1]
        X_first_derivative.append(x_first_derivative)
    X_first_derivative = np.array(X_first_derivative)
    return X_first_derivative

def second_derivative(X: np.array):
    '''
    Calculate the second derivative of the input hyperspectral pixels.

    This correction computes the second derivative of each spectrum by taking the difference between consecutive first derivative values.

    Parameters:
        X (np.array): Input array of hyperspectral pixels.

    Returns:
        np.array: Array containing the second derivative of each spectrum.
    '''
    X = X.astype(np.int32)
    X_second_derivative = []
    for index in range(X.shape[0]):
        x = X[index]
        x = x / 4096
        x_first_derivative = x[1:] - x[:len(x) - 1]
        x_second_derivative = x_first_derivative[1:] - x_first_derivative[:len(x_first_derivative) - 1]
        X_second_derivative.append(x_second_derivative)
    X_second_derivative = np.array(X_second_derivative)
    return X_second_derivative