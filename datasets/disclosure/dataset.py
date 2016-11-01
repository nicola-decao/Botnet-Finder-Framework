
import numpy as np
import operator
import math

from util import log
from datasets.ip_labeled_dataset import IpLabeledDataset


class DisclosureDataset(IpLabeledDataset):

    def _extract_ips(self, netflow, labels, sigma=0.2, threshold=0, part=None):
        log('[START]\tapplying heuristic to detect servers')

        ip_list = {}
        for row in self.netflow:
            if row[self.Field.DestinationIPAddress] not in ip_list:
                ip_list[row[self.Field.DestinationIPAddress]] = 0

            ip_list[row[self.Field.DestinationIPAddress]] += 1

        ip_list = {k: ip_list[k] for k in ip_list.keys() if ip_list[k] >= threshold}
        
        a = np.array(sorted(ip_list.items(), key=operator.itemgetter(1)))
        std = np.std(np.array(a[:, 1], dtype=int))

        servers = {row[0] for row in a if int(a[0, 1]) + sigma * std <= int(row[1])}

        if part:
            current, total = part
            n = math.ceil(float(len(servers)) / total)
            servers = {s for i, s in enumerate(servers) if current * n <= i < n + current * n}

        log('[END]\tapplying heuristic to detect servers')

        return servers

    class Field:
        DateFlowStart = 0
        Duration = 1
        SourceIPAddress = 2
        SourceIPPort = 3
        DestinationIPAddress = 4
        DestinationIPPort = 5
        Bytes = 6
        Labels = 7
