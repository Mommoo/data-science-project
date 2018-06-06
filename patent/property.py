# this file is consist of data class

# this data class mainly be used build in patent-title and patent-number of USPTO-patent
#
# @author mommoo
# @date 2018. 06. 04.


class USPTOPatentProperty:

    def __init__(self) -> None:
        self.__number = ''
        self.__title = ''

    @property
    def number(self) -> str:
        return self.__number

    @number.setter
    def number(self, value) -> None:
        if value.find('US') != -1:
            self.__number = value.replace(",", "")
        else:
            self.__number = 'US' + value.replace(",", "")

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value) -> None:
        self.__title = " ".join(value.split())

    def __str__(self) -> str:
        return "\n(number : " + self.__number + ", title : " + self.__title + ")"

    def __repr__(self) -> str:
        return self.__str__()

# this class have role of data object. and inherit class USPTOPatentProperty
# this data class is very important in this project
# using this data class, build data object and set the patent information parsed from the web page ( google-patent )
#
# @author mommoo
# @date 2018. 06. 04.


class BasicPatentProperty(USPTOPatentProperty):

    def __init__(self) -> None:
        super().__init__()
        self.__abstract = ''
        self.__inventor = []
        self.__assignee = []
        self.__issued_date = ''
        self.__submitted_date = ''
        self.__family_list = {}
        self.__cpc = []
        self.__claim = ''
        self.__citation_finder = {}
        self.__cited_finder = {}
        self.__similar_finder = {}
        self.__legal_events = []

    @property
    def abstract(self) -> str:
        return self.__abstract

    @abstract.setter
    def abstract(self, value) -> None:
        self.__abstract = value

    @property
    def inventor(self) -> list:
        return self.__inventor

    def append_inventor_all(self, inventor_list) -> None:
        for inventor in inventor_list:
            self.__inventor.append(inventor)

    @property
    def assignee(self) -> list:
        return self.__assignee

    def append_assignee_all(self, assignee_list) -> None:
        for assignee in assignee_list:
            self.__assignee.append(assignee)

    @property
    def issued_date(self) -> str:
        return self.__issued_date

    @issued_date.setter
    def issued_date(self, value) -> None:
        self.__issued_date = value

    @property
    def submitted_date(self) -> str:
        return self.__submitted_date

    @submitted_date.setter
    def submitted_date(self, value) -> None:
        self.__submitted_date = value

    @property
    def family(self) -> dict:
        return self.__family_list

    def append_family_all(self, family_data_list):

        for family_data in family_data_list:
            family_data_dump = family_data.split(':')
            if len(family_data_dump) > 1:
                key = family_data_dump[0]

                if key in self.__family_list:
                    self.__family_list[key] = self.__family_list[key] + 1
                else:
                    self.__family_list[key] = 1

    @property
    def cpc(self) -> list:
        return self.__cpc

    def append_cpc_all(self, cpc_list):
        for cpc in cpc_list:
            self.__cpc.append(cpc)

    @property
    def claim(self) -> str:
        return self.__claim

    @claim.setter
    def claim(self, value) -> None:
        self.__claim = value

    @property
    def citation(self) -> dict:
        return self.__citation_finder

    def put_citation_all(self, citation_dictionary):
        for patent_number in citation_dictionary:
            self.__citation_finder[patent_number] = citation_dictionary[patent_number]

    @property
    def cited(self) -> dict:
        return self.__cited_finder

    def put_cited_all(self, cited_dictionary):
        for patent_number in cited_dictionary:
            self.__cited_finder[patent_number] = cited_dictionary[patent_number]

    @property
    def similar(self) -> dict:
        return self.__similar_finder

    def put_similar_all(self, similar_dictionary):
        for patent_number in similar_dictionary:
            self.__similar_finder[patent_number] = similar_dictionary[patent_number]

    @property
    def legal_events(self) -> list:
        return self.__legal_events

    def append_legal_events_all(self, legal_events_list):
        for legal_events in legal_events_list:
            self.__legal_events.append(legal_events)

    def __str__(self) -> str:
        return ('(\nnumber         : ' + self.number + "\n" +
                'title          : ' + self.title + "\n" +
                'abstract       : ' + self.__abstract + "\n" +
                'inventor       : ' + str(self.__inventor) + "\n" +
                'assignee       : ' + repr(self.__assignee) + "\n" +
                'issued_date    : ' + self.__issued_date + "\n" +
                'submitted_date : ' + self.__submitted_date + "\n" +
                'family         : ' + str(self.__family_list) + "\n" +
                'cpc            : ' + str(self.__cpc) + "\n" +
                'claim          : ' + self.__claim + "\n" +
                'citation_list  : ' + str(self.__citation_finder) + "\n" +
                'cited_list     : ' + str(self.__cited_finder) + "\n" +
                'similar_list   : ' + str(self.__similar_finder) + "\n" +
                'legal_events   : ' + str(self.__legal_events) + ")")

    def __repr__(self) -> str:
        return self.__str__()


class PatentLegalEvents:
    def __init__(self) -> None:
        self.__title = ''
        self.__owner_name = ''
        self.__date = ''

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value) -> None:
        self.__title = value

    @property
    def owner_name(self) -> str:
        return self.__owner_name

    @owner_name.setter
    def owner_name(self, value) -> None:
        self.__owner_name = value

    @property
    def date(self) -> str:
        return self.__date

    @date.setter
    def date(self, value) -> None:
        self.__date = value

    def __str__(self) -> str:
        return '\n(title : ' + self.__title + " , owner name : " + self.__owner_name + " )"

    def __repr__(self) -> str:
        return self.__str__()
