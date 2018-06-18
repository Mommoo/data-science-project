import time
from datetime import datetime

class Timer:
    def __init__(self) -> None:
        self.__printed_time = None
        self.__start_time = None
        self.__end_time = None

    def start(self)->None:
        self.__printed_time = datetime.today().strftime("%H:%M:%S")
        self.__start_time = time.time()

    def end(self) -> None:
        self.__end_time = time.time()

    @classmethod
    def __convert_to_time_format(cls, target_time):
        target_time = int(target_time)
        return '{:02d}:{:02d}:{:02d}'.format(target_time // 3600, (target_time % 3600 // 60), target_time % 60)

    def get_start_time(self) -> str:
        return self.__printed_time

    def get_taken_time(self) -> str:
        return Timer.__convert_to_time_format(self.__end_time - self.__start_time)

