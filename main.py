from patent.USPTO import PatentAnalyzer as USPTO

QUERY = 'CPCL/G06Q and ISD/1/1/2005->1/1/2017'
DEFAULT_PATENT_COUNT = 1024

patent_url_list = USPTO.get_patent_string_url_list(QUERY, DEFAULT_PATENT_COUNT)
print(USPTO.build_patent_property_list([patent_url_list[0]]))