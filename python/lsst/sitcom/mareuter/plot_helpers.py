import gc

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

__all__ = ["remove_figure"]


def remove_figure(fig: Figure) -> None:
    """
    Remove a figure to reduce memory footprint.

    Taken from the DP0.2 notebook series

    Parameters
    ----------
    fig: matplotlib.figure.Figure
        Figure to be removed.

    Returns
    -------
    None
    """
    # get the axes and clear their images
    for ax in fig.get_axes():
        for im in ax.get_images():
            im.remove()
    fig.clf()  # clear the figure
    plt.close(fig)  # close the figure
    gc.collect()  # call the garbage collector
