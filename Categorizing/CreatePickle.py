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


def wordcounts(ignore_top=100):
    faqs = './../data/qa_data.xlsx'
    data = pd.read_excel(faqs)
    faqs = {}
    words = {}
    for dpoint in data['Content']:
        words_in_dp = Utils.str_to_words(dpoint)
        words = Utils.words_to_frequency(words_in_dp, words)

        faq_split = dpoint.split('?')
        if len(faq_split) == 2:
            question, answer = faq_split
        elif len(faq_split) > 2:
            question = faq_split[0]
            answer = ' '.join(faq_split[1::])
        else:
            continue
        faqs[question] = answer

    tops = sorted([(f, w) for w, f in words.items() if isinstance(w, str)], reverse=True)
    try:
        tops_x = [entry[1] for entry in tops][:ignore_top]
    except IndexError:
        tops_x = [entry[1] for entry in tops]

    do_pickle(words, n='wordcounts_faq')
    do_pickle(faqs, n='faq')
    do_pickle(tops_x, n='ignore_words')
    return words


if __name__ == '__main__':
    wordcounts()
