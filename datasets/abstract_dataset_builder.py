
import abc
import numpy as np

from util import log
from datetime import datetime
from datasets.abstract_dataset import AbstractDataset
from datasets.dataset_builder_interface import DatasetBuilderInterface


class AbstractDatasetBuilder(DatasetBuilderInterface):

    __metaclass__ = abc.ABCMeta

    def _pre_build(self, columns, **kwargs):
        return sorted(list(set(columns))), kwargs

    def _load(self, filename, columns):
        try:
            log('[START]\tread from file ' + filename)

            log('[START]\tcounting lines')

            n_lines = 0
            with open(filename, 'r') as f:
                for _ in f:
                    n_lines += 1

            log('[END]\tcounting lines')

            log('[START]\treading lines')

            i = 0
            output = []
            with open(filename, 'r') as f:
                for index, line in enumerate(f):
                    line = line.strip().split(',')

                    if AbstractDataset.Field.DateFlowStart in columns:
                        date_column = datetime.strptime(line[self.FileField.DateFlowStart], '%Y-%m-%d %H:%M:%S.%f')
                    else:
                        date_column = None

                    if AbstractDataset.Field.Duration in columns:
                        time_column = float(line[self.FileField.Duration])
                    else:
                        time_column = None

                    if AbstractDataset.Field.Protocol in columns:
                        protocol_column = line[self.FileField.Protocol]
                    else:
                        protocol_column = None

                    if AbstractDataset.Field.SourceIPAddress in columns or AbstractDataset.Field.SourceIPPort in columns:
                        splitted = line[self.FileField.SourceIPAddressPort].split(':')
                        if len(splitted) == 2:
                            source_ip, source_port = splitted
                        else:
                            source_ip, source_port = line[self.FileField.SourceIPAddressPort], '0'

                        if AbstractDataset.Field.SourceIPAddress in columns:
                            ip_source_column = source_ip
                        else:
                            ip_source_column = None

                        if AbstractDataset.Field.SourceIPPort in columns:
                            port_source_column = source_port
                        else:
                            port_source_column = None
                    else:
                        ip_source_column = None
                        port_source_column = None

                    if AbstractDataset.Field.DestinationIPAddress in columns or AbstractDataset.Field.DestinationIPPort in columns:
                        splitted = line[self.FileField.DestinationIPAddressPort].split(':')
                        if len(splitted) == 2:
                            destination_ip, destination_port = splitted
                        else:
                            destination_ip, destination_port = line[self.FileField.DestinationIPAddressPort], '0'

                        if AbstractDataset.Field.DestinationIPAddress in columns:
                            ip_destination_column = destination_ip
                        else:
                            ip_destination_column = None

                        if AbstractDataset.Field.DestinationIPPort in columns:
                            port_destination_column = destination_port
                        else:
                            port_destination_column = None
                    else:
                        ip_destination_column = None
                        port_destination_column = None

                    if AbstractDataset.Field.Bytes in columns:
                        byte_column = int(line[self.FileField.Bytes])
                    else:
                        byte_column = None

                    if AbstractDataset.Field.Labels in columns:
                        try:
                            label_column = line[self.FileField.Labels]
                        except IndexError:
                            print(line)
                    else:
                        label_column = None

                    output.append(np.array([date_column, time_column, protocol_column, ip_source_column, port_source_column, ip_destination_column, port_destination_column, byte_column, label_column])[np.array(columns)])

                    if n_lines > 100:
                        i += 1
                        if i % int(n_lines/100) == 0:
                            print('\r' + str(int(i/int(n_lines/100))) + ' %', end='')

            if n_lines > 100:
                print('\r')

            log('[END]\treading lines')

            output = np.array(output)

            log('[END]\tread from file ' + filename)

            return output
        except IOError:
            raise IOError('could not read file: ' + filename)

    @abc.abstractmethod
    def _build(self, netflow, columns, **kwargs):
        raise NotImplementedError

    def build(self, filename, **kwargs):
        columns, kwargs = self._pre_build(self.columns, **kwargs)
        netflow = self. _load(filename, columns)
        product = self._build(netflow, columns, **kwargs)

        return product

    @abc.abstractproperty
    def columns(self):
        raise NotImplementedError

    class FileField:
        DateFlowStart = 0
        Duration = 1
        Protocol = 2
        SourceIPAddressPort = 3
        DestinationIPAddressPort = 4
        Bytes = 5
        Labels = 6
