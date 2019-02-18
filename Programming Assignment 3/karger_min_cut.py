''' randomized contraction algorithm


'''
import random
import sys


class graph():
    def __init__(self, adjacency_list, random_seed=None):
        self.node_collections = {}
        self.edges = []

        self._build_graph_from_list(adjacency_list)
        self.parent_node = list(range(max(self.node_collections)+1))

        # print(f'{len(self.parent_node)} nodes')
        # print(f'{len(self.edges)} edges')

        random.seed(random_seed)
        random.shuffle(self.edges)

    def _build_graph_from_list(self, adjacency_list):
        num_edges = 0
        num_nodes = len(adjacency_list)

        num_edges_added = 0
        num_nodes_added = 0
        num_edges_skipped = 0

        for single_list in adjacency_list:
            num_edges += len(single_list) - 1

            node = single_list[0]
            num_nodes_added += 1

            self.node_collections[node] = {node}

            for adjacent_node in single_list[1:]:
                if adjacent_node > node:
                    self.edges.append((node, adjacent_node))
                    num_edges_added += 1
                else:
                    num_edges_skipped += 1

        # assert num_edges == num_edges_added + num_edges_skipped, 'Edge count mismatch \
        #     {} edges expected, {} edges added'.format(num_edges, num_edges_added)
        # assert num_nodes == num_nodes_added, 'Node count mismatch \
        #     {} nodes expected, {} nodes added'.format(num_nodes, num_nodes_added)

        # print(f'{num_nodes} nodes added')
        # print(f'{num_edges} edges added')
        # print(f'{num_edges_skipped} duplicate edges')
        return None




    def find_min_cut(self):
        '''note: find_min_cut destroys edge list'''
        assert self.edges, "No edges to contract"

        while len(self.node_collections) > 2:
            node_a, node_b = self.edges.pop()
            # print(f'contracting {node_a}, {node_b}...', end=' ')

            # if nodes have the same parent node, then it is a self-link, skip it
            # if nodes have different parent nodes, contract them.
            parent_a, parent_b = self.parent_node[node_a], self.parent_node[node_b]
            if parent_a == parent_b:
                continue
            else:
                # print(f'contracting {parent_a}, {parent_b}', end='\n\n')
                self._contract(parent_a, parent_b)

        # for remaining edges:
        #     if they have the same parent, ignore them
        #     if they have different parents, count them
        num_crossing_edges = 0
        for edge in self.edges:
            node_a, node_b = edge
            if self.parent_node[node_a] != self.parent_node[node_b]:
                num_crossing_edges += 1

        self.edges = []
        return num_crossing_edges

    def _contract(self, node_a, node_b):
        # add all nodes collected under b to collection under a
        self.node_collections[node_a] = self.node_collections[node_a] | self.node_collections[node_b]

        # for nodes in node_b's collection, set parent to node_a
        for node in self.node_collections[node_b]:
            self.parent_node[node] = node_a

        # remove node_b from node_collections
        self.node_collections.pop(node_b)

        return None

if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename) as f:
        contents = f.readlines()

    contents = [
        [eval(val) for val in line.strip('\n').split('\t')[:-1]]
        for line in contents
    ]

    if len(sys.argv) > 2:
        for _ in range(int(sys.argv[2])):
            new_graph = graph(contents)
            min_cut = new_graph.find_min_cut()
            print(min_cut)
    else:
        new_graph = graph(contents)
        min_cut = new_graph.find_min_cut()
        print(f'Min cut: {min_cut}')
