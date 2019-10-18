import os
import csv

class GraphDAO:
    # get from env
    def __init__(self, input_path = None):
        # Path of the csv passed as env variable
        if input_path is None:
            self.input_path = os.environ['CSV_PATH']
        else:
            self.input_path = input_path
  
    def get_graph(self):
        graph_a = []
        with open(self.input_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                graph_a.append((row[0], row[1], float(row[2])))
        return graph_a


    def append_node_to_graph(self, row):

        try:
            origin = str(row[0])
            destination = str(row[1])
            price = float(row[2])
        except:
            print("bad formatted registar")
            raise Exception("bad formatted registar")
        
        existing = self.get_graph()
        existing.append((origin, destination, price))

        with open(self.input_path, mode='w') as csv_file:
            writer_file = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for path in  existing:
                writer_file.writerow([path[0], path[1], path[2]])
            

