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

class PatentAnalyzer:
    __LIST_COUNT = 50  # the count of web-page
    __BASIC_URL_PATTERN = ('http://patft.uspto.gov/netacgi/nph-Parser' +  # the basic pattern url of USPTO-patent
                           '?Sect1=PTO2&Sect2=HITOFF&u=/netahtml/PTO/search-adv.htm&r=0&p=%d&f=S&l=%d&Query=%s&d=PTXT')

    # @description :
    #   it is try to finding the total count of patent through web-page crawling
    # @arg :
    #   encoded_query : encoded query input by user
    # @return type : int
    @classmethod
    def __try_find_total_patent_count(cls, encoded_query) -> int:
        url_for_max_patent_count = cls.__BASIC_URL_PATTERN % (1, 1, encoded_query)

        crawler = handler.Crawler(url_for_max_patent_count)

        parser = crawler.get_beautiful_soup_parser()
        doc = parser.find_all("strong")
        if doc is None:
            return -1
        else:
            return int(doc[len(doc) - 1].get_text())

    # @description :
    #   if failed to finding the total number of patent, the number is replaced with temporary number user entered
    # @arg :
    #   encoded_query : encoded query input by user
    #   default_cont  : temporary number of the total number of patent
    # @return type : int
    @classmethod
    def __get_proper_total_patent_count(cls, encoded_query, default_count) -> int:
        total_patent_count = PatentAnalyzer.__try_find_total_patent_count(encoded_query)
        if total_patent_count == -1:
            total_patent_count = default_count

        return total_patent_count

    # @description :
    #   it is try to finding the max count of web-page
    # @arg :
    #   total_patent_count : the total number of patent
    # @return type : int
    @classmethod
    def __get_max_page_count(cls, total_patent_count) -> int:
        max_page_count = total_patent_count // cls.__LIST_COUNT

        if total_patent_count % cls.__LIST_COUNT == 0:
            max_page_count = max_page_count+1
        else:
            max_page_count = max_page_count+2
        return max_page_count

    # @description :
    #   it is build url-list of USPTO-patent
    # @arg :
    #   query : search data of patent
    #   default_count : temporary number of the total number of patent
    # @return type : list of string-url
    @classmethod
    def get_patent_string_url_list(cls, query, default_count) -> list:
        encoded_query = encoder.quote(query)
        total_patent_count = PatentAnalyzer.__get_proper_total_patent_count(encoded_query, default_count)
        total_patent_count = 40  # for test
        patent_string_url_list = []
        max_page_count = PatentAnalyzer.__get_max_page_count(total_patent_count)

        for page_count in range(1, max_page_count):
            patent_string_url = cls.__BASIC_URL_PATTERN % (page_count, cls.__LIST_COUNT, encoded_query)
            patent_string_url_list.append(patent_string_url)
        return patent_string_url_list

    # @description :
    #   it is build information list of USPTO-patent.
    #   this information is consist of two property of patent-title, patent-number
    #   the two property were parsed from USPTO-patent
    # @arg :
    #   query : search data of patent
    #   default_count : temporary number of the total number of patent
    # @return type : list of string-url
    @classmethod
    def build_patent_property_list(cls, patent_url_list):
        patent_property_list = []

        for patent_url in patent_url_list:

            parser = handler.Crawler(patent_url).get_beautiful_soup_parser()

            table_td = parser.find_all('td', {"valign": "top"})

            patent_index = 0

            for index, elem in enumerate(table_td):
                position = index % 3
                data = elem.string.strip()

                if position == 0:
                    patent_index = int(data) - 1
                    patent_property_list.append(USPTOPatentProperty())
                elif position == 1:
                    patent_property_list[patent_index].number = data
                elif position == 2:
                    patent_property_list[patent_index].title = data

        return patent_property_list
