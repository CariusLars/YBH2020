import pandas as pd
import pickle
import re

TOP_WORDS = './../NLP/top_20_words.csv'

# TODO: Remove category names from important words of other category


def do():
    words = pd.read_csv(TOP_WORDS)
    blacklist = pickle.load(open('blacklist.p', 'rb'))
    # print(words.head(5), '\n' + '-' * 50 + '\n', words.describe())

    categories = words.columns
    parsed = {}
    for cat in categories:
        parsed[cat] = []
        for word in words[cat]:
            if not isinstance(word, str):
                continue
            # Remove common words
            if word in blacklist:
                continue
            # Don't take other categories names as key word
            if word in categories and not word == cat:
                continue
            # And we also don't want to accept integers as 'words'
            if re.fullmatch('[0-9]*', word):
                continue
            parsed[cat].append(word)

    for name, l in parsed.items():
        print('Words in category {}:'.format(name))
        print(l)

    maxlen = min([len(l) for l in parsed])
    take_top = min(maxlen, 15)
    parsed = [l[:take_top] for l in parsed]

    return parsed


if __name__ == '__main__':
    do()
