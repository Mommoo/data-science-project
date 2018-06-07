#-*- coding: utf-8 -*-

from patent.USPTO import USPTOPatentAnalyzer
from patent.google import PatentAnalyzer as GooglePatentAnalyzer
from patent.handler import *
from concurrent.futures import *
from mommoo_timer import Timer
from patent.property import *

QUERY = 'CPCL/G06Q and ISD/1/1/2005->1/1/2017'
DIR_PATH = 'C:\\Users\\mommoo.DESKTOP-Q7JLIUA\\Desktop\\test'
DEFAULT_PATENT_COUNT = 1024
WORKER_COUNT = 50


def crawling_google_patent(USPTO_patent_property):
    patent_property = GooglePatentAnalyzer(USPTO_patent_property).build_patent_property()
    return patent_property


def do_multi_process_crawling(USPTO_patent_property_list, progress_count, total_patent_count) -> list:
    with ProcessPoolExecutor(max_workers=WORKER_COUNT) as executor:
        future_list = []
        patent_property_list = []
        for USPTO_patent_url in USPTO_patent_property_list:
            future_list.append(executor.submit(crawling_google_patent, USPTO_patent_url))

        for future in as_completed(future_list):
            patent_property = future.result()
            patent_property_list.append(patent_property)
            progress_count += 1
            (print("patent information({}) crawling successfully..! {}%({}/{})"
                   .format(patent_property.number, round(progress_count*100/total_patent_count, 3), progress_count, total_patent_count)))

    return patent_property_list


def main():
    patent_csv_file_handler = PatentCSVFileHandler(DIR_PATH)

    timer = Timer()
    timer.start()
    print("crawler start... start time is %s" % timer.get_start_time())

    patent_csv_file_handler.open()
    print("csv files created... ")

    USPTO_patent_analyzer = USPTOPatentAnalyzer(QUERY, DEFAULT_PATENT_COUNT)
    patent_page_url_list = USPTO_patent_analyzer.get_patent_page_url_list()
    total_patent_count = USPTO_patent_analyzer.get_total_patent_count()
    print("build success list of patent-page-url... (number of %d)" % total_patent_count)

    count = 0

    cnt = 0

    while(True):
        size = len(patent_page_url_list)
        pop_size = 10 if size > 10 else size

        def create_property_list(patent_page_url):
            return USPTOPatentAnalyzer.build_USPTO_patent_property_list(patent_page_url)

        property_list = []

        with ThreadPoolExecutor(10) as executor:
            f = []
            for idx in range(0, pop_size):
                f.append(executor.submit(create_property_list, patent_page_url_list.pop(idx)))

            for future in as_completed(f):
                property_list.extend(future.result())

        print(property_list)
        patent_property_list = do_multi_process_crawling(property_list, count, total_patent_count)
        print("=======================================================")
        print('try to save csv files...')
        patent_csv_file_handler.append_patent_property_list(patent_property_list)
        print('success save csv files...!!')
        print("=======================================================")
        count += len(patent_property_list)

    patent_csv_file_handler.close()
    timer.end()

    print("all tasks are done!! take time is %s" % timer.get_take_time())


if __name__ == '__main__':
    main()
