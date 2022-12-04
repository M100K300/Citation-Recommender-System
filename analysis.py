from networkAnalysys.citations_net_analysys import CitationsNetAnalysis
import sys, getopt

from recommender.jaccard_similarity_recommender_system import JaccardSimilarityRecommender
from recommender.paper_recommender_system import PaperSimilarityRecommender

# This file is controlling the analysis methods. 
def main(argv):
    input_file = ''
    output_file = ''
    number_recommendations = 10
    method = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:n:m:", ["input=", "output=", "number=", "method="])
    except getopt.GetoptError:
        print('python3 analysis.py -i <input_file> -o <output_file> -m <method_name> -n <number_of_items>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("use --input --output, --method and --number")
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-n", "--number"):
            number_recommendations = int(arg)
        elif opt in ("-m", "--method"):
            method = arg.lower()

    if method.__eq__("network_degree"):
        test_class = CitationsNetAnalysis(csv_path=input_file)
        test_class.read_csv_to_pandas()
        flw = test_class.get_network()
        result = test_class.get_most_degree_central_nodes(flw, number=number_recommendations)
        print("Output: <{")
        for rec in result.index: 
            print(str(rec))
        print("}>")
        result.to_csv(output_file, header=False)
        print("Data saved in: <{" + output_file + "}>")

    elif method.__eq__("network_betweenness"):
        test_class = CitationsNetAnalysis(csv_path=input_file)
        test_class.read_csv_to_pandas()
        flw = test_class.get_network()
        result = test_class.get_most_betweenness_central_nodes(flw, number=number_recommendations)
        print("Output: <{")
        for rec in result.index: 
            print(str(rec))
        print("}>")
        result.to_csv(output_file, header=False)
        print("Data saved in: <{" + output_file + "}>")

    elif method.__eq__("jaccard"):
        test_class = JaccardSimilarityRecommender(csv_path=input_file)
        matrix = test_class.get_matrix_jaccard()
        flw = test_class.get_most_similar_recommendation(number=number_recommendations, matrix=matrix)
        print("Output: <{")
        for rec in list(flw): 
            print(str(rec))
        print("}>")

        flw.to_csv(output_file, index=False, header=False)
        print("Data saved in: <{" + output_file + "}>")

    elif method.__eq__("jaccard_no_division"):
        test_class = JaccardSimilarityRecommender(csv_path=input_file)
        matrix = test_class.get_matrix_no_division()
        flw = test_class.get_most_similar_recommendation(number=number_recommendations, matrix=matrix)
        print("Output: <{")
        for rec in list(flw): 
            print(str(rec))
        print("}>")
        flw.to_csv(output_file, index=False, header=False)
        print("Data saved in: <{" + output_file + "}>")

    elif method.__eq__("paper"):
        test_class = PaperSimilarityRecommender(csv_path=input_file)
        matrix = test_class.get_matrix()
        flw = test_class.get_most_similar_recommendation(number=number_recommendations, matrix=matrix)
        print("Output: <{")
        for rec in list(flw): 
            print(str(rec))
        print("}>")
        flw.to_csv(output_file, index=False, header=False)
        print("Data saved in: <{" + output_file + "}>")

    else:
        print("There is no such method: <{" + method + "}>")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print("no input")  # this is used by the ui, as it reads this file as another class. preventing code duplication
