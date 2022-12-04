# FYP Citations Recommender System

Name: <><><><><><>
Student number: <><><><><>

The project consists of 2 parts. CLI version and the UI. Each build instruction is outlined in the corresponding sections below.

## CLI

### Installation

1. Pull the git project to the Documents folder on macOS under the name of `RecommenderSystem`. (any other folder if you don't wish to use the UI or using Windows or Linux)
2. Install using pip command in all packages outlined in `requirements.txt`.
3. Install tor with brew service if you wish to use the functionality (macOS only). ~This step is not recommended due to the recent changes in google robot detection~

### Usage

1. Write initial 4-6 citations in the txt/CSV file.
2. Run the scraper with the command similar to the following

```shell
python3 scraper.py -i input.txt -o dataset.csv -t -n 10
```

-i stands for input file, -o output file, -t enables Tor interactions and -n identifies the number of threads

Please note, due to the recent changes in google robot detection, using multiple threads and tor functionality may cause errors in scraping. the following command is safe to use.

```shell
python3 scraper.py -i input.txt -o dataset.csv
```

3. Run the analyser methods with with following commands:

```shell
python3 analysis.py -m jaccard -i dataset.csv -o output.csv -n 10
python3 analysis.py -m jaccard_no_division -i dataset.csv -o output.csv -n 10
python3 analysis.py -m network_degree -i dataset.csv -o output.csv -n 10
python3 analysis.py -m network_betweenness -i dataset.csv -o output.csv -n 10
python3 analysis.py -m paper -i dataset.csv -o output.csv -n 10
```

-m stands for method, -i stands for the input file, -o output file and -n number of recommendations

4. Get your answer from the output file (`output.csv` in the example).

## UI

The UI is contained in the MacOSFYPUI folder and is an Xcode project. The instructions on the compilations could be found below

### Installation

1. Install the terminal version of the project into the Documents folder as described above.
2. Navigate to the `RecommenderSystem\MacOSFYPUI`.
3. Open the Xcode project.
4. Build it and move the resulted application to the Applications folder.
5. Give permissions to the application to access the disk on the machine

Now the application should be ready to use

### Usage

In order to use the application the following steps should be performed:

1. Start the application
2. Insert the citations in the input field separated by enter (no more than 6-7 recommended).
3. Pick the number of threads and if you wish to use Tor. (recommended settings: Tor = off and 1 thread)
4. Click the `Collect the data` button.
5. Wait until the data is collected
6. If you wish to use the already collected data, then select the file with the dataset to use, else leave it at the default value.
7. select the method and the number of recommendations you wish to receive
8. the recommendations would be displayed in the bottom right part of the application

## Some possible issues

Q: Scraper doesn't work.

A: Install a Mozilla Firefox browser. It is required in the case of Google Scholar blocking the program with a captcha. Then go to `scholar.google.com` and search for anything. The captcha will be triggered and could be solved. Alternatively, Google may have blocked the IP address, in that case - use another IP or wait for approximately an hour.
