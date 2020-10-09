"""
Parse the dwb Excel
requires xlrd package!
"""

from copy import deepcopy
import numpy as np
import pandas as pd
import random
import re

DWB_XLXS = './../data/Mails.xlsx'
RANDOM_NAMES = './../data/random_names.txt'


def as_json(unique_content=False):
    raw = parse_xlsx(DWB_XLXS)
    ret = []
    with open(RANDOM_NAMES, 'r') as ntxt:
        names = ntxt.read().split()
    content = ''
    for i, row in raw.iterrows():
        mail = {'input': {'timestamp': None, 'message': '', 'user_name':  '', 'contact_details': ''},
                'output': {'timestamp': None, 'sentiment': [], 'semtiment_prob': None, 'categories': '',
                           'categories_prob': [], 'assignee': '', 'answers': []}}
        try:
            if unique_content:
                if content == row['Mail']:
                    continue  # Avoid duplicate messages with different categories
            content = row['Mail']
            mail['input']['message'] = 'Betreff: ' + row['Betreff'] + '\n' + content
            mail['input']['user_name'] = random.choice(names)  # Our ground truth is anonymized
            ret.append(mail)
        except TypeError:
            pass  # Ignore rows in wrong format

    return raw


def parse():
    dwv_df = parse_xlsx(DWB_XLXS)
    print("Loaded excel, here is an overview:\n", dwv_df.describe())
    unique = dwv_df['Kategorie'].unique()
    print("{} Unique Categories in the data:\n".format(len(unique)), unique)
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
    as_json()
