
import json

from metrics import metrics_by_bot


class Save:

    @staticmethod
    def features(filename, features, which=None, bots=None, sort_keys=False, indent=None):

        if which and 'all' not in which:
            features = {ip: {feature: features[ip][feature] for feature in which} for ip in features}

        if bots and 'all' not in bots:
            features = {ip: item for ip, item in features.items() if item['label'] in bots or item['label'] == '0'}

        with open(filename, 'w') as outs:
            outs.write(json.dumps(features, sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

    @staticmethod
    def metrics(filename, y_tests, y_predictions, y_labels, which=None, bots=None, sort_keys=False, indent=None):
        with open(filename, 'w') as outs:
            outs.write(json.dumps(metrics_by_bot(y_tests, y_predictions, y_labels, which, bots), sort_keys=sort_keys, indent=indent, separators=(',', ': ')))

    @staticmethod
    def predictions(filename_tests, filename_predictions, filename_labels, y_tests, y_predictions, y_labels, bots=None, indent=None):

        y_tests = [[float(yt) for yt, yl in zip(y_test, y_label) if not bots or 'all' in bots or yl in bots or yl == '0'] for y_test, y_label in zip(y_tests, y_labels)]
        y_predictions = [[float(yp) for yp, yl in zip(y_prediction, y_label) if not bots or 'all' in bots or yl in bots or yl == '0'] for y_prediction, y_label in zip(y_predictions, y_labels)]
        y_labels = [[yl for yl in y_label if not bots or 'all' in bots or yl in bots or yl == '0'] for y_label in y_labels]

        with open(filename_tests, 'w') as outs:
            outs.write(json.dumps(y_tests, indent=indent, separators=(',', ': ')))

        with open(filename_predictions, 'w') as outs:
            outs.write(json.dumps(y_predictions, indent=indent, separators=(',', ': ')))

        with open(filename_labels, 'w') as outs:
            outs.write(json.dumps(y_labels, indent=indent, separators=(',', ': ')))
