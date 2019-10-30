def align_legend(legend):
    """
    Aligns text in a legend

    Parameters
    ----------
    legend : matplotlib.legend.Legend
    """
    renderer = legend.get_figure().canvas.get_renderer()
    shift = max([t.get_window_extent(renderer).width for t in legend.get_texts()])
    for t in legend.get_texts():
        t.set_ha('right') # ha is alias for horizontalalignment
        t.set_position((shift,0))