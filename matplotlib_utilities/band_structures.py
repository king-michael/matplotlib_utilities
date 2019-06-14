from .utils import sliding_window
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv, hex2color


def plot_band_sliding_mean(ax, x, y, window, kwargs_mean={}, kwargs_band={'alpha': .5}, axis=-1):
    r"""
    Function to plot a band around the structure.
    Uses a running average for the plot and a running standard deviation for the band.

    Parameters
    ----------
    ax : ~.axes.Axes
        Matplotlib axes
    x : np.ndarray
        x values.
    y : np.ndarray
        y values.
    window : int
        Window size for the running average.
    kwargs_mean : dict, optional
        kwargs passed to the line plot for the mean
    kwargs_band : dict, optional
        kwargs passed to the band plot for the std
    axis : int or tuple, optional
        Axis on which the mean is applied.
        The axis of the sliding window is `-1`. Default is `-1`.

    Returns
    -------
    plt_mean :
        handles for the mean
    plt_band :
        handles for the band

    Examples
    --------

    set up some test data
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> x = np.linspace(0, 2*np.pi, 1000)
    >>> y = np.sin(x) + (np.random.random(x.size)-0.5)

    plot band structures
    >>> fig, ax = plt.subplots()
    >>> plot_band_sliding_mean(ax, x, y, window=10)


    plot band structures with gray band
    >>> fig, ax = plt.subplots()
    >>> plot_band_sliding_mean(ax, x, y, window=10, kwargs_band={'color' : 'gray'})


    plot band structure of multiple runs for only the **mean** on `axis = 0`
    >>> y_multiple = [np.sin(x) + (np.random.random(x.size)-0.5) for i in range(5)] # create data
    >>> plot_band_sliding_mean(ax, x, y_multiple, window=1, axis=0)

    plot band structure of multiple runs for the running mean over `axis = 0`
    >>> y_multiple = [np.sin(x) + (np.random.random(x.size)-0.5) for i in range(5)] # create data
    >>> plot_band_sliding_mean(ax, x, y_multiple, window=10, axis=(0, -1))

    """

    if window == 1:
        y_mean = y.mean(axis)
        y_std = y.std(axis)
        x_slice = slice(None, None)
    else:
        y_mean = sliding_window(y, window, copy=False).mean(axis)
        y_std = sliding_window(y, window, copy=False).std(axis)
        x_slice = slice(window // 2 - 1, -window // 2)

    color = kwargs_mean.pop('color', ax._get_lines.get_next_color())
    color_faded = hsv_to_rgb(rgb_to_hsv(hex2color(color)) * (1, 0.5, 1))
    kwargs_mean_defaults = {'color': color}
    kwargs_mean_defaults.update(kwargs_mean)
    kwargs_band_defaults = {'alpha': 0.5, 'color': color_faded}
    kwargs_band_defaults.update(kwargs_band)

    plt_band = ax.fill_between(x[x_slice], y_mean - y_std, y_mean + y_std, **kwargs_band_defaults)
    plt_mean = ax.plot(x[x_slice], y_mean, **kwargs_mean_defaults)

    return plt_mean, plt_band