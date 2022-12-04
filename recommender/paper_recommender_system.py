import pandas as pd

# This is the Recommender system which uses Paper module.
# Paper module is the module based on 'A Citation-Based Recommender System for Scholarly Paper Recommendation' paper
# Significance threashold is set to 2
# Gets csv path as input and performs the analysis on the network given in the csv

def is_significant(first_dataframe: pd.DataFrame, second_dataframe: pd.DataFrame):
    total_overlap = 0
    for citation in first_dataframe:
        if second_dataframe.__contains__(citation):
            total_overlap = total_overlap + 1
    if total_overlap > 1:
        return 1
    return 0


def new_jaccard_similarity(row: dict):
    bottom = 0
    top = 0

    for element in row.values():
        bottom = bottom + 1
        if element == 1:
            top = top + 1
    return top / bottom


class PaperSimilarityRecommender:
    def __init__(self, csv_path):
        # this creates the variable csv
        self.matrix = pd.DataFrame()
        self.csv = pd.read_csv(csv_path, sep=",", names=["to", "from"],
                               header=0)

    def get_matrix(self):
        init_dataset = self.__read_csv()
        result_matrix = dict()
        for element_1 in init_dataset.keys():
            result_matrix[element_1] = dict()
            for element_2 in init_dataset.keys():

                result_matrix[element_1][element_2] = is_significant(
                    first_dataframe=pd.DataFrame(
                        init_dataset.get(element_1)),
                    second_dataframe=pd.DataFrame(
                        init_dataset.get(element_2)))
        return result_matrix

    def __read_csv(self):
        to_return = dict()
        # recording the df in form <{ ["to"]: ["from"] ["from"] ["from"] }>
        for i, row in self.csv.iterrows():
            to_return.setdefault(str(row["from"]), []).append(str(row["to"]))

        return to_return

    def get_most_similar_recommendation(self, number, matrix: dict):
        self.matrix = matrix
        tmp = dict()
        for key in matrix.keys():
            tmp[key] = [new_jaccard_similarity(matrix.get(key))]

        to_return = pd.DataFrame(list(tmp.items()), columns=['name', 'value'])

        to_return = to_return.sort_values(by="value", ascending=False)
        return to_return['name'][0:number]
