import pandas as pd
import sys, getopt

# this script flips files from the ['from', 'to'] format
# to ['to', 'from'] format and the other way around
def main(argv):
    input_file = ''
    output_file = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["input=", "output="])
    except getopt.GetoptError:
        print('python3 csvFormatConverter.py -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("use --input and  --output")
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg

    if input_file == '' or output_file == '':
        print('python3 csvFormatConverter.py -i <input_file> -o <output_file>')
        sys.exit(2)

    df = pd.read_csv(input_file, sep=",", names=["from", "to"])
    df = df.reindex(columns={"to": "from", "from": "to"})
    df.to_csv(output_file, index=False, header=False)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
