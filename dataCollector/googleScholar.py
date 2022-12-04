import time
from scholarly import scholarly
import threading
import pandas as pd
import os
import math

# This is a scraper program. Uses Scholarly library. 
# Each paper from the inputted citations is searched and 20 papers that cite it are collected in the table
# The table has a ['to', 'from'] format
#
# Program is capable of running multithreaded, but due to the Google Scholar updates, this may reult in the block

class GoogleScholar:
    def __init__(self, is_thor_enabled=False):
        self.list_citations = pd.DataFrame()
        self.is_thor_enabled = is_thor_enabled

    def restart_tor(self):
        if self.is_thor_enabled: # change the insede if you wish to change Tor to something else.
            os.system("brew services restart tor")
            proxy_generator = ProxyGenerator()
            proxy_generator.Tor_External(9050, 9051, "")
            scholarly_lib.use_proxy(proxy_generator)

        print("tor restarted")

    def __record_citations(self, search_array: list, start_point, article_count, max_depth=20):
        try:
            i = 0 + start_point
            while i < start_point + article_count:
                print(search_array[i])
                root_url = scholarly.search_pubs(search_array[i])
                i = i + 1

                root_publication = next(root_url)
                print("publication " + str(i))
                time.sleep(2)
                if (i - start_point - 1) % 10 == 0 and i - start_point > 9:
                    self.restart_tor()
                try:
                    j = 1
                    for ref_pub in scholarly.search_pubs_custom_url(root_publication['citedby_url']):
                        if j >= max_depth:
                            break
                        j = j + 1

                        try:
                            self.list_citations = self.list_citations.append(
                                pd.DataFrame(
                                    {"to": [[root_publication["bib"]['title'].__str__()
                                             + " - URL: "
                                             + root_publication["pub_url"].__str__()]],
                                     "from": [[ref_pub["bib"]['title'].__str__()
                                               + " - URL: "
                                               + ref_pub["pub_url"].__str__()]]}),
                                ignore_index=True)
                            print(ref_pub["pub_url"].__str__())
                        except:
                            print("Pub_url is empty, ignoring ")
                        print("reference " + str(j))

                except Exception as e:
                    print("exception: ", e)

        except Exception as e:
            print("Something went very wrong: ", e)

    def search_citations(self, citations_file, max_thread_number, max_depth=20):
        thread_list = list()

        citation_PD = list()
        for i, row in citations_file.iterrows():
            print(str(row[0]))
            citation_PD.append(str(row[0]))

        article_number_in_thread = math.ceil(len(citation_PD) / max_thread_number)

        tmp = 0
        while tmp < len(citation_PD):
            thread = threading.Thread(
                target=self.__record_citations, args=(citation_PD, tmp, article_number_in_thread, max_depth))
            thread_list.append(thread)
            thread.start()
            tmp = tmp + article_number_in_thread
            time.sleep(0.05)

        for index, thread in enumerate(thread_list):
            print("Joining thread" + str(index))
            thread.join()
            print("Thread " + str(index) + " is done")

    def search_from_file(self, input_file, num_threads):
        self.restart_tor()
        citations = pd.read_csv(input_file, sep="\n", header=None)
        self.search_citations(citations,
                              max_thread_number=num_threads)
