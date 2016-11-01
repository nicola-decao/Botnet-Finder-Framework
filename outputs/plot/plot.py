
import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import FuncFormatter
from metrics import metrics_by_bot


class Plot:

    @staticmethod
    def plots_map():
        return {
            'total-metrics-bars': Plot.total_metrics_bar,
            'metrics-bars': Plot.metrics_bars
        }

    @staticmethod
    def all(filename, metrics, **plot_config):
        for name, par in plot_config.items():
            Plot.plots_map()[name](filename, metrics, **par)

    @staticmethod
    def __get_colours_map(n):
        color_norm = colors.Normalize(vmin=0, vmax=n)
        scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv')

        def map_index_to_rgb_color(index):
            return scalar_map.to_rgba(index)

        return map_index_to_rgb_color

    @staticmethod
    def metrics_bars(filename, metrics, bar_width=0.8, xlabels=None, ylabel=None, xlabel=None, color=None, ncol=3, **kwargs):
        del metrics['Total']
        index = np.arange(len(metrics.popitem()[1]))

        bars_width = bar_width/len(metrics)
        cls = Plot.__get_colours_map(len(metrics))

        fig = plt.figure()
        ax = fig.add_subplot(111)

        for i, bot in enumerate(sorted(metrics.keys())):
            ax.bar(index + i*bars_width + (1 - bar_width)/2, [metrics[bot][k]['mean'] for k in sorted(metrics[bot])], bars_width, color=color if color else cls(i), yerr=[metrics[bot][k]['std'] for k in sorted(metrics[bot])], error_kw={'ecolor': '0'}, label=bot)

        if ylabel:
            plt.ylabel(ylabel)

        if xlabel:
            plt.xlabel(xlabel)

        plt.xticks(index + 0.5, xlabels if xlabels else (metric for metric in sorted(metrics.popitem()[1])))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: y if y <= 1 else ''))

        handles, labels = ax.get_legend_handles_labels()
        lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=ncol, fontsize='small', frameon=False)

        fig.savefig(filename + '_metrics_bars', bbox_extra_artists=(lgd,), bbox_inches='tight', format='eps')
        plt.clf()

    @staticmethod
    def total_metrics_bar(filename, metrics, bar_width=0.5, xlabels=None, ylabel=None, xlabel=None, color='b', **kwargs):

        total_metrics = metrics['Total']

        index = np.arange(len(total_metrics))

        fig, ax = plt.subplots()

        plt.bar(index + (1 - bar_width)/2, [total_metrics[k]['mean'] for k in sorted(total_metrics)], bar_width, color=color, yerr=[total_metrics[k]['std'] for k in sorted(total_metrics)], error_kw={'ecolor': '0'})

        if ylabel:
            plt.ylabel(ylabel)

        if xlabel:
            plt.xlabel(xlabel)

        plt.xticks(index + 0.5, xlabels if xlabels else (metric for metric in sorted(total_metrics)))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: y if y <= 1 else ''))

        plt.savefig(filename + '_total_metrics_bar',  bbox_inches='tight', format='eps')
        plt.clf()
