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

def main():
    if len(sys.argv) < 2:
        print('Please pass a filename then pid as a parameter.')
        return

    network_file = sys.argv[1]
    pid = None
    if(len(sys.argv) > 2):
        pid = sys.argv[2]

    network = Network(network_file)
    print()

if __name__== "__main__":
  main()