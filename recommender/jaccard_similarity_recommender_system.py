import pandas as pd

# This is the Recommender system which uses Jaccard Similarity module
# It implements both a recommender with jaccard similarity mesure and a ecommender with jaccard similarity without devision
# Gets csv path as input and performs the analysis on the network given in the csv
class JaccardSimilarityRecommender:
    def __init__(self, csv_path):
        # this creates the variable csv
        self.matrix = pd.DataFrame()
        self.csv = pd.read_csv(csv_path, sep=",", names=["to", "from"],
                               header=0)

    def get_matrix_jaccard(self):
        init_dataset = self.__read_csv()
        result_matrix = pd.DataFrame(columns=["first", "second", "similarity"])
        for element_1 in init_dataset.keys():
            for element_2 in init_dataset.keys():
                # checking if such values have already been compared
                if not (result_matrix["second"].values.__contains__(str(element_1))
                        and result_matrix["first"].values.__contains__(str(element_2))):
                    result_matrix = result_matrix.append(pd.DataFrame([[str(element_1),
                                                                        str(element_2),
                                                                        float(self.__jaccard_similarity(
                                                                            first_dataframe=pd.DataFrame(
                                                                                init_dataset.get(element_1)),
                                                                            second_dataframe=pd.DataFrame(
                                                                                init_dataset.get(element_2))))
                                                                        ]],
                                                                      columns=["first", "second", "similarity"]),
                                                         ignore_index=True)

        return result_matrix.sort_values(by="similarity", ascending=True)

    def get_matrix_no_division(self):
        init_dataset = self.__read_csv()
        result_matrix = pd.DataFrame(columns=["first", "second", "similarity"])
        for element_1 in init_dataset.keys():
            for element_2 in init_dataset.keys():
                # checking if such values have already been compared
                if not (result_matrix["second"].values.__contains__(str(element_1))
                        and result_matrix["first"].values.__contains__(str(element_2))):
                    result_matrix = result_matrix.append(pd.DataFrame([[str(element_1),
                                                                        str(element_2),
                                                                        float(self.__jaccard_similarity_no_division(
                                                                            first_dataframe=pd.DataFrame(
                                                                                init_dataset.get(element_1)),
                                                                            second_dataframe=pd.DataFrame(
                                                                                init_dataset.get(element_2))))
                                                                        ]],
                                                                      columns=["first", "second", "similarity"]),
                                                         ignore_index=True)

        return result_matrix.sort_values(by="similarity", ascending=True)

    def __read_csv(self):
        to_return = dict()
        # recording the df in form <{ ["to"]: ["from"] ["from"] ["from"]... }>
        for i, row in self.csv.iterrows():
            to_return.setdefault(str(row["from"]), []).append(str(row["to"]))

        return to_return

    def __jaccard_similarity(self, first_dataframe: pd.DataFrame, second_dataframe: pd.DataFrame):
        cite_paper_list = pd.concat([first_dataframe, second_dataframe]).drop_duplicates().reset_index(drop=True)

        top = 0
        bottom = cite_paper_list.size

        if bottom == 0:
            return 0

        for citation in first_dataframe:
            if second_dataframe.__contains__(citation):
                top = top + 1

        return top / bottom

    def __jaccard_similarity_no_division(self, first_dataframe: pd.DataFrame, second_dataframe: pd.DataFrame):
        top = 0

        for citation in first_dataframe:
            if second_dataframe.__contains__(citation):
                top = top + 1

        return top

    def get_most_similar_recommendation(self, number, matrix):
        self.matrix = matrix
        to_return = pd.DataFrame(columns=["paper", "recommendation"])
        # summing all similarities, as we care about the total similarity in the dataset
        for i, row in self.matrix.iterrows():
            if to_return["paper"].values.__contains__(row["first"]):
                j = to_return[to_return["paper"] == row["first"]].index.values
                to_return["recommendation"][j] = str(float(to_return["recommendation"][j]) + float(row["similarity"]))
            else:
                to_return = to_return.append(
                    pd.DataFrame([[row["first"], str(row["similarity"])]], columns=["paper", "recommendation"]),
                    ignore_index=True)

        # removing all values initially given in the input
        for i in to_return["paper"]:
            for j in self.csv["to"].unique():
                if str(i) == str(j):
                    to_return = to_return[to_return["paper"] != i]

        to_return = to_return.sort_values(by="recommendation", ascending=False)
        to_return.reset_index(drop=True, inplace=True)
        return to_return["paper"][0:number]
