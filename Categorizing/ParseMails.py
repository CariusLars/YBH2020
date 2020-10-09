"""
Parse the dwb Excel
requires xlrd package!
"""

from copy import deepcopy
import numpy as np
import pandas as pd
import re

DWB_XLXS = './../data/Mails.xlsx'


def parse():
    dwv_df = parse_xlsx(DWB_XLXS)
    print("Loaded excel, here is an overview:\n", dwv_df.describe())
    unique = dwv_df['Kategorie'].unique()
    print("{} Unique Categories in the data:\n".format(len(unique)), unique)
    dwf_dict = dwv_df.to_dict()
    # mail_wordcount = count_occurences(dwv_df['Mail'])
    tops = top_words(dwv_df[['Mail', 'Betreff', 'Kategorie']])
    return tops


def top_words(df):
    top = {}
    for col in df.columns:
        sorted_list = count_occurences(df[col])
        top[col] = {word: i for i, (_, word) in enumerate(sorted_list)}
    return top

# Internet und TV ist ganze Schweiz, Strom und Glasfaser nicht. Zzev ist auch schweiz-weit


def parse_xlsx(fpath):
    raw = pd.read_excel(fpath)
    # Split multiple categories:
    iterator_df = deepcopy(raw)
    for idx, row in iterator_df.iterrows():
        if ',' in row['Kategorie']:
            cats = [s.strip() for s in row['Kategorie'].split(',')]
            raw.drop(idx, inplace=True)
            for cat in cats:
                single = deepcopy(row)
                single['Kategorie'] = cat
                raw = raw.append(single)
    return raw


def count_occurences(series):
    """Dont use this, return will change!"""
    words = {}
    for row in series:
        if pd.isna(row):
            continue
        txt = re.split(' |\n|\\.|/', row)
        # Split the words in the mail, delete punctiation and delete words that are actually only punctuation
        # We ignore upper/lower case
        txt = [t.strip().lower() for t in txt if not re.fullmatch('[ ,.]*', t)]
        for word in txt:
            if word in words:
                words[word] += 1
            else:
                words[word] = 0
    wordlist_sorted = sorted([(count, word) for word, count in words.items()], reverse=True)
    return wordlist_sorted


if __name__ == '__main__':
    parse()
