import sys

class Network:
    def __init__(self, input_file):
        network = self.get_network(input_file)
        self.labels = network[0]
        self.weighted_adjacency_matrix = network[1]

    def get_network(self, input_file):
        parsed_file = self.parse_file(input_file)
        labels = []
        weighted_adjacency_matrix = []

        for line in parsed_file:
            labels.append(self.get_label_from_input_line(line))
            weighted_adjacency_matrix.append(self.get_weighted_adjacency_array_from_input_line(line))
        return (labels, weighted_adjacency_matrix)

    def parse_file(self, input_file):
        with open(input_file) as f:
            content = f.readlines()
        return [x.strip() for x in content]

    def get_label_from_input_line(self, line):
        label_line = line.split('\t')[0]
        return label_line

    def get_weighted_adjacency_array_from_input_line(self, line):
        weighted_adjacency_array = line.split('\t')[1].split(',')
        return [float(x) for x in weighted_adjacency_array]

class Prim:
    # finds if the network passed in is a bridge
    # if the minimum spanning tree contains all vertices, then it is not a bridge
    # if the minimum spanning tree separates into two trees then it is a bridge
    @staticmethod
    def is_bridge(graph, starting_index: int, adjacent_index: int) -> bool:
        mst_set = Prim.vertices_in_minimum_spanning_tree(graph, starting_index)
        return starting_index not in mst_set or adjacent_index not in mst_set

    # returns the vertices in the mst as a set, this is used instead of the actual mst since the actual mst isn't needed to tell if the graph is a bridge
    @staticmethod
    def vertices_in_minimum_spanning_tree(graph, starting_index) -> set:
        mst_set = set()
        weights_for_vertices = [sys.maxsize] * len(graph)
        # set starting_index weight to 0 so it will be chosen
        weights_for_vertices[starting_index] = 0

        for _ in range(len(graph)):
            minimum_index = Prim.get_min_unvisited(mst_set, weights_for_vertices)
            if minimum_index == None:
                break
            mst_set.add(minimum_index)

            for adjacent_index in range(len(graph[_])):
                cur_weight = graph[minimum_index][adjacent_index]
                if cur_weight > 0 and adjacent_index not in mst_set and weights_for_vertices[adjacent_index] > cur_weight:
                    weights_for_vertices[adjacent_index] = cur_weight
        return mst_set

    @staticmethod
    def get_min_unvisited(mst_set: set, weights_for_vertices: [int]):
        minimum = sys.maxsize
        minimum_index = None
        for i in range(len(weights_for_vertices)):
            if weights_for_vertices[i] < minimum and i not in mst_set:
                minimum = weights_for_vertices[i]
                minimum_index = i
        return minimum_index

class Fleury:
    @staticmethod
    def fleurys_algorithm(network: Network, starting_index: int):
        graph = network.weighted_adjacency_matrix
        output_circuit = [starting_index]

        while(not Fleury.is_graph_empty(graph)):
            adjacent_vertices = graph[starting_index]
            for adjacent_index in range(len(adjacent_vertices)):
                # assuming the value would be the same in both places for the graph
                weight = graph[starting_index][adjacent_index]
                if weight < 1:
                    continue
                # temporarily remove values from graph
                Fleury.set_value_in_graph(graph, starting_index, adjacent_index, 0)
                is_disconnected_by_itself = Fleury.is_disconnected_by_itself(graph[starting_index])
                is_bridge = Prim.is_bridge(graph, starting_index, adjacent_index)
                if is_bridge or not is_disconnected_by_itself:
                    # reset values if potential new graph might be a bridge
                    output_circuit.append(adjacent_index)
                    starting_index = adjacent_index
                    break
                else:
                    Fleury.set_value_in_graph(graph, starting_index, adjacent_index, weight)

        print(output_circuit)

    @staticmethod
    def is_graph_empty(graph):
        for vertex_connections in graph:
            if not Fleury.is_disconnected_by_itself(vertex_connections):
                return False
        return True

    @staticmethod
    def is_disconnected_by_itself(vertex_connections: [int]):
        for weight in vertex_connections:
            if weight > 0:
                return False
        return True

    @staticmethod
    def set_value_in_graph(graph, starting_index, adjacent_index, value):
        graph[starting_index][adjacent_index] = value
        graph[adjacent_index][starting_index] = value


def main():
    if len(sys.argv) < 2:
        print('Please pass a filename then pid as a parameter.')
        return

    network_file = sys.argv[1]
    pid = None
    if(len(sys.argv) > 2):
        pid = sys.argv[2]

    starting_vertex = int(pid[-2:])

    network = Network(network_file)
    #temp for testing
    network.weighted_adjacency_matrix = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
    ]
    starting_vertex = 0
    # should print:
    # 0, 1, 2, 0
    #end temp for testing
    Fleury.fleurys_algorithm(network, starting_vertex)

if __name__== "__main__":
  main()