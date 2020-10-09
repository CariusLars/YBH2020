import pickle

import ParseMails

name = 'blacklist'


def do_pickle(data, n=None):
    if not n:
        n = name
    fname = n + '.p' if not n.endswith('.p') else ''
    pickle.dump(data, open(fname, 'wb'))


def whitelist():
    return ['km', 'tv', 'frage', ]


def blacklist():
    black_manual = ['ja', 'nein']
    common_words = ParseMails.parse()['Mail']
    words_by_rank = {r: w for w, r in common_words.items()}
    good_words = whitelist()
    black = [words_by_rank[i] for i in range(100)]  # Blacklist the 100 most common words
    black = [f for f in black if f not in good_words]
    black.extend(black_manual)
    do_pickle(black)


if __name__ == '__main__':
    blacklist()
