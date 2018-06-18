from abc import *
from mommoo.http import HttpURLConnection
from mommoo.file import CSVFileRepository
from patent.property import BasicPatentProperty
from threading import Lock
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


class CommonPatentCSVRepository(metaclass=ABCMeta):

    def __init__(self, dir_path) -> None:
        self.__file_handler = None
        self.__dir_path = dir_path

    @abstractmethod
    def get_column(self) -> list:
        pass

    @abstractmethod
    def get_file_name(self) -> str:
        pass

    @abstractmethod
    def convert_to_data_row(self, patent_property: BasicPatentProperty):
        pass

    def open(self) -> None:
        self.__file_handler = CSVFileRepository(self.__dir_path, self.get_file_name())
        self.__file_handler.open()
        self.__file_handler.set_column(self.get_column())

    def close(self) -> None:
        self.__file_handler.close()

    def append_patent_data_row_list(self, patent_property_list: list) -> None:
        row_data_list = []
        for patent_property in patent_property_list:
            row_data_list.append(self.convert_to_data_row(patent_property))

        self.__file_handler.add_row_list(row_data_list)


class BasicPatentCSVRepository(CommonPatentCSVRepository):

    def get_column(self) -> list:
        return (['patent_number',
                 'patent_title',
                 'abstract',
                 'inventor',
                 'assignee',
                 'issued_date',
                 'submitted_date',
                 'family',
                 'cpc',
                 'claims'])

    def get_file_name(self) -> str:
        return 'basic_table.csv'

    def convert_to_data_row(self, patent_property: BasicPatentProperty):
        return ([patent_property.number,
                 patent_property.title,
                 patent_property.abstract,
                 patent_property.inventor,
                 patent_property.assignee,
                 patent_property.issued_date,
                 patent_property.submitted_date,
                 patent_property.family,
                 patent_property.cpc,
                 patent_property.claim])


class CitationPatentCSVRepository(CommonPatentCSVRepository):

    def get_column(self) -> list:
        return (['patent_number',
                 'citation'])

    def get_file_name(self) -> str:
        return 'citation_table.csv'

    def convert_to_data_row(self, patent_property: BasicPatentProperty):
        return ([patent_property.number,
                 patent_property.citation])


class CitedPatentCSVRepository(CommonPatentCSVRepository):

    def get_column(self) -> list:
        return (['patent_number',
                 'cited'])

    def get_file_name(self) -> str:
        return 'cited_table.csv'

    def convert_to_data_row(self, patent_property: BasicPatentProperty):
        return ([patent_property.number,
                 patent_property.cited])


class SimilarPatentCSVRepository(CommonPatentCSVRepository):

    def get_column(self) -> list:
        return (['patent_number',
                 'similar'])

    def get_file_name(self) -> str:
        return 'similar_table.csv'

    def convert_to_data_row(self, patent_property: BasicPatentProperty):
        return ([patent_property.number,
                 patent_property.similar])


class AssignmentPatentCSVRepository(CommonPatentCSVRepository):

    def get_column(self) -> list:
        return (['patent_number',
                 'assignment_count',
                 'assignment_info',
                 'transfer'])

    def get_file_name(self) -> str:
        return 'assignment_table.csv'

    def convert_to_data_row(self, patent_property: BasicPatentProperty):
        event_analyzer = LegalEventsAnalyzer(patent_property.legal_events)
        assignment_count = event_analyzer.get_assignment_count()
        assignment_info = event_analyzer.get_assignment_info()
        transfer_result = 1 if assignment_count >= 2 else 0
        return ([patent_property.number,
                 assignment_count,
                 assignment_info,
                 transfer_result])


class LegalEventsAnalyzer:
    def __init__(self, legal_events_list) -> None:
        self.__assignment_count = 0
        self.__assignment_info = []

        for index, legal_events in enumerate(legal_events_list):
            if index is 0:
                continue

            if LegalEventsAnalyzer.__is_transfer(legal_events_list, index):
                self.__assignment_count += 1
                legal_event = legal_events_list[index]
                self.__assignment_info.append(legal_event.owner_name + '(' + legal_event.date + ")")

    def get_assignment_count(self) -> int:
        return self.__assignment_count

    def get_assignment_info(self) -> str:
        return ",".join(self.__assignment_info)

    @classmethod
    def __is_transfer(cls, legal_events_list, index) -> bool:
        upper_legal_events = legal_events_list[index - 1]
        current_legal_events = legal_events_list[index]

        if upper_legal_events.title != 'Assignment' and current_legal_events.title == 'Assignment':
            return True
        elif upper_legal_events.title == 'Assignment' and current_legal_events.title == 'Assignment':
            if upper_legal_events.owner_name != current_legal_events.owner_name:
                return True
            else:
                return False

        return False


class PatentCSVFileHandler:
    def __init__(self, dir_path) -> None:
        self.__file_repo_list = ([
            BasicPatentCSVRepository(dir_path),
            CitationPatentCSVRepository(dir_path),
            CitedPatentCSVRepository(dir_path),
            SimilarPatentCSVRepository(dir_path),
            AssignmentPatentCSVRepository(dir_path)
        ])
        self.__lock = Lock()

    def open(self):
        for file_repo in self.__file_repo_list:
            file_repo.open()

    def close(self):
        for file_repo in self.__file_repo_list:
            file_repo.close()

    def append_patent_property_list(self, patent_property_list: list):
        with Lock():
            for file_repo in self.__file_repo_list:
                file_repo.append_patent_data_row_list(patent_property_list)
