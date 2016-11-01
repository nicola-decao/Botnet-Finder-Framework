
import argparse
import json

from algorithms import Algorithm
from datasets import DatasetBuilder
from extractors import Extractor
from outputs import Save, Plot


class App:

    @staticmethod
    def __parse():
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        parser.add_argument('-s', '--save', dest='save_configuration', metavar='configuration', help='JSON where are specified saving options')

        parser_extract = subparsers.add_parser('extract', help='performs features extraction')
        parser_extract.set_defaults(action='extract')
        parser_extract.add_argument('dataset_filename_in', metavar='dataset', help='netflow dataset')
        parser_extract.add_argument('features_filename_out', metavar='features', help='where save features in')
        parser_extract.add_argument('extractor', help='name of the extractor')
        parser_extract.add_argument('-c', '--configuration', dest='extractor_configuration', metavar='configuration', help='JSON where are specified extractor options')
        parser_extract.add_argument('-b', '--builder', dest='builder_configuration', metavar='configuration', help='JSON where are specified dataset builder options')

        parser_predict = subparsers.add_parser('predict', help='predictutes the algorithm and generates predictions')
        parser_predict.set_defaults(action='predict')
        parser_predict.add_argument('features_filename_in', metavar='features', help='JSON with features')
        parser_predict.add_argument('y_tests_filename',metavar='tests', help='where save test labels in')
        parser_predict.add_argument('y_predictions_filename',metavar='predictions', help='where save prediction labels in')
        parser_predict.add_argument('y_labels_filename', metavar='labels', help='where save name of botnets as labels in')
        parser_predict.add_argument('algorithm', help='name of the algorithm')
        g_predictute_mode = parser_predict.add_mutually_exclusive_group(required=True)
        g_predictute_mode.add_argument('-e', '--evaluation', dest='evaluation_filename_in', metavar='evaluation', help='JSON with features of the evaluation dataset')
        g_predictute_mode.add_argument('-k', '--kfold', type=int, metavar='folds', help='number of folds to perform in a stratified k fold validation')
        parser_predict.add_argument('-c', '--configuration', dest='algorithm_configuration', metavar='configuration', help='JSON where are specified algorithm options')

        parser_eval = subparsers.add_parser('eval', help='performs evaluation on generated predictions')
        parser_eval.set_defaults(action='eval')
        parser_eval.add_argument('y_tests_filename',metavar='tests', help='JSON with test labels')
        parser_eval.add_argument('y_predictions_filename',metavar='predictions', help='JSON with prediction labels')
        parser_eval.add_argument('y_labels_filename',metavar='labels', help='JSON with name of botnets as labels')
        parser_eval.add_argument('metrics_filename_out',metavar='metrics', help='where save metrics in')

        parser_plot = subparsers.add_parser('plot', help='generates graphs on generated metrics')
        parser_plot.set_defaults(action='plot')
        parser_plot.add_argument('metrics_filename_in',metavar='metrics', help='JSON with stored metrics in')
        parser_plot.add_argument('plot_filename_out', metavar='filename')
        parser_plot.add_argument('-c', '--configuration', dest='plot_configuration')

        return parser.parse_args()

    def main(self):
        args = self.__parse()

        with open(args.save_configuration if args.save_configuration else self.__app_dir + '/outputs/save/config.json') as f:
            save_config = json.load(f)

        if args.action == 'extract':

            with open(args.builder_configuration if args.builder_configuration else self.__app_dir + '/datasets/' + args.extractor + '/config.json') as f:
                dataset_builder_config = json.load(f)

            dataset = DatasetBuilder(args.extractor).build(args.dataset_filename_in, **dataset_builder_config)

            with open(args.extractor_configuration if args.extractor_configuration else self.__app_dir + '/extractors/' + args.extractor + '/config.json') as f:
                extractor_config = json.load(f)

            features = Extractor(args.extractor).extract(dataset, **extractor_config)

            Save.features(args.features_filename_out, features, **save_config['extract'] if 'extract' in save_config else {})

        elif args.action == 'predict':

            with open(args.features_filename_in) as f:
                features = json.load(f)

            with open(args.algorithm_configuration if args.algorithm_configuration else self.__app_dir + '/algorithms/' + args.algorithm + '/config.json') as f:
                algorithm_config = json.load(f)

            algorithm = Algorithm(args.algorithm, features=features, **algorithm_config)

            if args.kfold:
                y_tests, y_predictions, y_labels = algorithm.stratified_k_fold(folds=args.kfold)
            else:
                raise RuntimeError

            Save.predictions(args.y_tests_filename, args.y_predictions_filename, args.y_labels_filename, y_tests, y_predictions, y_labels, **save_config['predict'] if 'predict' in save_config else {})

        elif args.action == 'eval':

            with open(args.y_tests_filename) as f:
                y_tests = json.load(f)

            with open(args.y_predictions_filename) as f:
                y_predictions = json.load(f)

            with open(args.y_labels_filename) as f:
                y_labels = json.load(f)

            Save.metrics(args.metrics_filename_out, y_tests, y_predictions, y_labels, **save_config['eval'] if 'eval' in save_config else {})

        elif args.action == 'plot':

            with open(args.metrics_filename_in) as f:
                metrics = json.load(f)

            with open(args.plot_configuration if args.plot_configuration else self.__app_dir + '/outputs/plot/config.json') as f:
                plot_config = json.load(f)

            Plot.all(args.plot_filename_out, metrics, **plot_config)

    def __init__(self, app_dir):
        self.__app_dir = app_dir
