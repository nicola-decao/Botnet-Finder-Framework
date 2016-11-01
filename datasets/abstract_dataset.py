
import abc


class AbstractDataset:

    __metaclass__ = abc.ABCMeta

    class Field:
        DateFlowStart = 0
        Duration = 1
        Protocol = 2
        SourceIPAddress = 3
        SourceIPPort = 4
        DestinationIPAddress = 5
        DestinationIPPort = 6
        Bytes = 7
        Labels = 8
