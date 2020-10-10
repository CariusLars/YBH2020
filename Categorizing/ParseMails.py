"""
Parse the dwb Excel
requires xlrd package!
"""

from copy import deepcopy
import numpy as np
import pandas as pd
import random
import re
import Utils

DWB_XLXS = './../data/Mails.xlsx'
RANDOM_NAMES = './../data/random_names.txt'


def as_json(unique_content=False, shortest=None):
    raw = parse_xlsx(DWB_XLXS)
    ret = []
    shortmail_identifier = []
    with open(RANDOM_NAMES, 'r') as ntxt:
        names = ntxt.read().split()
    content = ''
    for i, row in raw.iterrows():
        mail = {'input': {'timestamp': None, 'message': '', 'user_name':  '', 'contact_details': '', 'id': -1},
                'output': {'timestamp': None, 'extreme_negative': False, 'category': '',
                           'category_score': None, 'assignee': '', 'answers': []}}
        try:
            if unique_content:
                if content == row['Mail']:
                    continue  # Avoid duplicate messages with different categories
            content = row['Mail']
            mail['input']['message'] = 'Betreff: ' + row['Betreff'] + '\n' + content
            username = random.choice(names)
            mail['input']['user_name'] = username  # Our ground truth is anonymized
            mail['input']['contact_details'] = str(username + '@half.a.chicken.ch')
            mail['input']['id'] = random.randint(0, 2**16-1)
            date_generator = random.random()
            mail['input']['timestamp'] = Utils.random_date('1/1/2020 8:00 AM', '9/10/2020 8:00 PM', '%m/%d/%Y %I:%M %p', date_generator)
            ret.append(mail)

            if shortest is not None:
                chars_in_mail = len(mail['input']['message'])
                shortmail_identifier.append((chars_in_mail, len(ret)-1))

        except TypeError:
            pass  # Ignore rows in wrong format

    if shortest is not None:
        if shortest >= len(shortmail_identifier):
            return ret
        short_ret = []
        shortmail_identifier.sort()
        for i in range(shortest):
            short_ret.append(ret[shortmail_identifier[i][1]])
        return short_ret
    return ret


def parse():
    dwv_df = parse_xlsx(DWB_XLXS)
    # print("Loaded excel, here is an overview:\n", dwv_df.describe())
    unique = dwv_df['Kategorie'].unique()
    # print("{} Unique Categories in the data:\n".format(len(unique)), unique)
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
        txt = Utils.str_to_words(row)
        for word in txt:
            if word in words:
                words[word] += 1
            else:
                words[word] = 0
    wordlist_sorted = sorted([(count, word) for word, count in words.items()], reverse=True)
    return wordlist_sorted


if __name__ == '__main__':
    as_json(shortest=5)
