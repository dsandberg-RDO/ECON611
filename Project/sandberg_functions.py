
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def format_axis_ticklabel(axis, format_, maxn=None): # format y-axis tick labels formats
    # axis: 0 = xaxis; 1=yaxis
    # format: p0 = percent as integer; p1 = percent as decimal; c = currency, t = comma
    ax = plt.gca()

    if format_ == 'p0':
        label_format = '{:.0%}'
    elif format_ == 'p1':
        label_format = '{:.1%}'
    elif format == 'c':
        label_format = '${:,.0f}'
    elif format == 't':
        label_format = '{:,.0f}'

    if axis == 0:
        if ~ maxn == None:
            ax.xaxis.set_major_locator(mtick.MaxNLocator(maxn))
        ticks_loc = ax.get_xticks().tolist()
        ax.xaxis.set_major_locator(mtick.FixedLocator(ticks_loc))
        ax.set_xticklabels([label_format.format(x) for x in ticks_loc])
    else:
        if ~ maxn == None:
            ax.yaxis.set_major_locator(mtick.MaxNLocator(maxn))
        ticks_loc = ax.get_yticks().tolist()
        ax.yaxis.set_major_locator(mtick.FixedLocator(ticks_loc))
        ax.set_yticklabels([label_format.format(y) for y in ticks_loc])
    return ax


