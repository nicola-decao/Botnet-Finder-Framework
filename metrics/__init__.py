
from metrics.metrics import Metrics

metrics_map = {
    'accuracy': Metrics.accuracy,
    'precision': Metrics.precision,
    'recall': Metrics.recall#,
    #'roc_auc': Metrics.roc_auc
}


def metrics_by_bot(y_tests, y_predictions, y_labels, which=None, bots=None):

    if not bots or 'all' in bots:
        bots = set([label for y_label in y_labels for label in y_label]) - set('0')

    output = {bot: {} for bot in bots}

    for bot in output:
        y_tests_bot = [[yt for yt, yl in zip(y_test, y_label) if yl == bot or yl == '0'] for y_test, y_label in zip(y_tests, y_labels)]
        y_predictions_bot = [[yp for yp, yl in zip(y_prediction, y_label) if yl == bot or yl == '0'] for y_prediction, y_label in zip(y_predictions, y_labels)]

        if not which or 'all' in which:
            which = metrics_map.keys()

        for metric in which:
            values, mean, std = metrics_map[metric](y_tests_bot, y_predictions_bot)
            output[bot][metric] = {'values': values, 'mean': mean, 'std': std}

    output['Total'] = {}
    for metric in which:
        values, mean, std = metrics_map[metric](y_tests, y_predictions)
        output['Total'][metric] = {'values': values, 'mean': mean, 'std': std}

    return output
