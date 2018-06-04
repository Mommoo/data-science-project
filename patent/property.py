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
        self.__inventor = ''
        self.__assignee = ''
        self.__issued_date = ''
        self.__submitted_date = ''
        self.__family = ''
        self.__cpc = ''
        self.__claims = ''
        self.__citation_list = []
        self.__cited_list = []
        self.__similar_list = []

    @property
    def abstract(self) -> str:
        return self.__abstract

    @abstract.setter
    def abstract(self, value) -> None:
        self.__abstract = value

    @property
    def inventor(self) -> str:
        return self.__inventor

    @inventor.setter
    def inventor(self, value) -> None:
        self.__inventor = value

    @property
    def assignee(self) -> str:
        return self.__assignee

    @assignee.setter
    def assignee(self, value) -> None:
        self.__assignee = value

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
    def family(self) -> str:
        return self.__family

    @family.setter
    def family(self, value) -> None:
        self.__family = value

    @property
    def cpc(self) -> str:
        return self.__cpc

    @cpc.setter
    def cpc(self, value) -> None:
        self.__cpc = value

    @property
    def claims(self) -> str:
        return self.__claims

    @claims.setter
    def claims(self, value) -> None:
        self.__claims = value

    def add_citation(self, number, date):
        self.__citation_list.append(PatentNumberAndDate(number, date))

    def add_cited(self, number, date):
        self.__cited_list.append(PatentNumberAndDate(number, date))

    def add_similar(self, number, date):
        self.__similar_list.append(PatentNumberAndDate(number, date))

    def __str__(self) -> str:
        return ('\n(number         : ' + self.__number + "\n" +
                'title          : ' + self.__title + "\n" +
                'abstract       : ' + self.__abstract + "\n" +
                'inventor       : ' + self.__inventor + "\n" +
                'assignee       : ' + self.__assignee + "\n" +
                'issued_date    : ' + self.__issued_date + "\n" +
                'submitted_date : ' + self.__submitted_date + "\n" +
                'family         : ' + self.__family + "\n" +
                'cpc            : ' + self.__cpc + "\n" +
                'claims         : ' + self.__claims + "\n" +
                'citation_list  : ' + str(self.__citation_list) + "\n" +
                'cited_list     : ' + str(self.__cited_list) + "\n" +
                'similar_list   : ' + str(self.__similar_list) + ")")

    def __repr__(self) -> str:
        return self.__str__()

# this data class have two property : patent-title, patent-number
#
# @author mommoo
# @date 2018. 06. 04.


class PatentNumberAndDate:
    def __init__(self, number, date) -> None:
        self.__number = number
        self.__date = date

    @property
    def number(self) -> str:
        return self.__number

    @property
    def date(self) -> str:
        return self.__date

    def __str__(self) -> str:
        return "\n(number : " + self.__number + ", date   : " + self.__date + ")"

    def __repr__(self) -> str:
        return self.__str__()
