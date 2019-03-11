import sys


class dfs_loop():
    def __init__(self, graph, search_order=None):
        self.graph = graph
        self.s = None  # second pass only
        self.search_order = search_order if search_order else list(range(1, len(graph) + 1))  # nodes ordered 1 to n
        # print(f'search order: {self.search_order}')
        self.nodes_explored = set()
        self.priority_stack = []

        self.leaders = [None] * (len(graph) + 1)
        self.nodes_by_finishing_time = [] # replacemnt for variable t, only used for first pass

        self.loop()

    def loop(self):
        ''' recursive approach deprecated in favor of iterative approach'''
        # self.loop_recursive()
        self.loop_iterative()

    def loop_iterative(self):
        '''implement iterative dfs to avoid stack overflow. Use a stack
        seperate from search_order to prioritize exploration of node children
        while maintaining record keeping of leaders
        '''
        while self.search_order or self.priority_stack:
            if self.priority_stack:
                node = self.priority_stack.pop()
                if node not in self.nodes_explored:
                    self.dfs_iterative(node)
            else:
                node = self.search_order.pop()
                if node not in self.nodes_explored:
                    self.s = node
                    self.dfs_iterative(node)

    def dfs_iterative(self, node):
        self.nodes_explored.add(node)
        self.leaders[node] = self.s

        for arc in self.graph[node]:
            if arc not in self.nodes_explored:
                self.priority_stack.append(arc)
        self.nodes_by_finishing_time.append(node)

    def loop_recursive(self):
        while self.search_order:
            node = self.search_order.pop()
            if node not in self.nodes_explored:
                self.s = node
                self.dfs_recursive(node)

    def dfs_recursive(self, node):
        self.nodes_explored.add(node)
        self.leaders[node] = self.s

        for arc in self.graph[node]:
            if arc not in self.nodes_explored:
                self.dfs_recursive(arc)
        self.nodes_by_finishing_time.append(node)


class graph():
    def __init__(self, pair_list):
        self.graph = {}

        self._build_graph(pair_list)

    def _build_graph(self, pair_list):
        for x, y in pair_list:
            if x in self.graph:
                self.graph[x]['outgoing'].append(y)
            else:
                self.graph[x] = {'outgoing': [y], 'incoming': []}

            if y in self.graph:
                self.graph[y]['incoming'].append(x)
            else:
                self.graph[y] = {'outgoing': [], 'incoming': [x]}

    def find_strongly_connected_components(self):
        print(f'{max(self.graph)} elements')
        print('starting first loop...')
        first_loop = dfs_loop(
            {k: self.graph[k]['incoming'] for k in self.graph.keys()}
        )
        # print(f'finishing order: {first_loop.nodes_by_finishing_time}')
        print('starting second loop...')
        second_loop = dfs_loop(
            {k: self.graph[k]['outgoing'] for k in self.graph.keys()},
            first_loop.nodes_by_finishing_time
        )
        # print(f'Second Loop Leaders: {first_loop.leaders}')
        return second_loop.leaders


def count_occurences(list_in):
    counter = [0] * (len(list_in) + 1)
    for x in list_in:
        if x:
            counter[x] += 1

    return sorted(counter, reverse=True)


def make_pair_from_row(row):
    return [int(val) for val in row.strip().split(' ')]


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename) as f:
        pair_list = [make_pair_from_row(row) for row in f.readlines()]

    g = graph(pair_list)
    leaders = g.find_strongly_connected_components()
    print(f'Second Loop Leaders: {leaders}')
    largest_sccs = count_occurences(leaders)
    print(largest_sccs[:10])
