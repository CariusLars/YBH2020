"""
Parse the dwb Excel
requires xlrd package!
"""

import pandas as pd
import numpy as np

DWB_XLXS = './../data/Mails.xlsx'


def main():
    dwv_excel = parse_xlsx(DWB_XLXS)
    print("Loaded excel, here is an overview:\n", dwv_excel.describe())

def parse_xlsx(fpath):
    raw = pd.read_excel(fpath)
    return raw


if __name__== '__main__':
    main()
