import urllib.request as url_request

# this class have the role of handling http connect
# @author mommoo
# @date 2018. 06. 02.


class HttpURLConnection:
    __INVALID_RESULT = 'NONE'  # invalid string data

    # @description :
    #   this constructor have to need url string data
    # @return type : None
    def __init__(self, string_url) -> None:
        self.string_url = string_url
        self.open_result = self.__INVALID_RESULT
        self.response_txt = self.__INVALID_RESULT
        self.status_code = self.__INVALID_RESULT

    """
        :return 
    """
    # @description :
    #   try http connect if not try previously
    # @return type : None
    def __open_connect_if_not_open(self) -> None:
        if self.open_result == self.__INVALID_RESULT:
            self.open_connection()

    # @description :
    #   try http connect from server of input url
    #   set http response data ( content, status-code )
    # @return type : None
    def open_connection(self) -> None:
        self.open_result = url_request.urlopen(self.string_url)

        charset = self.open_result.info().get_content_charset()
        if charset is None:
            charset = 'utf-8'

        self.response_txt = self.open_result.read().decode(charset)
        self.status_code = str(self.open_result.getcode())

    # @description :
    #   get web-page content
    # @return type : string
    def get_response(self) -> str:
        self.__open_connect_if_not_open()

        return self.response_txt

    # @description :
    #   get integer http status code about http connect result
    #   200 ~ : http ok ( success )
    #   300 ~ : http ok but, not completed ( half success )
    #   400, 500 ~ : http fail ( fail )
    # @return type : string
    def get_status_code(self) -> str:
        self.__open_connect_if_not_open()

        return self.status_code

    # @description :
    #   whether http connect success or fail
    # @return type : boolean
    def is_http_ok(self) -> bool:
        return self.get_status_code() == '200'

    # @description :
    #   string information of this class
    # @return type : string
    def __str__(self) -> str:
        self.__open_connect_if_not_open()

        return '## status code   : ' + self.get_status_code() + '\n## response text : ' + self.get_response()
