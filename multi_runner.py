from multiprocessing import Process
import time
import os
from typing import Callable


from cu.cu_item import run as cu_crawler
from gs.gs_item import run as gs_crawler
from seven11.seven11_item import run as seven11_crawler
from emart24.emart24_item import run as emart24_crawler

start_time = time.time()


def runner(crawler: Callable, name: str):
    proc = os.getpid()
    print(f"Process Id: {proc} --> {name} start!!!")
    crawler()
    print(f"Process Id: {proc} --> {name} end!!!")


def run():
    naming = ["cu", "gs", "seven-eleven", "emart24"]
    crawler_arr = [cu_crawler, gs_crawler, seven11_crawler, emart24_crawler]
    procs = []

    for index, crawler in enumerate(crawler_arr):
        proc = Process(target=runner, args=(crawler, naming[index]))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()


if __name__ == "__main__":
    run()
