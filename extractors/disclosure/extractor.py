
import scipy.stats
import numpy as np

from extractors import ExtractorInterface
from util import log
from multiprocessing import Process, Queue


class DisclosureExtractor(ExtractorInterface):

    def extract(self, dataset, autocorrelation=1, unmatched=1, parallel=False):

        # creation of an easy to iterate data structure from dataset matrix
        flows_by_server = DisclosureExtractor.__extract_flows(dataset)

        if parallel:
            q = Queue()
    
            p1 = Process(target=DisclosureExtractor.__extract_statistical_features, args=(q, flows_by_server,))
            p2 = Process(target=DisclosureExtractor.__extract_autocorrelation_features, args=(q, flows_by_server, dataset, autocorrelation))
            p3 = Process(target=DisclosureExtractor.__extract_unique_flow_sizes_features, args=(q, flows_by_server,))
            p4 = Process(target=DisclosureExtractor.__regular_access_patterns_features, args=(q, flows_by_server,))
            p5 = Process(target=DisclosureExtractor.__unmatched_flow_density_features, args=(q, flows_by_server, dataset, unmatched))
    
            p1.start()
            p2.start()
            p3.start()
            p4.start()
            p5.start()
    
            p1.join()
            fg1 = q.get()
    
            p2.join()
            fg2 = q.get()
    
            p3.join()
            fg3 = q.get()
    
            p4.join()
            fg4 = q.get()
    
            p5.join()
            fg5 = q.get()
        else:
            fg1 = DisclosureExtractor.__extract_statistical_features(None, flows_by_server)
            fg2 = DisclosureExtractor.__extract_autocorrelation_features(None, flows_by_server, dataset, autocorrelation)
            fg3 = DisclosureExtractor.__extract_unique_flow_sizes_features(None, flows_by_server)
            fg4 = DisclosureExtractor.__regular_access_patterns_features(None, flows_by_server)
            fg5 = DisclosureExtractor.__unmatched_flow_density_features(None, flows_by_server, dataset, unmatched)

        features = {ip: {'label': label} for ip, label in dataset.labeled_ips.items()}

        for feat, f1, f2, f3, f4, f5 in zip(features.values(), fg1.values(), fg2.values(), fg3.values(), fg4.values(), fg5.values()):
            feat.update(f1)
            feat.update(f2)
            feat.update(f3)
            feat.update(f4)
            feat.update(f5)

        return features

    @staticmethod
    def __extract_flows(dataset):
        """This function build a data structure from the array of flows given as input.

            :return: A map with server IPs as key. The values of these maps are other maps with 2 keys: 'to' and
                'from' which divide the incoming flows ('to') from outgoing flows ('from'). The values of these
                2 maps are other maps which use destination (for outgoing flows) or source (for outgoing flows)
                IPs as keys. Finally the values of these maps are arrays of flows. A flow is represented as a 2
                values array: a size in bytes and a start date as datetime.
        """
        log('[START]\tflows extraction')

        # creation of output base structure
        output = {server_ip: {'from': {}, 'to': {}} for server_ip in dataset.labeled_ips}

        # it iterates the dataset matrix
        for current_source_ip, current_destination_ip, bytes_flow, start in zip(dataset.netflow[:, dataset.Field.SourceIPAddress], dataset.netflow[:, dataset.Field.DestinationIPAddress], dataset.netflow[:, dataset.Field.Bytes], dataset.netflow[:, dataset.Field.DateFlowStart]):

            # if source ip is a server it inserts the flow in output
            if current_source_ip in dataset.labeled_ips:
                if current_destination_ip not in output[current_source_ip]['from']:
                    output[current_source_ip]['from'][current_destination_ip] = []

                output[current_source_ip]['from'][current_destination_ip].append([bytes_flow, start])

            # if destination ip is a server it inserts the flow in output
            if current_destination_ip in dataset.labeled_ips:
                if current_source_ip not in output[current_destination_ip]['to']:
                    output[current_destination_ip]['to'][current_source_ip] = []

                output[current_destination_ip]['to'][current_source_ip].append([bytes_flow, start])

        log('[END]\tflows extraction')

        return output

    @staticmethod
    def __extract_statistical_features(q, flows_by_server):
        """This function extracts the mean and standard deviation of bytes separately
        for both incoming and outgoing flows of each server.

        In particular it adds
            mean_from := mean of incoming flows,
            mean_to := mean of outgoing flows,
            std_from := standard deviation of incoming flows,
            std_to := standard deviation of outgoing flows,
        to the features map.

            :param flows_by_server: flows of servers which the function has to extract features from
            :type flows_by_server: a map with server IPs as key. The values of these maps are other maps with 2 keys:
                'to' and 'from' which divide the incoming flows ('to') from outgoing flows ('from').
                The values of these 2 maps are other maps which use destination (for outgoing flows) or source
                (for outgoing flows) IPs as keys. Finally the values of these maps are arrays of flows.
                A flow is represented as a 2 values array: a size in bytes and a start date as datetime.
        """

        log('[START]\tstatistical features extraction')

        output = {}

        # for each server it computes the features related to it
        for server_ip, flows in flows_by_server.items():

            output[server_ip] = {}

            # flow sizes for outgoing connections extraction
            flows_from = [f[0] for client_flows in flows['from'].values() for f in client_flows]

            # mean and standard deviation extraction
            output[server_ip]['mean_from'] = np.mean(flows_from) if flows_from else 0
            output[server_ip]['std_from'] = np.std(flows_from) / output[server_ip]['mean_from'] if flows_from else 0

            # flow sizes for incoming connections extraction
            flows_to = [f[0] for client_flows in flows['to'].values() for f in client_flows]

            # mean and standard deviation extraction
            output[server_ip]['mean_to'] = np.mean(flows_to) if flows_to else 0
            output[server_ip]['std_to'] = np.std(flows_to) / output[server_ip]['mean_to'] if flows_to else 0

        log('[END]\tstatistical features extraction')
        
        if q:
            q.put(output)
        else:
            return output

    @staticmethod
    def __extract_autocorrelation_features(q, flows_by_server, dataset, autocorrelation):
        """This function extracts autocorrelation features.

        In particular it adds:
            autocorrelation_mean_from := mean of autocorrelation of incoming flows,
            autocorrelation_mean_to := mean of autocorrelation of outgoing flows,
            autocorrelation_std_from := standard deviation of autocorrelation of incoming flows,
            autocorrelation_std_to := standard deviation of autocorrelation of outgoing flows,
        to the features map.

            :param flows_by_server: flows of servers which the function has to extract features from
            :type flows_by_server: a map with server IPs as key. The values of these maps are other maps with 2 keys:
                'to' and 'from' which divide the incoming flows ('to') from outgoing flows ('from').
                The values of these 2 maps are other maps which use destination (for outgoing flows) or source
                (for outgoing flows) IPs as keys. Finally the values of these maps are arrays of flows.
                A flow is represented as a 2 values array: a size in bytes and a start date as datetime.
        """

        log('[START]\tautocorrelation features extraction')

        output = {}

        # it calculates the range of time series and the interval time
        min_date = np.amin(dataset.netflow[:, dataset.Field.DateFlowStart])
        max_date = np.amax(dataset.netflow[:, dataset.Field.DateFlowStart])
        diff = (max_date - min_date) / autocorrelation

        # for each server it computes the features related to it
        for server_ip, flows in flows_by_server.items():

            output[server_ip] = {}

            # creates time series empty base structure
            time_series = {'mean_from': np.ndarray((1, autocorrelation)), 'mean_to': np.ndarray((1, autocorrelation))}

            # initial values
            lower_bound_date = min_date
            upper_bound_date = lower_bound_date + diff

            # for each time interval
            for index in range(0, autocorrelation):
                # incoming and outgoing flow sizes in the interval extraction
                curr_from = [f[0] for flow in flows['from'].values() for f in flow if lower_bound_date <= f[1] < upper_bound_date or (upper_bound_date == max_date == f[1])]
                curr_to = [f[0] for flow in flows['to'].values() for f in flow if lower_bound_date <= f[1] < upper_bound_date or (upper_bound_date == max_date == f[1])]

                # mean of incoming and outgoing flows extraction
                time_series['mean_from'][0][index] = np.mean(curr_from) if curr_from else 0
                time_series['mean_to'][0][index] = np.mean(curr_to) if curr_to else 0

                # increments in order to shift time intervals
                lower_bound_date = upper_bound_date
                upper_bound_date = lower_bound_date + diff

            # it calculates autocorrelation normalized with standard deviation of incoming and outgoing flows
            autocorrelation_from = list(np.correlate(time_series['mean_from'][0], time_series['mean_from'][0], 'full') / np.var(time_series['mean_from'][0])) if np.var(time_series['mean_from'][0]) else []
            autocorrelation_to = list(np.correlate(time_series['mean_to'][0], time_series['mean_to'][0], 'full') / np.var(time_series['mean_to'][0])) if np.var(time_series['mean_to'][0]) else []

            # mean and standard deviation extraction
            output[server_ip]['autocorrelation_mean_from'] = np.mean(autocorrelation_from) if autocorrelation_from else 0
            output[server_ip]['autocorrelation_std_from'] = np.std(autocorrelation_from) / output[server_ip]['autocorrelation_mean_from'] if autocorrelation_from else 0
            output[server_ip]['autocorrelation_mean_to'] = np.mean(autocorrelation_to) if autocorrelation_to else 0
            output[server_ip]['autocorrelation_std_to'] = np.std(autocorrelation_to) / output[server_ip]['autocorrelation_mean_to'] if autocorrelation_to else 0

        log('[END]\tautocorrelation features extraction')

        if q:
            q.put(output)
        else:
            return output

    @staticmethod
    def __extract_unique_flow_sizes_features(q, flows_by_server):
        """This function extracts unique flow sizes features.

        Counts the number of unique flow sizes observed, and performs
        statistical measurements of occurrence density for each of them.

        In particular it adds:
            unique_flow_sizes_entropy := entropy of both incoming and outgoing flows together,
            unique_flow_sizes_entropy_from := entropy of incoming flows,
            unique_flow_sizes_entropy_to := entropy of outgoing flows,
            unique_flow_sizes_kurtosis := kurtosis of both incoming and outgoing flows together,
            unique_flow_sizes_kurtosis_from := kurtosis of incoming flows,
            unique_flow_sizes_kurtosis_to := kurtosis of outgoing flows,
        to the features map.

            :param flows_by_server: flows of servers which the function has to extract features from
            :type flows_by_server: a map with server IPs as key. The values of these maps are other maps with 2 keys:
                'to' and 'from' which divide the incoming flows ('to') from outgoing flows ('from').
                The values of these 2 maps are other maps which use destination (for outgoing flows) or source
                (for outgoing flows) IPs as keys. Finally the values of these maps are arrays of flows.
                A flow is represented as a 2 values array: a size in bytes and a start date as datetime.
        """

        log('[START]\tunique flow sizes features extraction')

        output = {}

        # for each server it computes the features related to it
        for server_ip, flows in flows_by_server.items():

            output[server_ip] = {}

            # flow sizes for both incoming and outgoing flows extraction
            flows_to = [f[0] for client_flows in flows['to'].values() for f in client_flows]
            flows_from = [f[0] for client_flows in flows['from'].values() for f in client_flows]

            # kurtosis and entropy of both incoming and outgoing flows together extraction
            if flows['to'] and flows['from']:
                output[server_ip]['unique_flow_sizes_kurtosis'], output[server_ip]['unique_flow_sizes_entropy'] = DisclosureExtractor.__extract_kurtosis_and_entropy(np.concatenate((flows_to, flows_from)))
            else:
                output[server_ip]['unique_flow_sizes_kurtosis'], output[server_ip]['unique_flow_sizes_entropy'] = 0, 0

            # kurtosis and entropy of outgoing flows extraction
            if flows['to']:
                output[server_ip]['unique_flow_sizes_kurtosis_to'], output[server_ip]['unique_flow_sizes_entropy_to'] = DisclosureExtractor.__extract_kurtosis_and_entropy(flows_to)
            else:
                output[server_ip]['unique_flow_sizes_kurtosis_to'], output[server_ip]['unique_flow_sizes_entropy_to'] = 0, 0

            # kurtosis and entropy of incoming flows extraction
            if flows['from']:
                output[server_ip]['unique_flow_sizes_kurtosis_from'], output[server_ip]['unique_flow_sizes_entropy_from'] = DisclosureExtractor.__extract_kurtosis_and_entropy(flows_from)
            else:
                output[server_ip]['unique_flow_sizes_kurtosis_from'], output[server_ip]['unique_flow_sizes_entropy_from'] = 0, 0

        log('[END]\tunique flow sizes features extraction')

        if q:
            q.put(output)
        else:
            return output

    @staticmethod
    def __extract_kurtosis_and_entropy(flow_sizes):
        """This function extracts kurtosis of given flow sizes and entropy on unique flow size.

        For kurtosis Pearson's definition is used (normal := 3.0).

            :param flow_sizes: flows of servers which the function has to extract kurtosis and entropy from
            :type flow_sizes: list of sizes in bytes.
        """

        # kurtosis (Pearson's definition is used: normal := 3.0) extraction
        kurtosis = scipy.stats.kurtosis(flow_sizes, fisher=False)

        # initial values of counters to zero
        unique_flow_sizes_counter = {flow_size: 0 for flow_size in np.unique(flow_sizes)}

        # counting the occurrences of each flow size
        for flow_size in flow_sizes:
            unique_flow_sizes_counter[flow_size] += 1

        # entropy on occurrences extraction
        entropy = scipy.stats.entropy(list(unique_flow_sizes_counter.values()))

        return kurtosis, entropy

    @staticmethod
    def __regular_access_patterns_features(q, flows_by_server):
        """This function extracts regular access patterns features.

        For each server and client it prepares a time series of flows observed during analysis period.
        Then, a sequence of flow inter-arrival times is derived from the time series by taking the
        difference between consecutive connections. Then, statistical features are computed over
        each inter-arrival sequence, including the minimum, maximum, median, and standard deviation.
        Finally, there are derived features for each server.

        In particular it adds (cap is for client access pattern):
            cap_max := mean of maximums of inter-arrival sequences of incoming flows,
            cap_median := mean of medians of inter-arrival sequences of incoming flows,
            cap_median_normalized := mean of medians (from 0 to 1) of inter-arrival sequences of incoming flows,
            cap_min := mean of minimums of inter-arrival sequences of incoming flows,
            cap_std := mean of standard deviations of inter-arrival sequences of incoming flows,
        to the features map.

            :param flows_by_server: flows of servers which the function has to extract features from
            :type flows_by_server: a map with server IPs as key. The values of these maps are other maps with 2 keys:
                'to' and 'from' which divide the incoming flows ('to') from outgoing flows ('from').
                The values of these 2 maps are other maps which use destination (for outgoing flows) or source
                (for outgoing flows) IPs as keys. Finally the values of these maps are arrays of flows.
                A flow is represented as a 2 values array: a size in bytes and a start date as datetime.
        """

        log('[START]\tregular access patterns features extraction')

        output = {}

        # for each server it computes the features related to it
        for server_ip, flows in flows_by_server.items():

            output[server_ip] = {}

            # creates time series base structure
            time_series = {'min': [], 'max': [], 'median': [], 'std': []}

            # for each incoming connection
            for client_flows in flows['to'].values():

                # start times of connections extraction
                client_flows = [f[1] for f in client_flows]
                client_flows.sort()

                # creation a copy of start times in order to compute the difference efficiently
                client_flows_shift = list(client_flows)
                client_flows_shift.pop(0)

                # it computes the difference between two consecutive connections and converts it in milliseconds
                client_flows_diff = [flow_shift - flow for flow, flow_shift in zip(client_flows, client_flows_shift)]
                # client_flows_diff = [client_flows_shift[i] - client_flows[i] for i in range(0, len(client_flows_shift))]
                client_flows_diff = [time_diff.microseconds/1000 + time_diff.seconds*1000 + time_diff.days*24*60*60*1000 for time_diff in client_flows_diff]

                # minimum, maximum, median, and standard deviation extraction
                if client_flows_diff:
                    time_series['min'].append(np.amin(client_flows_diff))
                    time_series['max'].append(np.amax(client_flows_diff))
                    time_series['median'].append(np.median(client_flows_diff))
                    time_series['mean'] = np.mean(client_flows_diff)
                    time_series['std'].append(np.std(client_flows_diff) / time_series['mean'] if time_series['mean'] else 0)

            # statistical features of the server extraction
            output[server_ip]['cap_min'] = np.mean(time_series['min']) if time_series['min'] else 0
            output[server_ip]['cap_max'] = np.mean(time_series['max']) if time_series['max'] else 0
            output[server_ip]['cap_median'] = np.mean(time_series['median']) if time_series['median'] else 0
            output[server_ip]['cap_median_normalized'] = (output[server_ip]['cap_median'] - output[server_ip]['cap_min']) / (output[server_ip]['cap_max'] - output[server_ip]['cap_min']) if output[server_ip]['cap_min'] != output[server_ip]['cap_max'] else 0.5
            output[server_ip]['cap_std'] = np.mean(time_series['std']) if time_series['std'] else 0

        log('[END]\tregular access patterns features extraction')

        if q:
            q.put(output)
        else:
            return output

    @staticmethod
    def __unmatched_flow_density_features(q, flows_by_server, dataset, unmatched):
        """This function extracts unmatched flow density features.

            Extracts statistics regarding the number of unmatched incoming and outgoing flows.

        In particular it adds:
            unmatched_flows_mean := mean of unmatched flows,
            unmatched_flows_std := standard deviation of unmatched flows,
        to the features map.

            :param flows_by_server: flows of servers which the function has to extract features from
            :type flows_by_server: a map with server IPs as key. The values of these maps are other maps with 2 keys:
                'to' and 'from' which divide the incoming flows ('to') from outgoing flows ('from').
                The values of these 2 maps are other maps which use destination (for outgoing flows) or source
                (for outgoing flows) IPs as keys. Finally the values of these maps are arrays of flows.
                A flow is represented as a 2 values array: a size in bytes and a start date as datetime.
        """

        log('[START]\tunmatched flow density features extraction')

        output = {}

        # it calculates the range of time series and the interval time
        min_date = np.amin(dataset.netflow[:, dataset.Field.DateFlowStart])
        max_date = np.amax(dataset.netflow[:, dataset.Field.DateFlowStart])
        diff = (max_date - min_date) / unmatched

        # for each server it computes the features related to it
        for server_ip, flows in flows_by_server.items():

            output[server_ip] = {}

            # initial values
            unmatched_flows = []
            lower_bound_date = min_date
            upper_bound_date = lower_bound_date + diff

            # for each time interval
            for index in range(0, unmatched):
                # initial partial sum
                p_sum = 0

                # for each client which has at least one flow with the server
                for client_ip in list(set(flows['to'].keys()) | set(flows['from'].keys())):

                    # incoming and outgoing flows extraction
                    flow_to = flows['to'][client_ip] if client_ip in flows['to'] else []
                    flow_from = flows['from'][client_ip] if client_ip in flows['from'] else []

                    # incoming and outgoing flows into the time interval counting
                    flow_to = sum(lower_bound_date <= flow[1] < upper_bound_date or (upper_bound_date == max_date == flow[1]) for flow in flow_to) if flow_to else 0
                    flow_from = sum(lower_bound_date <= flow[1] < upper_bound_date or (upper_bound_date == max_date == flow[1]) for flow in flow_from) if flow_from else 0

                    # it updates partial sum
                    p_sum += abs(flow_to - flow_from)

                # it increments in order to shift time intervals
                lower_bound_date = upper_bound_date
                upper_bound_date = lower_bound_date + diff

                unmatched_flows.append(p_sum)

            # mean and standard deviation over the time series extraction
            output[server_ip]['unmatched_flows_mean'] = np.mean(unmatched_flows) if unmatched_flows else 0
            output[server_ip]['unmatched_flows_std'] = np.std(unmatched_flows) / output[server_ip]['unmatched_flows_mean'] if output[server_ip]['unmatched_flows_mean'] else 0

        log('[END]\tunmatched flow density features extraction')

        if q:
            q.put(output)
        else:
            return output
