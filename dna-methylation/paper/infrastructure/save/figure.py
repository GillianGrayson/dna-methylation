import plotly
from plotly import io as pio


def save_figure(fn, fig):
    plotly.offline.plot(fig, filename=fn + '.html', auto_open=False, show_link=True)
    pio.write_image(fig, fn + '.png')
    pio.write_image(fig, fn + '.pdf')