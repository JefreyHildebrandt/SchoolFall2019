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

class Output:
    def __init__(self, output_file_name):
        self.output_file_name = output_file_name
        self.output = []

    def append_output(self, label_start, label_end, shortest_path, total_cost):
        single_out = []
        single_out.append(', '.join([label_start, label_end]))
        single_out.append(', '.join(shortest_path))
        single_out.append(str(total_cost))
        self.output.append('\n'.join(single_out))

    def print(self):
        for i, output in enumerate(self.output):
            output_file = ''.join([self.output_file_name, '.', str(i), '.txt'])
            print(output_file)
            print(output)
            print()

class Dijkstra:
    def __init__(self, network: Network):
        self.labels = network.labels
        self.weighted_adjacency_matrix = network.weighted_adjacency_matrix

    def find_shortest_path(self, index_start, index_end):
        return [1, 2]

    def find_total_cost(self, shortest_path):
        return 0

class Utils:
    @staticmethod
    def remove_letters(string):
        return ''.join(filter(lambda x: x.isdigit(), string))

    @staticmethod
    def shortest_path_to_labels_array(shortest_path, labels):
        return [labels[x] for x in shortest_path]

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
    output = Output(network_file[:-4] + '.out')

    if(pid):
        pid_no_letters = Utils.remove_letters(pid)
        for i in range(len(pid_no_letters) - 2):
            index_start = int(pid_no_letters[i:(i+2)])
            index_end = int(pid_no_letters[(i+1):(i+3)])

            shortest_path = dijkstra.find_shortest_path(index_start, index_end)
            total_cost = dijkstra.find_total_cost(shortest_path)
            shortest_path_labels = Utils.shortest_path_to_labels_array(shortest_path, dijkstra.labels)
            output.append_output(dijkstra.labels[index_start], dijkstra.labels[index_end], shortest_path_labels, total_cost)
    else:
        for index_start, label_start in enumerate(network.labels):
            for index_end, label_end in enumerate(network.labels):
                if(index_start == index_end):
                    output.append_output(label_start, label_end, [label_start, label_end], 0)
                    continue
                shortest_path = dijkstra.find_shortest_path(index_start, index_end)
                total_cost = dijkstra.find_total_cost(shortest_path)
                shortest_path_labels = Utils.shortest_path_to_labels_array(shortest_path, dijkstra.labels)
                output.append_output(label_start, label_end, shortest_path_labels, total_cost)
    output.print()

if __name__== "__main__":
  main()
