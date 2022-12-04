import sys, getopt

from dataCollector.googleScholar import GoogleScholar

# This file is the controlls for scraper
def main(argv):
    input_file = ''
    output_file = ''
    threads_number = 1
    tor_enabled = False
    try:
        opts, args = getopt.getopt(argv, "hti:o:n:", ["input=", "tor", "output=", "number="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("use --input, --output, --tor and --number")
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-n", "--number"):
            threads_number = int(arg)
        elif opt in ("-t", "--tor"):
            tor_enabled = True

    google = GoogleScholar(is_thor_enabled=tor_enabled)
    google.search_from_file(input_file=input_file, num_threads=threads_number)
    google.list_citations.to_csv(output_file, index=False, header=False)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print("no input") # this is used by the ui, as it reads this file as another class. preventing code duplication
