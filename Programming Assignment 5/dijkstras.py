import sys
from heapq import heappush, heappop, heapify, heapreplace


class graph():
    def __init__(self):
        # graph structure is {targetNode: [(sourceNodeA, lenA), (sourceNodeB, lenB), ...], ...}
        self.graph = {}

        self.nodes_captured = None
        self.target_nodes = None


    def add_node(self, line):
        line = line.split('\t')
        source = int(line[0])

        for pair_string in line[1:-1]:
            target, length = [int(val) for val in pair_string.split(',')]

            if source in self.graph:
                self.graph[source]['outgoing'].append((length, target))
            else:
                self.graph[source] = {'outgoing': [(length, target)], 'incoming': [], 'greedy_score': 1000000}

            if target in self.graph:
                self.graph[target]['incoming'].append((length, source))
            else:
                self.graph[target] = {'outgoing': [], 'incoming': [(length, source)], 'greedy_score': 1000000}

        # print(self.graph)

    def build_graph(self, f):
        for line in f.readlines():
            self.add_node(line)

    def _further_frontier(self):
        next_target = self._get_next_target()
        if not next_target: return None
        self._migrate_node(next_target)

    def _get_next_target(self):
        score, next_target = heappop(self.target_nodes)

        while next_target in self.nodes_captured:
            if self.target_nodes:
                score, next_target = heappop(self.target_nodes)
            else:
                return None

        return next_target

    def _migrate_node(self, node):
        self.nodes_captured.add(node)
        self.nodes_to_find.discard(node)

        node_greedy_score = self.graph[node]['greedy_score']

        for length, target in self.graph[node]['outgoing']:
            if target not in self.nodes_captured:
                self.graph[target]['greedy_score'] = min(self.graph[target]['greedy_score'], node_greedy_score + length)
                heappush(self.target_nodes, (self.graph[target]['greedy_score'], target))

    def search_until_satisfied(self, source, nodes_to_find):
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
    g = graph()

    filename = sys.argv[1]

    with open(filename) as f:
        g.build_graph(f)

    g.search_until_satisfied(1, [7, 37, 59, 82, 99, 115, 133, 165, 188, 197])
