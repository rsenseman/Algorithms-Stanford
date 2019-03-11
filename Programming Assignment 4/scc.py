import sys


class dfs_loop():
    def __init__(self, graph, search_order=None):
        '''variables s and t from lecture are handled by algorithm structure.

        The variable t is implicit as the index of the nodes_by_finishing time
        array to which nodes are appended as they are explored

        The variable s is the node_start argument passed to dfs_iterative. self.s
        is included in the __init__ function to preserve functionality of the
        recursive dfs function
        '''
        self.graph = graph
        self.s = None  # second pass only
        self.search_order = search_order if search_order else list(range(0, len(graph)))  # nodes ordered 0 to n-1
        # print(f'search order: {self.search_order}')
        self.nodes_explored = set()

        self.leaders = [None] * len(graph)
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
        while self.search_order:
            node = self.search_order.pop()
            if node not in self.nodes_explored:
                self.dfs_iterative(node)

    def dfs_iterative(self, node_start):
        dfs_stack = [node_start]

        while dfs_stack:
            node = dfs_stack.pop()
            if node not in self.nodes_explored:
                self.nodes_explored.add(node)
                self.leaders[node] = node_start
                self.nodes_by_finishing_time.append(node)

                for arc in self.graph[node]:
                    if arc not in self.nodes_explored:
                        dfs_stack.append(arc)

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
        print(f'{len(self.graph)} elements added to graph')

    def find_strongly_connected_components(self):
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
    counter = [0] * len(list_in)
    for x in list_in:
        counter[x] += 1

    return sorted(counter, reverse=True)


def make_pair_from_row(row):
    ''' cast strings to integers and subtract one to change from 1-indexed
    to 0-indexed'''
    return [int(val)-1 for val in row.strip().split(' ')]


if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename) as f:
        pair_list = [make_pair_from_row(row) for row in f.readlines()]

    g = graph(pair_list)
    leaders = g.find_strongly_connected_components()
    largest_sccs = count_occurences(leaders)
    print(largest_sccs[:10])
