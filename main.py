#-*- coding: utf-8 -*-
from typing import List

from patent.USPTO import USPTOPatentAnalyzer
from patent.google import PatentAnalyzer as GooglePatentAnalyzer
from patent.handler import *
from concurrent.futures import *
from mommoo.timer import Timer
from patent.property import USPTOPatentProperty

QUERY = 'CPCL/G06Q and ISD/1/1/2005->1/1/2017'
DIR_PATH = 'C:\\Users\\mommoo.DESKTOP-Q7JLIUA\\Desktop\\repository'
DEFAULT_PATENT_COUNT = 1024


def crawling_google_patent(USPTO_patent_property) -> BasicPatentProperty:
    patent_property = GooglePatentAnalyzer(USPTO_patent_property).build_patent_property()
    return patent_property


def crawling_USPTO_patent(patent_page_url) -> List[USPTOPatentProperty]:
    USPTO_patent_property_list = USPTOPatentAnalyzer.build_USPTO_patent_property_list(patent_page_url)
    return USPTO_patent_property_list


def do_multi_process_google_crawling(USPTO_patent_property_list, progress_count, total_patent_count) -> list:
    with ProcessPoolExecutor(max_workers=50) as executor:
        future_list = []
        google_patent_property_list = []

        for USPTO_patent_url in USPTO_patent_property_list:
            future_list.append(executor.submit(crawling_google_patent, USPTO_patent_url))

        for future in as_completed(future_list):
            google_patent_property = future.result()
            google_patent_property_list.append(google_patent_property)
            progress_count += 1
            (print("patent information({}) crawling successfully..! {}%({}/{})"
                   .format(google_patent_property.number,
                           round(progress_count*100/total_patent_count, 3),
                           progress_count, total_patent_count)))

    return google_patent_property_list


def main():
    timer = Timer()
    timer.start()
    print("crawler start... start time is %s" % timer.get_start_time())

    patent_csv_file_handler = PatentCSVFileHandler(DIR_PATH)
    patent_csv_file_handler.open()
    print("csv files created... ")

    USPTO_analyzer = USPTOPatentAnalyzer(QUERY, DEFAULT_PATENT_COUNT)
    patent_page_url_list = USPTO_analyzer.get_patent_page_url_list()
    total_patent_count = USPTO_analyzer.get_total_patent_count()
    print("build success list of patent-page-url... (number of %d)" % total_patent_count)

    count = 0
    default_pop_size = 10

    while True:
        size = len(patent_page_url_list)
        pop_size = default_pop_size if size > default_pop_size else size-1
        print('pop_size : ' + str(pop_size))
        main_USPTO_patent_property_list = []

        if pop_size == 0:
            break

        with ThreadPoolExecutor(max_workers=default_pop_size) as executor:
            future_list = []

            while pop_size > 0:
                submitted_future = executor.submit(crawling_USPTO_patent, patent_page_url_list.pop(0))
                future_list.append(submitted_future)
                pop_size -= 1

            for completed_future in as_completed(future_list):
                sub_USPTO_patent_property_list = completed_future.result()
                main_USPTO_patent_property_list.extend(sub_USPTO_patent_property_list)

        # print(main_USPTO_patent_property_list)
        patent_property_list = do_multi_process_google_crawling(main_USPTO_patent_property_list, count, total_patent_count)
        print("=======================================================")
        print('try to save csv files...')
        patent_csv_file_handler.append_patent_property_list(patent_property_list)
        print('success save csv files...!!')
        print("=======================================================")
        count += len(patent_property_list)

    patent_csv_file_handler.close()
    timer.end()

    print("all tasks are done!! taken time is %s" % timer.get_taken_time())

if __name__ == '__main__':
    main()
