# -*- coding: utf-8 -*-

import json
import glob
from traceback import format_exc

from multiprocessing import Process

workers = 10

def iterdict(d, seq, fc):
    for k,v in d.items():
        if isinstance(v, dict):
            iterdict(v, seq + "/" + k, fc)
        elif isinstance(v, list):
            for e in v:
                iterdict(e, seq + "/" + k, fc)
        else:
            print(seq + "/" + k + ", " + str(v).replace("\n", '\\n'))
            fc.write(seq + "/" + k + ", " + str(v).replace("\n", '\\n') + "\n")

def multi_proc(json_data_list, output_path):

    for json_name, json_data in json_data_list:
        save_path = output_path + "/" + json_name + ".csv"
        fc = open(save_path, "a")
        fc.write("key, value\n")
        iterdict(json_data, "data", fc)
        fc.close()


def main_convert(input_json_path, output_path):

    json_path = glob.glob(input_json_path + "/*")

    json_data_list = []

    for each_path in json_path:

        each_json_name = each_path.split("/")[-1].split(".")[0]

        f = open(each_path, "r")
        json_data = {}
        try:
            json_data = json.loads(f.read())
        except:
            print(format_exc())

        f.close()
        json_data_list.append([each_json_name, json_data])

    proc_list = []
    for wk in range(workers):
        front = int(len(json_data_list) * (wk / workers))
        rear = int(len(json_data_list) * ((wk + 1) / workers))

        proc = Process(target=multi_proc, args=(json_data_list[front:rear], output_path,))
        proc_list.append(proc)

    for proc in proc_list:
        proc.start()

    for proc in proc_list:
        proc.join()

