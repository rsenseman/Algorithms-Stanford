import sys
from random import sample


class dfs_loop():
    def __init__(self, graph, search_order=None):
        self.depth = 0
        self.graph = graph
        self.t = 0  # first pass only
        self.s = None  # second pass only
        self.search_order = search_order if search_order else sample(list(range(1, len(graph) + 1)), len(graph))  # nodes ordered 1 to n
        # self.search_order = search_order if search_order else list(range(1, len(graph) + 1))  # nodes ordered 1 to n
        # print(f'search order: {self.search_order}')
        self.nodes_explored = set()

        self.leaders = [None] * (len(graph) + 1)
        self.nodes_by_finishing_time = []

        self.loop()

    def loop(self):
        while self.search_order:
            node = self.search_order.pop()
            if node not in self.nodes_explored:
                self.s = node
                self.dfs(node)

    def dfs(self, node):
        self.nodes_explored.add(node)
        self.leaders[node] = self.s

        # print(self.depth)
        for arc in self.graph[node]:
            if arc not in self.nodes_explored:
                self.depth += 1
                self.dfs(arc)
                self.depth -= 1
        self.t += 1
        self.nodes_by_finishing_time.append(node)


class graph():
    def __init__(self, pair_list):
        self.graph = {}
        self.graph_reverse = {}

        self._build_graph(pair_list)


    def _build_graph(self, pair_list):
        for x, y in pair_list:
            if x in self.graph:
                self.graph[x]['outgoing'].append(y)
            else:
                self.graph[x] = {'outgoing':[y], 'incoming':[]}

            if y in self.graph:
                self.graph[y]['incoming'].append(x)
            else:
                self.graph[y] = {'outgoing':[], 'incoming':[x]}
        print(self.graph[1])

    def find_strongly_connected_components(self):
        print('starting first loop...')
        print(f'{max(self.graph)} elements')
        first_loop = dfs_loop({k:self.graph[k]['incoming'] for k in self.graph.keys()})
        # print(f'finishing order: {first_loop.nodes_by_finishing_time}')
        # print(f'First Loop Leaders: {first_loop.leaders}')
        print('starting second loop...')
        second_loop = dfs_loop(
            {k:self.graph[k]['outgoing'] for k in self.graph.keys()},
            first_loop.nodes_by_finishing_time
        )
        return second_loop.leaders

def count_occurences(list_in):
    counter = [0] * (len(list_in) + 1)
    for x in list_in:
        if x:
            counter[x] += 1

    return sorted(counter, reverse=True)

def make_pair_from_row(row):
    # apply this to a generator?
    return [int(val) for val in row.strip().split(' ')]

if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename) as f:
        pair_list = [make_pair_from_row(row) for row in f.readlines()]

    g = graph(pair_list)
    leaders = g.find_strongly_connected_components()
    # leaders = leaders[1:]
    print(f'Second Loop Leaders: {leaders}')
    largest_sccs = count_occurences(leaders)
    print(largest_sccs[:10])
