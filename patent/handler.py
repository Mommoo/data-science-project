from mommoo_http import HttpURLConnection
from bs4 import BeautifulSoup

# this class help that crawling web-page-content of url and building parsing-object powered by `BeautifulSoup`
# so, if use class of Crawler you have to need to install 3-th party library ( BeautifulSoup )
# just input "pip install beautifulsoup" in your python enviroment of pip-cmd
#
# @author mommoo
# @date 2018. 06. 03.


class Crawler:
    # @description
    #   this constructor have to need string-url for crawling web-page
    #   after crawling, crawled content will wrapped by BeautifulSoup object
    # @return type : None
    def __init__(self, string_url) -> None:
        url_conn = HttpURLConnection(string_url)

        if url_conn.is_http_ok() is True:
            content = url_conn.get_response()
        else:
            content = ''

        self.__parser = BeautifulSoup(content, "html.parser")

    # @description
    #   get parsing object
    # @return type : BeautifulSoup
    def get_beautiful_soup_parser(self) -> BeautifulSoup:
        return self.__parser
