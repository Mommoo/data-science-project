import patent.handler as handler
from patent.property import BasicPatentProperty, PatentLegalEvents


class PatentAnalyzer:
    def __init__(self, USPTO_patent_property) -> None:
        google_patent_url = "https://patents.google.com/patent/%s" % USPTO_patent_property.number

        crawler = handler.Crawler(google_patent_url)

        self.__patent_property = PatentAnalyzer.__wrapping_patent_property(USPTO_patent_property)
        self.__parser = crawler.get_beautiful_soup_parser()
        self.__head_elem = self.__parser.head
        self.__section_elems = self.__parser.find_all('section')

    @classmethod
    def __wrapping_patent_property(cls, USPTO_patent_property) -> BasicPatentProperty:
        patent_property = BasicPatentProperty()
        patent_property.number = USPTO_patent_property.number
        patent_property.title = USPTO_patent_property.title
        return patent_property

    def build_patent_property(self) -> BasicPatentProperty:
        self.__patent_property.abstract = self.__find_abstract()
        self.__patent_property.append_inventor_all(self.__find_inventors())
        self.__patent_property.append_assignee_all(self.__find_assignees())
        self.__patent_property.issued_date = self.__find_issued_date()
        self.__patent_property.submitted_date = self.__find_submitted_date()
        self.__patent_property.append_family_all(self.__find_family())
        self.__patent_property.append_cpc_all(self.__find_cpcs())
        self.__patent_property.claim = self.__find_claim()
        self.__patent_property.put_citation_all(self.__find_citation_dict())
        self.__patent_property.put_cited_all(self.__find_cited_dict())
        self.__patent_property.put_similar_all(self.__find_similar_dict())
        self.__patent_property.append_legal_events_all(self.__find_legal_event_list())
        return self.__patent_property

    def __find_abstract(self) -> str:
        meta_elem = self.__head_elem.find('meta', {"name": "description"})

        if meta_elem is None or meta_elem.has_attr('content') is False:
            return ''
        else:
            return meta_elem['content'].strip()

    @classmethod
    def __parse_content(cls, elem) -> str:
        if elem is not None and elem.has_attr('content'):
            return elem['content']
        else:
            return ''

    @classmethod
    def __parse_contents(cls, elems) -> list:
        if elems is None:
            return []
        else:
            return [PatentAnalyzer.__parse_content(elem) for elem in elems]

    @classmethod
    def __parse_text(cls, elem) -> str:
        if elem is None:
            return ''
        else:
            return elem.text

    def __find_inventors(self) -> list:
        inventor_meta_elems = self.__head_elem.find_all('meta', {"scheme": "inventor"})

        return PatentAnalyzer.__parse_contents(inventor_meta_elems)

    def __find_assignees(self) -> list:
        assignee_meta_elems = self.__head_elem.find_all('meta', {"scheme": "assignee"})

        return PatentAnalyzer.__parse_contents(assignee_meta_elems)

    def __find_issued_date(self) -> str:
        issued_date_meta_elem = self.__head_elem.find('meta', {"scheme": "issue"})

        return PatentAnalyzer.__parse_content(issued_date_meta_elem)

    def __find_submitted_date(self) -> str:
        submitted_date_meta_elem = self.__head_elem.find('meta', {"scheme": "dateSubmitted"})

        return PatentAnalyzer.__parse_content(submitted_date_meta_elem)

    def __find_family(self) -> list:
        family_meta_elems = self.__head_elem.find_all('meta', {"name": "DC.relation"})

        return PatentAnalyzer.__parse_contents(family_meta_elems)

    def __search_section_and_del(self, tag_name, attr_dict, delete):
        target_elems = []
        index = 0
        for section in self.__section_elems:
            target_elems = section.find_all(tag_name, attr_dict)
            if len(target_elems) > 0:
                break

            index += 1

        if len(self.__section_elems) > index and delete:
            del self.__section_elems[index]

        return target_elems

    def __find_cpcs(self) -> list:
        cpc_elem = None

        for section in self.__section_elems:
            h2_elem = section.find('h2')
            if h2_elem is not None and h2_elem.text == 'Classifications':
                cpc_elem = section
                break

        cpc_list = []
        cpc_li_elems = cpc_elem.find_all('li', {"itemprop": "cpcs"})

        if cpc_li_elems is None:
            return []

        for cpc_li_elem in cpc_li_elems:

            leaf_meta = cpc_li_elem.find("meta", {"itemprop": "Leaf"})

            if leaf_meta is not None:
                cpc_span_elem = cpc_li_elem.find("span", {"itemprop": "Code"})
                if cpc_span_elem is not None:
                    cpc_list.append(cpc_span_elem.text)

        return cpc_list

    def __find_claim(self) -> str:
        claim_section = None

        index = 0
        for section in self.__section_elems:
            if section.has_attr('itemprop') and section['itemprop'] == 'claims':
                claim_section = section
                break
            index += 1

        del self.__section_elems[index]

        return PatentAnalyzer.__parse_text(claim_section)

    @classmethod
    def __parse_pair_number_and_date(cls, data_elems) -> dict:
        if data_elems is None:
            return {}

        data_dictionary = {}

        for data_elem in data_elems:
            patent_number = data_elem.find('span', {"itemprop": "publicationNumber"}).text

            patent_priority_date_elem = data_elem.find('td', {"itemprop": "priorityDate"})
            patent_publication_date_elem = data_elem.find('td', {"itemprop": "publicationDate"})

            if patent_priority_date_elem is None and patent_publication_date_elem is None:
                patent_date = ''
            elif patent_priority_date_elem is None or patent_publication_date_elem is None:
                if patent_priority_date_elem is None:
                    patent_date = patent_publication_date_elem.text
                else:
                    patent_date = patent_priority_date_elem.text
            else:
                patent_date = patent_priority_date_elem.text + '~' + patent_publication_date_elem.text

            data_dictionary[patent_number] = patent_date

        return data_dictionary

    def __find_citation_dict(self) -> dict:
        citation_tr_elems = self.__search_section_and_del('tr', {"itemprop": "backwardReferences"}, False)

        return PatentAnalyzer.__parse_pair_number_and_date(citation_tr_elems)

    def __find_cited_dict(self) -> dict:
        cited_tr_elems = self.__parser.find_all('tr', {"itemprop": "forwardReferences"})

        return PatentAnalyzer.__parse_pair_number_and_date(cited_tr_elems)

    def __find_similar_dict(self) -> dict:
        similar_dict = {}
        similar_tr_elems = self.__search_section_and_del('tr', {"itemprop": "similarDocuments"}, True)

        if similar_tr_elems is None:
            return {}

        for similar_tr_elem in similar_tr_elems:
            patent_number_elem = similar_tr_elem.find('span', {"itemprop": "publicationNumber"})
            publication_number_elem = similar_tr_elem.find('time', {"itemprop": "publicationDate"})

            if patent_number_elem is not None:
                similar_dict[patent_number_elem.text] = PatentAnalyzer.__parse_text(publication_number_elem)

        return similar_dict

    def __find_legal_event_list(self) -> list:
        legal_event_list = []
        legal_event_tr_elems = self.__search_section_and_del('tr', {"itemprop": "legalEvents"}, True)

        for legal_event_tr_elem in legal_event_tr_elems:
            patent_legal_event = PatentLegalEvents()
            date_time_elem = legal_event_tr_elem.find('time', {'itemprop': 'date'})
            title_td_elem = legal_event_tr_elem.find('td', {'itemprop': 'title'})

            owner_name_wrapping_p_elems = legal_event_tr_elem.find_all('p', {'itemprop': 'attributes'})
            owner_name_span_elem = None

            for owner_name_wrapping_p_elem in owner_name_wrapping_p_elems:
                label_elem = owner_name_wrapping_p_elem.find('strong', {'itemprop': 'label'})
                if PatentAnalyzer.__parse_text(label_elem) == 'Owner name':
                    owner_name_span_elem = owner_name_wrapping_p_elem.find('span', {'itemprop': 'value'})

            patent_legal_event.title = PatentAnalyzer.__parse_text(title_td_elem)
            patent_legal_event.owner_name = PatentAnalyzer.__parse_text(owner_name_span_elem)
            patent_legal_event.date = PatentAnalyzer.__parse_text(date_time_elem)

            legal_event_list.append(patent_legal_event)

        return legal_event_list
