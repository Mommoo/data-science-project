from typing import List

import patent.handler as handler
from patent.property import USPTOPatentProperty
import urllib.parse as encoder

# this class is handling about USPTO-patent
#   first of all, automatically it is find the total number of patents found by the query user entered
#   but if failed to finding the total number of patents, it replaced with a temporary number user entered
#   second of all, it is build the url-list of USPTO-patent needed to crawling then, the url-list is provided to user
#   last of all, is is build the patent information list consisted of parsed USPTO-patent
#   then, the list is provided to user
# @author mommoo
# @date 2018. 06. 02.


class USPTOPatentAnalyzer:
    __LIST_COUNT = 50  # the count of web-page
    __BASIC_URL_PATTERN = ('http://patft.uspto.gov/netacgi/nph-Parser' +  # the basic pattern url of USPTO-patent
                           '?Sect1=PTO2&Sect2=HITOFF&u=/netahtml/PTO/search-adv.htm&r=0&p=%d&f=S&l=%d&Query=%s&d=PTXT')

    # @arg :
    #   query : search data of patent
    #   default_total_size : temporary number of the total number of patent
    def __init__(self, query, default_total_size) -> None:
        self.__encoded_query = encoder.quote(query)
        self.__total_patent_count = self.__try_find_total_patent_count(default_total_size)

    # @description :
    #   it is try to finding the total count of patent through web-page crawling
    # @arg :
    #   default_cont  : temporary number of the total number of patent
    # @return type : int

    def __try_find_total_patent_count(self, default_total_size) -> int:
        url_for_max_patent_count = self.__BASIC_URL_PATTERN % (1, 1, self.__encoded_query)

        print("try auto detect 'the total number of patent'...")
        crawler = handler.Crawler(url_for_max_patent_count)

        parser = crawler.get_beautiful_soup_parser()
        doc = parser.find_all("strong")
        if doc is None:
            print("auto detect failed...")
            return default_total_size
        else:
            total_patent_count = int(doc[len(doc) - 1].get_text())
            print("auto detect success !! total number of patent is %d" % total_patent_count)
            return total_patent_count

    # @description :
    #   it is try to finding the max count of web-page
    # @return type : int

    def __get_max_page_count(self) -> int:
        max_page_count = self.__total_patent_count // self.__LIST_COUNT

        if self.__total_patent_count % self.__LIST_COUNT == 0:
            max_page_count = max_page_count+1
        else:
            max_page_count = max_page_count+2
        return max_page_count

    # @description :
    #   it is build url-list of USPTO-patent
    # @return type : list of page-url
    def get_patent_page_url_list(self) -> list:
        patent_string_url_list = []
        max_page_count = self.__get_max_page_count()

        for page_count in range(1, max_page_count):
            patent_string_url = self.__BASIC_URL_PATTERN % (page_count, self.__LIST_COUNT, self.__encoded_query)
            patent_string_url_list.append(patent_string_url)
        return patent_string_url_list

    # @description :
    #   it is build information list of USPTO-patent.
    #   this information is consist of two property of patent-title, patent-number
    #   the two property were parsed from USPTO-patent
    # @arg :
    #   patent_url : patent url
    # @return type : list of USPTOPatentProperty
    @classmethod
    def build_USPTO_patent_property_list(cls, patent_url) -> List[USPTOPatentProperty]:
        patent_property_list = []

        parser = handler.Crawler(patent_url).get_beautiful_soup_parser()

        table_td = parser.find_all('td', {"valign": "top"})

        patent_index = -1

        for index, elem in enumerate(table_td):
            position = index % 3
            data = elem.string.strip()

            if position == 0:
                patent_index += 1
                patent_property_list.append(USPTOPatentProperty())
            elif position == 1:
                patent_property_list[patent_index].number = data
            elif position == 2:
                patent_property_list[patent_index].title = data

        return patent_property_list

    def get_total_patent_count(self) -> int:
        return self.__total_patent_count
