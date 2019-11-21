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

class PageRank:
    # class PageRank:
    @staticmethod
    def page_rank(graph, dampening, convergence):
        total_pages = len(graph)
        # this will be added to the final value of each page_rank at the end of an iteration
        dampening_base = (1-dampening)/total_pages
        # initialize ranks with default value of 1/N
        page_ranks = [1/total_pages] * total_pages
        #ensures that the starting value won't break the while loop
        previous_page_ranks = [-convergence * 2] * total_pages
        # the number of outgoing links that each page has
        outgoing_links = [0] * total_pages
        for i in range(len(graph)):
            outgoing_links[i] = PageRank.count_links(graph[i])

        iterations = 0

        # continue until the previous_page_ranks and page_ranks values are less than the convergence value
        while not PageRank.has_converged(previous_page_ranks, page_ranks, convergence):
            previous_page_ranks = page_ranks
            page_ranks = [0] * total_pages

            for i in range(len(graph)):
                num_links_for_page = outgoing_links[i]
                self_page_rank = previous_page_ranks[i] / num_links_for_page

                for j in range(len(graph[i])):
                    connected = graph[i][j]
                    if not connected:
                        continue
                    # add the page_rank value to any connecting nodes
                    page_ranks[j] = page_ranks[j] + self_page_rank

            # multiply by the dampening and add the dampening_base to each page as per the formula
            for i in range(len(page_ranks)):
                page_ranks[i] = page_ranks[i] * dampening
                page_ranks[i] = page_ranks[i] + dampening_base
            iterations = iterations + 1

        return page_ranks, iterations

    @staticmethod
    def count_links(page_links):
        link_count = 0
        #finds the number of links a page has
        for connected in page_links:
            if connected:
                link_count = link_count + 1
        return link_count

    @staticmethod
    def has_converged(previous_page_ranks, page_ranks, convergence):
        # ensures that every value in page_ranks is less than the convergence value
        for i in range(len(previous_page_ranks)):
            difference = abs(page_ranks[i] - previous_page_ranks[i])
            if difference > convergence:
                return False
        return True

    @staticmethod
    def save_results(page_ranks, iterations):
        print_results = 'number of iterations:' + str(iterations) + '\n'
        tuple_array = [(i,page_ranks[i]) for i in range(len(page_ranks))]
        sorted_tuple_array = sorted(tuple_array, key=lambda rank: rank[1], reverse=True)
        print_results = print_results + 'ranking:'
        for node, result in sorted_tuple_array:
            print_results = print_results + str(node) + '(' + str(result) + '),'
        print_results = print_results[:-1]

        with open('output.txt', 'w') as f:
            f.write(print_results)

        print(print_results)

def main():
    if len(sys.argv) < 2:
        print('Please pass a filename then dampening as a parameter.')
        return

    network_file = sys.argv[1]

    dampening = float(sys.argv[2])
    convergence = 1.0e-5

    network = Network(network_file)
    page_ranks, iterations = PageRank.page_rank(network.weighted_adjacency_matrix, dampening, convergence)
    PageRank.save_results(page_ranks, iterations)

if __name__== "__main__":
  main()