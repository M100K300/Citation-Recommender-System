import pandas as pd
import networkx as nx

# This is the network analysis module
# It implements betweenness centrality mesure  as well as degree centrality
# Gets csv path as input and performs the analysis on the network given in the csv
class CitationsNetAnalysis:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def read_csv_to_pandas(self):
        self.csv = pd.read_csv(self.csv_path, sep=",", names=["to", "from"],
                               header=0)  # this creates the variable csv
        print(self.csv.head())

    def get_network(self):
        network = nx.DiGraph()

        for i, row in self.csv.iterrows():
            network.add_edge(row["from"], row["to"])

        print("Nodes", network.number_of_nodes())
        print("Edges", network.number_of_edges())

        return network

    def get_most_degree_central_nodes(self, network, number=10):
        series = pd.Series(nx.degree_centrality(network))
        return self.__get_most_central_nodes(series=series, number=number)

    def get_most_betweenness_central_nodes(self, network, number=10):
        series = pd.Series(nx.betweenness_centrality(network))
        return self.__get_most_central_nodes(series=series, number=number)

    def __get_most_central_nodes(self, series, number):
        # removing initial values
        for paper in series.keys():
            if self.csv["to"].__contains__(paper):
                series = series.drop(paper)

        df = pd.DataFrame(series, columns=["deg_centr"])
        df.sort_values(by="deg_centr", ascending=False)
        df = df.drop(columns="deg_centr")

        return df[0:number]
