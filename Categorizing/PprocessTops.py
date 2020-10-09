import pandas as pd
import pickle

TOP_WORDS = './../NLP/top_10_words.csv'

# TODO: Remove category names from important words of other category


def do():
    words = pd.read_csv(TOP_WORDS)
    blacklist = pickle.load(open('blacklist.p', 'rb'))
    # print(words.head(5), '\n' + '-' * 50 + '\n', words.describe())

    x = 1  # dummy command for debugging


if __name__ == '__main__':
    do()
