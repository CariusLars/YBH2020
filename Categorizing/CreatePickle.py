import pandas as pd
import pickle

import ParseMails
import Utils

name = 'blacklist'


def do_pickle(data, n=None):
    if not n:
        n = name
    fname = n + '.p' if not n.endswith('.p') else ''
    pickle.dump(data, open(fname, 'wb'))


def whitelist():
    return ['km', 'tv', 'frage']


def blacklist():
    black_manual = ['ja', 'nein']
    common_words = ParseMails.parse()['Mail']
    words_by_rank = {r: w for w, r in common_words.items()}
    good_words = whitelist()
    black = [words_by_rank[i] for i in range(100)]  # Blacklist the 100 most common words
    black = [f for f in black if f not in good_words]
    black.extend(black_manual)
    do_pickle(black)


def wordcounts():
    faqs = './../data/qa_data.xlsx'
    data = pd.read_excel(faqs)
    words = {}
    for dpoint in data['Content']:
        words_in_dp = Utils.str_to_words(dpoint)
        for w in words_in_dp:
            if w not in words:
                words[w] = 1
            else:
                words[w] += 1
    do_pickle(words, n='wordcounts_faq')
    return words


if __name__ == '__main__':
    wordcounts()
