from .DataLoader import ShootingsDataLoader
from . import Statistics as ShootingStats
from src.Cenus2019 import Census2019
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral5


def plot_shootings(df, total=False):
    race_names = ShootingsDataLoader.RACE_FULL_NAMES
    counts, fraction, pop_fraction, per_million = ShootingStats.total_shootings(df)
    counts = list(counts.values())
    per_million = list(per_million.values())

    # The default Spectral5 has a bright red that doesn't seem to fit & draws too much attention
    color_palette = list(Spectral5)[:-1]
    color_palette.extend(['#ff8d64'])

    if total:
        source = ColumnDataSource(data=dict(race=race_names, counts=counts))
        title = 'Fatal Shootings by Race (total)'
        range_end = int(max(counts) * 1.15)
    else:
        source = ColumnDataSource(data=dict(race=race_names, counts=per_million))
        title = 'Fatal Shootings by Race (per million)'
        range_end = int(max(per_million) * 1.15)

    p = figure(title=title, x_range=race_names, toolbar_location=None)
    p.vbar(x='race', top='counts', source=source, legend_field='race',
           fill_color=factor_cmap('race', palette=color_palette, factors=race_names))
    p.legend.orientation = 'horizontal'
    p.legend.location = 'top_center'
    p.y_range.end = range_end

    show(p)
