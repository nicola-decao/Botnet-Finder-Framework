
import networkx

from extractors import ExtractorInterface


class BotTrackExtractor(ExtractorInterface):

    def extract(self, dataset, hits_max_iter=100):

        graph = networkx.DiGraph()

        n_lines = dataset.netflow.shape[0]
        i = 0

        for current_source_ip, current_destination_ip in zip(dataset.netflow[:, dataset.Field.SourceIPAddress], dataset.netflow[:, dataset.Field.DestinationIPAddress]):
            graph.add_node(current_source_ip)
            graph.add_node(current_destination_ip)
            graph.add_edge(current_source_ip, current_destination_ip)

            if n_lines > 100:
                i += 1
                if i % int(n_lines/100) == 0:
                    print('\r' + str(int(i/int(n_lines/100))) + ' %', end='')

        if n_lines > 100:
            print('\r')

        (hubs, authorities) = networkx.hits(graph, max_iter=hits_max_iter, tol=1e-06)
        features = {ip: {'label': dataset.labeled_ips[ip], 'authority': authorities[ip], 'hub': hubs[ip]} for ip in graph.nodes()}

        return features
