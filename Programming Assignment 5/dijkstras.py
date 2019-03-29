import sys
from heapq import heappush, heappop


class Graph():
    def __init__(self):
        # graph structure is {
        #    Node:
        #        incoming: [(length, source), ...]
        #        outgoing: [(length, target), ...]
        #        greedy_score: 1000000
        # }
        self.graph = {}

        self.nodes_captured = None  # keep track of nodes already seen (in X)
        self.target_nodes = None  # keep track of nodes accessible from X

    def _add_new_node(self, node, incoming, outgoing, greedy_score=1000000):
        self.graph[node] = {
            'incoming': incoming,
            'outgoing': outgoing,
            'greedy_score': greedy_score
        }
    def add_node(self, line):
        '''parse line from input and insert node information into graph'''
        line = line.split('\t')
        source = int(line[0])

        for pair_string in line[1:-1]:
            target, length = [int(val) for val in pair_string.split(',')]

            if source in self.graph:
                self.graph[source]['outgoing'].append((length, target))
            else:
                self._add_new_node(source, [], [(length, target)])

            if target in self.graph:
                self.graph[target]['incoming'].append((length, source))
            else:
                self._add_new_node(target, [(length, target)], [])

        # print(self.graph)

    def build_graph(self, f):
        '''parse file and add nodes to graph'''
        for line in f.readlines():
            self.add_node(line)

    def _further_frontier(self):
        '''move the frontier one node further'''
        next_target = self._get_next_target()
        if not next_target: return None
        self._migrate_node(next_target)

    def _get_next_target(self):
        '''figure out which node to migrate next'''
        score, next_target = heappop(self.target_nodes)

        while next_target in self.nodes_captured:
            if self.target_nodes:
                score, next_target = heappop(self.target_nodes)
            else:
                return None

        return next_target

    def _migrate_node(self, node):
        '''migrate input node and clean up graph to
        maintain dijkstras invariants
        '''
        # bookkeeping for node migration
        self.nodes_captured.add(node)
        self.nodes_to_find.discard(node)
        node_greedy_score = self.graph[node]['greedy_score']

        # graph cleanup after node migration.
        for length, target in self.graph[node]['outgoing']:
            if target not in self.nodes_captured:
                self.graph[target]['greedy_score'] = min(
                    self.graph[target]['greedy_score'],
                    node_greedy_score + length
                )

                heappush(
                    self.target_nodes,
                    (self.graph[target]['greedy_score'], target)
                )

    def search_until_satisfied(self, source, nodes_to_find):
        '''Expand graph frontier until all nodes of interest are found
        or the entire graph connected to the source input is exhausted
        '''
        self.nodes_to_find = set(nodes_to_find)
        self.graph[source]['greedy_score'] = 0
        self.nodes_captured = set()
        self.target_nodes = []

        self._migrate_node(source)

        while self.target_nodes and self.nodes_to_find:
            self._further_frontier()

        print('frontier exhausted or all nodes found')
        print('Target nodes not found:')
        if self.nodes_to_find:
            for node in self.nodes_to_find:
                print(node)
        else:
            print('None')

        print('Nodes found:')
        for node in nodes_to_find:
            print('{}:\t{}'.format(node, self.graph[node]['greedy_score']))


if __name__ == '__main__':
    g = Graph()

    filename = sys.argv[1]

    with open(filename) as f:
        g.build_graph(f)

    g.search_until_satisfied(1, [7, 37, 59, 82, 99, 115, 133, 165, 188, 197])
