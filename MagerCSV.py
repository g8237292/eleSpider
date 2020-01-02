#!/usr/bin/env python
# encoding: utf-8
'''
@author: allen
@file: MagerCSV.py
@time: 2019/10/15 10:13
'''

import pandas as pd
import os

class MergeCSV:
    def __init__(self):
        self.save_name = "../MergeInfo/all11.csv"
        self.csv_list_path ='../infomation11/'
        self.file_list = os.listdir(self.csv_list_path)

    def run(self):
        for i in self.file_list:
            fr = open(self.csv_list_path + i, 'r').read()
            with open(self.save_name, 'a') as f:
                f.write(fr)


if __name__ == '__main__':

    test = MergeCSV()
    test.run()

