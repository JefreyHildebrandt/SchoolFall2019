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

class Dijkstra:
    def __init__(self, network: Network):
        self.weighted_adjacency_matrix = network.weighted_adjacency_matrix

    def find_shortest_path(self, index_start, index_end):
        vertices_distance = self.get_max_vertices_distance()
        vertices_distance[index_start] = 0
        already_visited = set()
        parent_nodes = [None] * len(vertices_distance)

        while index_end not in already_visited:
            current_index = self.get_smallest_distance_index(vertices_distance, already_visited)
            already_visited.add(current_index)
            # assumes the matrix is a square
            for i in range(len(vertices_distance)):
                next_adjacent_node_dist = self.weighted_adjacency_matrix[current_index][i]
                potential_next_dist = vertices_distance[current_index] + next_adjacent_node_dist

                # this means they aren't connected or already have the minimum
                if next_adjacent_node_dist < 1 or i in already_visited:
                    continue

                if vertices_distance[i] > potential_next_dist:
                    vertices_distance[i] = potential_next_dist
                    parent_nodes[i] = current_index

        return self.get_output_string(index_start, index_end, vertices_distance, parent_nodes)

    def get_path_nodes(self, parent, index, visited_nodes):
        if parent[index] is None:
            visited_nodes += str(index) + ','
            return visited_nodes
        visited_nodes = self.get_path_nodes(parent, parent[index], visited_nodes)
        visited_nodes += str(int(index)) + ','
        return visited_nodes

    def get_output_string(self, index_start, index_end, vertices_distance, parent_nodes):
        start_end_nodes = str(index_start) + ',' + str(index_end)
        nodes_in_path = self.get_path_nodes(parent_nodes, index_end, '')[:-1]
        distance = str(int(vertices_distance[index_end]))
        output_string = start_end_nodes + '\n' + nodes_in_path + '\n' + distance + '\n'
        return output_string

    def get_smallest_distance_index(self, vertices_distance, already_visited):
        smallest = sys.maxsize
        smallest_index = None
        for i in range(len(vertices_distance)):
            dist = vertices_distance[i]
            if dist < smallest and i not in already_visited:
                smallest = dist
                smallest_index = i
        return smallest_index

    def get_max_vertices_distance(self):
        return [sys.maxsize for _ in range(len(self.weighted_adjacency_matrix))]

class Utils:
    @staticmethod
    def remove_letters(string):
        return ''.join(filter(lambda x: x.isdigit(), string))

    @staticmethod
    def shortest_path_to_labels_array(shortest_path, labels):
        return [labels[x] for x in shortest_path]

    @staticmethod
    def print(output_file_name, output_string):
        with open(output_file_name, 'w+') as f:
            f.write(output_string)

def main():
    if len(sys.argv) < 2:
        print('Please pass a filename then pid as a parameter.')
        return

    network_file = sys.argv[1]
    pid = None
    if(len(sys.argv) > 2):
        pid = sys.argv[2]

    network = Network(network_file)
    dijkstra = Dijkstra(network)

    if(pid):
        pid_no_letters = Utils.remove_letters(pid)
        for i in range(len(pid_no_letters) - 2):
            index_start = int(pid_no_letters[i:(i+2)])
            index_end = int(pid_no_letters[(i+1):(i+3)])

            output_name = pid + '.' + str(i) + '.out.txt'
            output_string = dijkstra.find_shortest_path(index_start, index_end)
            Utils.print(output_name, output_string)

    else:
        for index_start, label_start in enumerate(network.labels):
            for index_end, label_end in enumerate(network.labels):
                output_string = dijkstra.find_shortest_path(index_start, index_end)
                print(output_string)


if __name__== "__main__":
  main()
